# -*- coding: utf-8 -*-
from django.conf import settings

from t2cloud.utils import enum  # noqa


DEFAULT_PORTAL_PA = \
    {'private_key': '82902c35315686baa7f7bc19db4fe5f08e0ab5225787aacb67d78a41d892527d',
     'public_key': '04ef39f3391c2d3aeaab6381c176af6edcb48b86cc6e001771eb08009fe4a81937a6cd355604c645e1a4e26b7c00d9269741ff8da25dfa0fa443c7d33df566d02c'}
PORTAL_PA = getattr(settings, 'PORTAL_PA', DEFAULT_PORTAL_PA)  # 'aaaaaa'



USER_STATUS = enum(
    ACTIVE="ACTIVE",
    NOT_ACTIVED="NOT_ACTIVED",
    DISABLED="DISABLED",
    DORMANCY="DORMANCY",
    LOCKING="LOCKING",
    FROZEN="FROZEN",
)


MANAGE_STATUS = enum(
    ENABLE="ENABLE",  # 启用
    DISABLED="DISABLED",  # 禁用
)

USER_TYPE = enum(
    CLOUD_ADMIN='CLOUD_ADMIN',
    ACCOUNT_ADMIN='ACCOUNT_ADMIN',
    ACCOUNT_MEMBER='ACCOUNT_MEMBER',
)


PASSWORD_TYPE = enum(
    PERMANENT="PERMANENT",  # 永久的
    TEMPORARY="TEMPORARY",  # 临时的, 必须修改
    TIMELINESS="TIMELINESS",  # 有时效性的
)

CERTIFY_STATUS = enum(
    SUBMIT='SUBMIT',
    INVALID='INVALID',
    VERIFIED='VERIFIED',
)

ACCOUNT_STATUS = enum(
    ACTIVE="ACTIVE",  # 可用
    INVALID="INVALID",  # 作废
    EXPIRED="EXPIRED",  # 过期
    EXHAUSTED="EXHAUSTED",  # 用尽
)

