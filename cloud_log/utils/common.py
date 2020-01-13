# -*- coding: utf-8 -*

import copy

from django.utils.translation import ugettext_lazy as _

from t2cloud.utils import enum
from cloud_log.exceptions import InternalServerError

# 组织资源几种类型
RES_ORG_TYPE = enum(
    # VDC类型
    VDC='vdc',
    # 平台侧类型
    SYS='sys',
    # 项目类型
    PROJECT='project'
)

CLOG_STATUS_RUNNING = 'RUNNING'
CLOG_STATUS_SUCCESS = 'SUCCESS'
CLOG_STATUS_ERROR = 'ERROR'

CLOG_STATUS = [CLOG_STATUS_RUNNING, CLOG_STATUS_SUCCESS, CLOG_STATUS_ERROR]


def get_res_org_tree(request):
    try:
        return request.user.res_org_tree
    except Exception as exc:
        return {}


def get_res_org_list(request, current=False):
    try:
        res_org_tree = request.user.res_org_tree
        if current:
            current_res_org_id = request.user.res_org_id
            res_org_list = copy.deepcopy(res_org_tree)
        else:
            res_org_list = []

        children = copy.deepcopy(res_org_tree)
        while children:
            new_children_list = []
            for child in children:
                if current and current_res_org_id == child['uuid']:
                    res_org_list = [child]
                    new_children_list = child.get('children')
                    break

                res_org_list.append(child)
                new_children = child.get('children')
                if new_children:
                    new_children_list.extend(new_children)
            children = new_children_list

        return res_org_list
    except Exception as exc:
        msg = _('Invalid request user res_org_tree')
        raise InternalServerError(msg)


def get_res_org_uuid_list(request, current=False):
    res_org_list = get_res_org_list(request, current=current)
    return [res_org['uuid'] for res_org in res_org_list]
