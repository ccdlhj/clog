# -*- coding:utf-8 -*-
from django.conf import settings
from portal_core.utils import enum

clog_filter_keys = [
    'request_id',
    'related_resources',
    'object_uuid',
    'object_name',
    'object_type',
    'res_org_id',
    'res_org_name',
    'res_org_id_path',
    'res_org_path',
    'user_id',
    'user_name',
    'ip_address',
    'operation_id',
    'operation_name',
    'status',
    'created_at',
    'updated_at',
    'origin_data',
    'expected_data',
    'result_data',
    'extra',
    'cloud_env_id',
    'sync_type'
]

CLOG_SAVE_LOWER_MONTH = getattr(settings, 'CLOG_SAVE_LOWER_MONTH', 6)
CLOG_SAVE_UPPER_MONTH = getattr(settings, 'CLOG_SAVE_UPPER_MONTH', 24)

CLOG_CSV_PATH = getattr(settings, 'CLOG_CSV_PATH', '/tmp/')

CLOG_EXPORT_MAX_SIZE = getattr(settings, 'CLOG_PAGE_SIZE', 20000)

NFS_CLOG_PATH = getattr(settings, 'NFS_PATH', '/nfs/clog/')

NFS_CLOG_NGINX_PORT = getattr(settings, 'NFS_CLOG_NGINX_PORT', 15657)

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

# 平台侧clog行为id
SYS_CLOG_OPERATION_IDS = [700, 701, 702, 703]

# 选择uuid版本
UUID_DEFAULT_VERSION = getattr(settings, 'UUID_DEFAULT_VERSION', 1)

# 递减月数
MONTH_DECREASE_PROGRESSIVELY = getattr(settings, 'MONTH_DECREASE_PROGRESSIVELY', 1)
# 递减年数
YEAR_DECREASE_PROGRESSIVELY = getattr(settings, 'YEAR_DECREASE_PROGRESSIVELY', 1)

# 初始月份
DEFAULT_FIRST_MONTH = 1
# 终止月份
DEFAULT_LAST_MONTH = 12

CSV_TITLE_CN = ['操作请求ID', '对象ID', '对象', '对象类型', '项目', '操作人', '操作人ID', '访问IP', '任务类型ID', '任务', '状态',
                '操作时间', '更新时间', '原始数据', '预期数据', '结果数据']

FILTER_NAME_CN = {
    'REQUEST_ID': '操作请求ID',
    'OBJECT_NAME': '对象',
    'OBJECT_UUID': '对象ID',
    'OPERATION_NAME': '任务',
    'USER_NAME': '操作人',
    'USER_ID': '操作人ID',
    'RES_ORG_PATH': '项目',
    'IP_ADDRESS': '访问IP',
    'STATUS': '状态',
    'OPERATION_ID':'任务类型ID'
}

# 文件大小进制转换
FILE_BINARY_SIZE = enum(
    B = 1,
    KB = 1024,
    MB = 1048576,
    GB = 1073741824,
    TB = 1099511627776
)
