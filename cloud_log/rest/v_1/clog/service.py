# -*- coding: utf-8 -*-


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
        params[query_param_key+"__contains"] = query_params[query_param_key]
    params.update(time_query_param)
    return params
