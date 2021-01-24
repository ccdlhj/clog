# -*- coding:utf-8 -*-
import calendar
import csv
import codecs
import json

import datetime
import os
import socket
import zipfile
import shutil
from itertools import chain

from oslo_utils import uuidutils

from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from cloud_log.models.clog import Clog
from cloud_log.rest.v_1.clog import service
from cloud_log.utils import websocket, taskinfo
from cloud_log.tasks.clog import utils
from cloud_log.utils.constants import CLOG_CSV_PATH, NFS_CLOG_PATH, NFS_CLOG_NGINX_PORT, MESSAGE_TYPE, \
    TASK_STATUS, PROCESS, CSV_TITLE_CN, CLOG_EXPORT_MAX_SIZE, FILTER_NAME_CN, clog_filter_keys, FILE_BINARY_SIZE
from cloud_log.utils.create_model import get_model, generate_all_clog_table_name
from cloud_log.utils.taskinfo import update_task_info
from cloud_log.utils.constants import CLOG_ACTIONS


def get_clog_zip_size_name(size, FILE_BINARY_SIZE=1, BINARY_NAME=None):
    return '%.2f' % float(size / FILE_BINARY_SIZE) + BINARY_NAME


def get_clog_zip_size(NFS_CLOG_PATH, export_clog_zip_name):
    size = os.path.getsize(NFS_CLOG_PATH + export_clog_zip_name + '.zip')
    if size < FILE_BINARY_SIZE.KB:
        return get_clog_zip_size_name(size, FILE_BINARY_SIZE=FILE_BINARY_SIZE.B, BINARY_NAME='B')
    elif FILE_BINARY_SIZE.KB <= size < FILE_BINARY_SIZE.MB:
        return get_clog_zip_size_name(size, FILE_BINARY_SIZE=FILE_BINARY_SIZE.KB, BINARY_NAME='KB')
    elif FILE_BINARY_SIZE.MB <= size < FILE_BINARY_SIZE.GB:
        return get_clog_zip_size_name(size, FILE_BINARY_SIZE=FILE_BINARY_SIZE.MB, BINARY_NAME='MB')
    elif FILE_BINARY_SIZE.GB <= size < FILE_BINARY_SIZE.TB:
        return get_clog_zip_size_name(size, FILE_BINARY_SIZE=FILE_BINARY_SIZE.GB, BINARY_NAME='GB')
    elif FILE_BINARY_SIZE.TB <= size:
        return get_clog_zip_size_name(size, FILE_BINARY_SIZE=FILE_BINARY_SIZE.TB, BINARY_NAME='TB')


def get_export_clog_filter(filters):
    for filter_data in filters:
        filter_dict = {}
        filter_name = filter_data.get('Name')
        filter_value = filter_data.get('Values')[0]
        if filter_name.endswith('__icontains'):
            name = filter_name.replace('__icontains', '')
        else:
            name = filter_name
        if name not in clog_filter_keys:
            continue
        filter_dict = {
            FILTER_NAME_CN.get(name.upper()): filter_value
        }
    return filter_dict


def build_filter_query(filters):
    query_filter = Q()
    if not filters:
        return filters
    for i in filters:
        k = i.get('Name')
        values = i.get('Values')
        if not k or not values:
            continue
        for value in values:
            query_filter |= Q(**{k: value})
    return query_filter


def build_order_by(sorting):
    order_bys = []
    if sorting:
        key = sorting['key']
        order = sorting['order']
        if order == 'asc':
            oder_by = key
        else:
            oder_by = '-' + key
        order_bys.append(oder_by)
    else:
        order_bys = ['-created_at']
    return order_bys


def generate_export_clog_zip_name(now_time, clog_uuid):
    return 'clog' + '_' + '{}'.format(now_time.year) \
           + '{}'.format(now_time.month) + '{}'.format(now_time.day) + '_' + clog_uuid


def generate_clog_export_url(export_clog_zip_name):
    return export_clog_zip_name + '.zip'


def generate_csv_path(export_clog_dir_path, csv_file_name):
    return export_clog_dir_path + '/' + csv_file_name


def generate_export_clog_absolute_path(export_clog_zip_name):
    path = CLOG_CSV_PATH
    return path + export_clog_zip_name


def genarate_csv_file_name(export_clog_dir_path, export_clog_zip_name):
    dir_num = os.listdir(export_clog_dir_path)
    clog_slicer = len(dir_num) + 1
    return export_clog_zip_name + '_' + '{}'.format(clog_slicer) + '.csv'


def wirte_export_clog_in_csv_file(clog_csv_datas, clog_path):
    # write csv title
    with codecs.open(clog_path, 'ab+', 'utf-8') as csvfile:
        csv_write = csv.writer(csvfile)
        csv_write.writerow(CSV_TITLE_CN)
        for clog_datas in clog_csv_datas:
            for clog_data in clog_datas:
                if clog_data.status == 'SUCCESS':
                    clog_data_status = '成功'
                else:
                    clog_data_status = '失败'
                origin_data = json.dumps(clog_data.origin_data, encoding='UTF-8', ensure_ascii=False)
                if origin_data == u'{"clog_operation_message": "\u65e0"}':
                    origin_data = '无'
                expected_data = json.dumps(clog_data.expected_data, encoding='UTF-8', ensure_ascii=False)
                if expected_data == u'{"clog_operation_message": "\u65e0"}':
                    expected_data = '无'
                result_data = json.dumps(clog_data.result_data, encoding='UTF-8', ensure_ascii=False)
                if result_data == u'{"clog_operation_message": "\u65e0"}':
                    result_data = '无'
                csv_write.writerow([clog_data.request_id, clog_data.object_uuid,
                                    clog_data.object_name, clog_data.object_type,
                                    clog_data.res_org_path, clog_data.user_name,
                                    clog_data.user_id, clog_data.ip_address,
                                    clog_data.operation_id, clog_data.operation_name,
                                    clog_data_status, clog_data.created_at,
                                    clog_data.updated_at,
                                    origin_data, expected_data,
                                    result_data])


def genarate_csv_files(param, clog_table_names, export_clog_dir_path, export_clog_zip_name):
    # get clog data
    clog_csv_datas = []
    has_clog_data_count = 0
    clog_export_start_index = 0
    clog_export_end_index = CLOG_EXPORT_MAX_SIZE
    for clog_table_name in clog_table_names:
        clog_model = get_model(clog_table_name, Clog)
        query = build_filter_query(param.get('filters'))
        order_by = build_order_by(param.get('Sorting'))
        clogs = service.get_clogs(clog_model, query=query)
        clogs = clogs.order_by(*order_by)
        try:
            clog_datas_num = clogs.count()
        except Exception as e:
            continue
        clog_split_count = clog_datas_num / CLOG_EXPORT_MAX_SIZE
        # 生成日志的csv文件
        for clog_aplit in range(0, clog_split_count + 1):
            if clog_datas_num > 0:
                clog_split = clogs[clog_export_start_index: clog_export_end_index]
                clog_csv_datas.append(clog_split)
                has_clog_data_count += clog_split.count()
                if has_clog_data_count == CLOG_EXPORT_MAX_SIZE:
                    # 生成csv文件名称
                    csv_file_name = genarate_csv_file_name(export_clog_dir_path, export_clog_zip_name)

                    # 生成csv文件的相对路径
                    clog_csv_path = generate_csv_path(export_clog_dir_path, csv_file_name)

                    # 把日志数据写进csv文件中
                    wirte_export_clog_in_csv_file(clog_csv_datas, clog_csv_path)
                    clog_export_start_index = clog_export_end_index
                    clog_export_end_index = clog_export_start_index + CLOG_EXPORT_MAX_SIZE
                    has_clog_data_count = 0
                    clog_csv_datas = []
        clog_export_start_index = 0
        clog_export_end_index = CLOG_EXPORT_MAX_SIZE - has_clog_data_count

    # 判断是否最后有剩余的日志未生成csv文件
    if clog_csv_datas:
        csv_file_name = genarate_csv_file_name(export_clog_dir_path, export_clog_zip_name)
        clog_csv_path = generate_csv_path(export_clog_dir_path, csv_file_name)
        wirte_export_clog_in_csv_file(clog_csv_datas, clog_csv_path)


def compress_zip_file(export_clog_dir_path):
    with zipfile.ZipFile(export_clog_dir_path + '.zip', 'w', zipfile.ZIP_DEFLATED) as clog_zip:
        for dirpath, dirnames, filenames in os.walk(export_clog_dir_path):
            fpath = dirpath.replace(export_clog_dir_path, '')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                clog_zip.write(os.path.join(dirpath, filename), fpath + filename)


def export_clog(context, param):
    task_id = context.get('task_id')
    taskinfo.create_task_log_template(task_id, '日志数据开始导出')
    update_task_info(task_id, status=TASK_STATUS.START, process_status=PROCESS.START)

    # generate clog model name
    start_time = datetime.datetime.strptime(param.get('startTime'), "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime(param.get('endTime'), "%Y-%m-%d %H:%M:%S")
    clog_table_name_sorting = service.get_clog_model_name_order_mode(param.get('Sorting'))
    clog_table_names = generate_all_clog_table_name(start_time, end_time, clog_table_name_sorting)
    clog_uuid = uuidutils.generate_uuid()
    # generate path
    export_clog_zip_name = generate_export_clog_zip_name(datetime.datetime.now(), clog_uuid)
    export_clog_dir_path = generate_export_clog_absolute_path(export_clog_zip_name)
    os.mkdir(export_clog_dir_path)
    # websocket
    message = _('Clog start exporting')
    notify_message = websocket.generate_msg(uuid=uuidutils.generate_uuid(),
                                            action=CLOG_ACTIONS.EXPORT,
                                            message_level=MESSAGE_TYPE.SUCCESS_TYPE,
                                            refush=False, is_alert=True, message=message)
    websocket.notify_msg(context['user_id'], notify_message, message_type=MESSAGE_TYPE.PORTAL_CLOG)
    # genrate csv
    genarate_csv_files(param, clog_table_names, export_clog_dir_path, export_clog_zip_name)

    # generate zip
    compress_zip_file(export_clog_dir_path)
    # change zip path to nfs
    shutil.move(export_clog_dir_path + '.zip', NFS_CLOG_PATH)
    # generate url
    clog_export_url = generate_clog_export_url(export_clog_zip_name)
    # update export clog log
    if param.get('filters'):
        filter = get_export_clog_filter(param.get('filters'))
    else:
        filter = '无'
    # get clog zip size(mb)
    clog_size = get_clog_zip_size(NFS_CLOG_PATH, export_clog_zip_name)
    result_data = {
        "开始时间": param.get('export_clog_log_start_time'),
        "结束时间": param.get('export_clog_log_end_time'),
        "所选择的搜索项": filter,
        "导出文件名称": export_clog_zip_name,
        "导出文件大小": clog_size
    }
    clog_uuid = param.get('export_clog_log_infos')[0].get('clog_uuid')
    utils.update_clog_status(clog_uuid, is_success=True, result_data=result_data)
    message = _('Clog was export successful')
    websocket.update_msg(notify_message, message=message,
                         exoport_url=clog_export_url,
                         export_clog_flag=param.get('export_clog_flag'),
                         message_level=MESSAGE_TYPE.SUCCESS_TYPE,
                         refush=False, is_alert=True)
    websocket.notify_msg(context['user_id'], notify_message, message_type=MESSAGE_TYPE.PORTAL_CLOG)
    return clog_export_url
