# -*- coding: utf-8 -*-
import datetime
import re
from uuid import UUID, uuid1
from dateutil.relativedelta import relativedelta

from django.conf import settings

from cloud_log.models import Clog
from cloud_log.utils.db_utils import generate_clog_table_name_by_datetime, get_model
from portal_rest.exceptions import ValidationError

from django.utils.translation import ugettext_lazy as _
from cloud_log.utils.constants import UUID_DEFAULT_VERSION, CLOG_SAVE_UPPER_MONTH, DEFAULT_FIRST_MONTH, \
    YEAR_DECREASE_PROGRESSIVELY, DEFAULT_LAST_MONTH, MONTH_DECREASE_PROGRESSIVELY


def set_date_start_and_end_filter(query_params):
    """设置日期过滤"""
    time_query_param = {}
    start = query_params.pop("start", None)
    end = query_params.pop("end", None)
    if start and end:
        time_query_param['created_at__range'] = [start, end]
    elif start and not end:
        time_query_param['created_at__gt'] = start
    elif not start and end:
        time_query_param['created_at__lt'] = end
    return time_query_param


def build_clog_query(query_params):
    """设置查询条件"""
    time_query_param = set_date_start_and_end_filter(query_params)
    params = {}
    # 参数模糊查询
    for query_param_key in query_params:
        params[query_param_key+"__icontains"] = query_params[query_param_key]
    params.update(time_query_param)
    return params


def get_uuid_create_time(uuid):
    if UUID(uuid).version != UUID_DEFAULT_VERSION:
        return None
    clog_uuid1 = UUID('{%s}' % uuid)
    # get uuid1 create_time
    create_time = datetime.datetime.fromtimestamp((clog_uuid1.time -0x01b21dd213814000L) * 100 / 1e9)
    return create_time


def get_clogs(clog_model_name, query=None):
    try:
        if query:
            clog_datas = clog_model_name.objects.filter(query)
        else:
            clog_datas = clog_model_name.objects.all()
    except Exception:
        clog_datas = None

    return clog_datas


def get_clog_model_name_order_mode(sorting=None):
    if sorting:
        return sorting['order']
    else:
        return getattr(settings, 'clog_name_order_mode', 'desc')


def get_limit_time(data, clog_keep_time):
    now_time = datetime.datetime.now()
    default_clog_start_time = now_time - relativedelta(months=clog_keep_time)
    default_clog_end_time = datetime.datetime(now_time.year, now_time.month, now_time.day, 23, 59, 59)
    start_time = data.get('startTime')
    end_time = data.get('endTime')
    # 如果传进来的起始时间和终止时间都存在, 并且终止时间小于起始时间.
    if start_time and end_time and end_time < start_time:
        ValidationError(_('Clog collect time error'))

    # 如果传进来的起始时间存在, 并且起始时间大于默认终止时间, 或者传进来终止时间存在, 并且终止时间小于默认起始时间.
    if (start_time and start_time > default_clog_end_time) or (end_time and end_time < default_clog_start_time):
        return None, None

    # 如果传进来的起始时间存在, 并且起始时间小于默认起始时间, 或者未传起始时间.
    if (start_time and start_time < default_clog_start_time) or not start_time:
        start_time = default_clog_start_time

    # 如果传进来的终止时间存在, 并且终止时间大于默认终止时间, 或者未传终止时间.
    if (end_time and end_time > default_clog_end_time) or not end_time:
        end_time = default_clog_end_time

    return start_time, end_time


def get_now_date():
    # 获取之前安全设置时间内的时间
    now_date = datetime.datetime.now()
    year = now_date.year
    month = now_date.month
    return now_date, year, month


def validate_clog_in_all_tables(clog_uuid):
    now_date, year, month = get_now_date()
    clog_save_upper_month = CLOG_SAVE_UPPER_MONTH
    for i in range(clog_save_upper_month - 1):
        if i != 0:
            if month == DEFAULT_FIRST_MONTH:
                year -= YEAR_DECREASE_PROGRESSIVELY
                month = DEFAULT_LAST_MONTH
            else:
                month -= MONTH_DECREASE_PROGRESSIVELY
        clog_table_name = generate_clog_table_name_by_datetime(datetime.datetime(year, month, 1))
        try:
            clog = get_model(clog_table_name, Clog).objects.get(uuid=clog_uuid)
            return clog
        except Exception as e:
            continue

    return None


def get_clog(clog_uuid, create_time):
    if create_time:
        try:
            clog_table_name = generate_clog_table_name_by_datetime(create_time)
            return get_model(clog_table_name, Clog).objects.get(uuid=clog_uuid)
        except:
            msg = _('Clog {uuid} could not be found.').format(uuid=clog_uuid)
            raise ValidationError(msg)
    else:
        clog = validate_clog_in_all_tables(clog_uuid)
        if not clog:
            msg = _('Clog {uuid} could not be found.').format(uuid=clog_uuid)
            raise ValidationError(msg)
        return clog
