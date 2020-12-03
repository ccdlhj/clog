# -*- coding:utf-8 -*-
import csv
import datetime
import os
import socket
import zipfile
import shutil
from oslo_utils import uuidutils

from django.core.paginator import Paginator
from django.utils.translation import ugettext_lazy as _

from cloud_log.models.clog import Clog
from cloud_log.utils import websocket, taskinfo
from cloud_log.utils.constants import CLOG_CSV_PATH, CLOG_PAGE_SIZE, NFS_CLOG_PATH, NFS_CLOG_NGINX_PORT, MESSAGE_TYPE, \
    TASK_STATUS, PROCESS
from cloud_log.utils.create_model import generate_clog_table_name, get_model
from cloud_log.utils.taskinfo import update_task_info
from cloud_log.utils.constants import CLOG_ACTIONS


def generate_clog_csv_path(clog_name):
    path = CLOG_CSV_PATH
    clog_path = path + clog_name + uuidutils.generate_uuid() + '.csv'
    return clog_path


def generate_clog_zip_path(clog_name):
    path = CLOG_CSV_PATH
    clog_uuid = uuidutils.generate_uuid()
    zip_path = path + clog_name + clog_uuid + '.zip'
    return zip_path, clog_uuid


def generate_csv_file(clog_datas, clog_path):
    # generate csv
    with open(clog_path, 'ab+') as csvfile:
        csv_write = csv.writer(csvfile)
        csv_write.writerow(clog_datas)


def export_clog(context, param):
    task_id = context.get('task_id')
    taskinfo.create_task_log_template(task_id, '日志数据开始导出')
    update_task_info(task_id, status=TASK_STATUS.START, process_status=PROCESS.START)

    # generate clog model name
    start_time = datetime.datetime.strptime(param.get('startTime'), "%Y-%m-%d %H:%M:%S")
    clog_name = generate_clog_table_name(start_time)
    clog_model = get_model(clog_name, Clog)
    # generate path
    clog_path = generate_clog_csv_path(clog_name)
    # websocket
    message = _('Clog start exporting')
    notify_message = websocket.generate_msg(uuid=uuidutils.generate_uuid(),
                                            action=CLOG_ACTIONS.EXPORT,
                                            message_level=MESSAGE_TYPE.SUCCESS_TYPE,
                                            refush=False, is_alert=True, message=message)
    websocket.notify_msg(context['user_id'], notify_message, message_type=MESSAGE_TYPE.PORTAL_CLOG)
    # get clog data
    clogs = clog_model.objects.all()
    clog_paginator = Paginator(clogs, CLOG_PAGE_SIZE)
    if clog_paginator.num_pages > 1:
        for clog_page in range(clog_paginator.num_pages):
            clog_datas = clog_paginator.page(clog_page)
            # generate csv
            generate_csv_file(clog_datas, clog_path)
            del clog_datas
    else:
        generate_csv_file(clogs, clog_path)
    # generate zip
    zip_path, clog_uuid = generate_clog_zip_path(clog_name)
    clog_zip = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    clog_zip.write(clog_path)
    # delete csv
    os.remove(clog_path)
    # change zip path to nfs
    shutil.move(zip_path, NFS_CLOG_PATH)
    # generate url
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    url = 'http://' + ip + ':' + str(NFS_CLOG_NGINX_PORT) + clog_name + clog_uuid + '.zip'
    message = _('Clog was export successful')
    websocket.update_msg(notify_message, message=message,
                         exoport_url=url,
                         export_clog_flag=param.get('export_clog_flag'),
                         message_level=MESSAGE_TYPE.SUCCESS_TYPE,
                         refush=False, is_alert=True)
    websocket.notify_msg(context['user_id'], notify_message, message_type=MESSAGE_TYPE.PORTAL_CLOG)
    return url
