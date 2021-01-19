# -*- coding:utf-8 -*-
from cloud_log.rest.v_1.clog import service
from cloud_log.utils import constants


def update_clog_data(export_clog_info):
    create_time = service.get_uuid_create_time(export_clog_info['clog_uuid'])
    clog = service.get_clog(export_clog_info['clog_uuid'], create_time)
    update_data = export_clog_info['update_data']
    status = update_data.get('status')
    result_data = update_data.get('result_data')
    if not result_data and clog:
        if status == "SUCCESS":
            clog.result_data = update_data['result_data']
        else:
            clog.result_data = '导出失败'
    clog_keys = ['uuid'] + constants.clog_filter_keys
    for k in clog_keys:
        if k in update_data:
            setattr(clog, k, update_data.get(k))
    clog.save()


def update_clog_status(clog_uuid, is_success=True, result_data=None):
    status = "SUCCESS" if is_success else "ERROR"
    export_clog_info = {
        "clog_uuid": clog_uuid,
        "update_data": {
            'status': status,
            'result_data': result_data
        }
    }
    update_clog_data(export_clog_info)
