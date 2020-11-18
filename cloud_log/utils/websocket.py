# -*- coding: utf-8 -*-
import copy
from portal_common.utils.notify import notify_websocket
from portal_common.utils.notify import NOTIFY_PAYLOAD

from cloud_log.utils.constants import MESSAGE_TYPE


def generate_msg(**notify_kwargs):
    notify_msg = copy.deepcopy(NOTIFY_PAYLOAD)
    for k in notify_kwargs:
        notify_msg[k] = notify_kwargs[k]
    return notify_msg


def notify_msg(user_id, notify_data, message_type=None):
    notify_websocket(message_type=message_type, data=notify_data, user_id=user_id)


def update_msg(ws_params, **kwargs):
    # This is mainly for update_task_info
    for k in kwargs.keys():
        ws_params[k] = kwargs.get(k)
