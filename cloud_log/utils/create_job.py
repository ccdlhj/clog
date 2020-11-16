# -*- coding: utf-8 -*-
from oslo_utils import uuidutils


def create_context(request, res_org_id=None, cloud_env_id=None, users=None, username=None,
                   request_id=None, user_id=None, user_info=None, message_type=None):
    user = request.user

    if not res_org_id:
        if user.res_org_info.get('type') != 'sys':
            res_org_id = user.res_org_id
    user_info = user_info or request.data.get('user_info')
    if not request_id:
        if user_info:
            request_id = user_info.get('request_id')
        else:
            request_id = 'req-' + uuidutils.generate_uuid()
    username = username if not users else users.get("user_name")
    user_id = users.get('id') if users else user_id
    context = {
        'username': user.user.get('user_name') if not username else username,
        'res_org_id': res_org_id,
        'user_id': user_id if user_id else user.get('user').get('id'),
        'cloud_env_id': str(request.META.get('HTTP_CMP_CURRENT_CLOUD_ENV')) if not cloud_env_id else cloud_env_id,
        'type': request.user.res_org_info.get('type'),
        'request': request,
        'user_info': user_info or {"create_clog": True},
        'request_id': 'req-' + uuidutils.generate_uuid() if not request_id else request_id,
        'message_type': message_type if message_type else None,
    }
    return context


def generate_task(context, task_name, params, depends_on=None, timeout=300, related_obj=None):
    if depends_on is None:
        depends_on = []

    return {
        'uuid': uuidutils.generate_uuid(),
        'name': task_name,
        'obj_id': context.get('obj_id'),
        'obj_type': context.get('obj_type', 'storage'),
        'depends_on': depends_on,
        'related_obj': related_obj,
        'context': {'request_id': context['request_id'],
                    'username': context['username'],
                    'res_org_id': context['res_org_id'],
                    'user_id': context['user_id'],
                    'cloud_env_id': context['cloud_env_id'],
                    'clog_uuid': context.get('clog_uuid'),
                    'user_info': context.get('user_info'),
                    'timeout': timeout,
                    'message_type': context['message_type'] if context['message_type'] else None},
        'param': params
    }
