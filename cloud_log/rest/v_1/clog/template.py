# -*- coding: utf-8 -*-
from cloud_log.utils.create_job import generate_task


def generate_export_clog_task(context, res_org_id, start_time, end_time, export_clog_flag,
                              sorting=None, filters=None, export_clog_log_infos=None,
                              export_clog_log_start_time=None,
                              export_clog_log_end_time=None, timeout=300,
                              res_org_type=None, res_org_uuids=None):
    task_name = 'export_clog'
    params = {
        'res_org_id': res_org_id,
        'res_org_type': res_org_type,
        'res_org_uuids': res_org_uuids,
        'startTime': start_time,
        'endTime': end_time,
        'export_clog_log_start_time': export_clog_log_start_time,
        'export_clog_log_end_time': export_clog_log_end_time,
        'filters': filters,
        'Sorting': sorting,
        'export_clog_log_infos': export_clog_log_infos,
        'export_clog_flag': export_clog_flag,
    }
    export_clog_task = generate_task(context, task_name, params, timeout=timeout)
    return export_clog_task
