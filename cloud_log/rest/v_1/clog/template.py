# -*- coding: utf-8 -*-
from cloud_log.utils.create_job import generate_task


def generate_export_clog_task(context, start_time, end_time, export_clog_flag, timeout=300):
    task_name = 'export_clog'
    params = {
        'startTime': start_time,
        'endTime': end_time,
        'export_clog_flag': export_clog_flag
    }
    export_clog_task = generate_task(context, task_name, params, timeout=timeout)
    return export_clog_task
