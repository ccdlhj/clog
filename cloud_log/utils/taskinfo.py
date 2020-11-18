import json
import time

import requests
from django.conf import settings
from oslo_log import log

from cloud_log.utils import constants
from cloud_log.utils.constants import RETRY_PARAMS
from cloud_log.utils.retrying import retry

LOG = log.getLogger(__name__)


@retry(RETRY_PARAMS.TASK_MAX_RETRIES, RETRY_PARAMS.TASK_INTERVAL)
def update_task_info(task_id, **kwargs):
    task_info_data = settings.UPDATE_TASK_INFO_PAYLOAD
    process = get_task_speed_progress(kwargs.get("process_status", 0))
    task_info_data["task-update"]["process"] = process
    task_info_data["task-update"]["output"] = kwargs.get("output")
    task_info_data["task-update"]["status"] = kwargs.get("status")
    task_info_data["task-update"]["failure_reason"] = kwargs.get("failure_reason")
    if kwargs.get("obj_type"):
        task_info_data["task-update"]["obj_type"] = kwargs.get("obj_type")
    if kwargs.get("obj_id"):
        task_info_data["task-update"]["obj_id"] = kwargs.get("obj_id")

    url = settings.TASK_UPDATE_URL.format(task_id)
    payload = json.dumps(task_info_data)
    requests.post(url, headers=constants.HEADERS, data=payload)


def get_task_speed_progress(status):
    # return str(TASK_PROCESS[status] * 10) + '%'
    return str(status * 10) + '%'


@retry(RETRY_PARAMS.TASK_MAX_RETRIES, RETRY_PARAMS.TASK_INTERVAL)
def create_task_log(task_uuid, task_info):
    url = settings.CREATE_TASK_LOG_URL
    data = {
        "task_log": {
            "info": task_info,
            "task_uuid": task_uuid
        }
    }
    requests.post(url, headers=constants.HEADERS, data=json.dumps(data))


def create_task_log_template(task_uuid, info, traceback=None):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    info = '[' + current_time + ']' + info
    if traceback:
        info = info + '/n' + traceback
    create_task_log(task_uuid, info)
