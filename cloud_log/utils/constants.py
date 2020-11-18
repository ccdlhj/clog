# -*- coding:utf-8 -*-
from django.conf import settings
from portal_core.utils import enum

CLOG_SAVE_LOWER_MONTH = getattr(settings, 'CLOG_SAVE_LOWER_MONTH', 6)
CLOG_SAVE_UPPER_MONTH = getattr(settings, 'CLOG_SAVE_UPPER_MONTH', 24)

CLOG_CSV_PATH = getattr(settings, 'CLOG_CSV_PATH', '/tmp/')

CLOG_PAGE_SIZE = getattr(settings, 'CLOG_PAGE_SIZE', 2000000)

NFS_CLOG_PATH = getattr(settings, 'NFS_PATH', '/NFS/CLOG/')

NFS_CLOG_NGINX_PORT = getattr(settings, 'NFS_CLOG_NGINX_PORT', 9999)

MESSAGE_TYPE = enum(
    PORTAL_CLOG='portal_clog',
    ERROR_TYPE='danger',
    SUCCESS_TYPE='success',
)

RETRY_PARAMS = enum(
    TASK_MAX_RETRIES=getattr(settings, 'TASK_MAX_RETRIES', 5) or settings.MAX_RETRIES,
    TASK_INTERVAL=getattr(settings, 'TASK_INTERVAL', 2) or settings.INTERVAL,
    JOB_MAX_RETRIES=getattr(settings, 'JOB_MAX_RETRIES', 5) or settings.MAX_RETRIES,
    JOB_INTERVAL=getattr(settings, 'JOB_INTERVAL', 2) or settings.INTERVAL,
)

TASK_STATUS = enum(
    START="START",
    RUNNING="RUNNING",
    SUCCESS="SUCCESS",
    ERROR="ERROR",
    TIMEOUT="TIMEOUT",
    CLOG_STATUS_ERROR=getattr(settings, 'CLOG_STATUS_ERROR', "ERROR"),
)

PROCESS = enum(
    START="START",
    RUNNING="RUNNING",
    SUCCESS="SUCCESS",
)

CLOG_ACTIONS = enum(
    EXPORT='EXPORT'
)

HEADERS = {'Content-Type': 'application/json'}

