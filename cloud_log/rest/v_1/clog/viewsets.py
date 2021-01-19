#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json

import datetime

from django.db.models import Q
from itertools import chain
from django.db import ProgrammingError
from django.utils.translation import ugettext_lazy as _

from uuid import uuid1

from cloud_log.exceptions import InternalServerError
from cloud_log.rest.v_1.clog import service
from cloud_log.utils.security import SecurityClient
from portal_rest import router
from portal_rest import mixins
from portal_rest import action
from portal_rest import ServiceBaseViewSet
from portal_rest.exceptions import ValidationError

from cloud_log.models import Clog
from cloud_log.rest.v_1.clog.schema import ClogListSchema
from cloud_log.rest.v_1.clog.schema import BulkClogSpawnSchema
from cloud_log.rest.v_1.clog.schema import ClogSpawnSchema
from cloud_log.rest.v_1.clog.schema import ClogUpdateSchema
from cloud_log.rest.v_1.clog.schema import ClogDumSchema
from cloud_log.utils.common import RES_ORG_TYPE
from cloud_log.utils.common import CLOG_STATUS_RUNNING
from cloud_log.utils.common import get_res_org_uuid_list
from cloud_log.utils.constants import SYS_CLOG_OPERATION_IDS, clog_filter_keys
from cloud_log.utils.create_model import get_model, generate_clog_table_name_by_datetime, generate_all_clog_table_name

clog_keys = ['uuid'] + clog_filter_keys


def parese_execption(result, http_status):
    if 300 < http_status < 500:
        raise ValidationError(result.get('message'))
    elif http_status >= 500:
        raise InternalServerError(message=result.get('message'),
                                  status_code=http_status)


def parse_clog_data(data):
    clog = {
        'uuid': data.get('uuid') or uuid1(),
        'request_id': data.get('request_id'),
        'object_uuid': data.get('object_uuid'),
        'object_name': data.get('object_name'),
        'object_type': data.get('object_type'),
        'res_org_id': data.get('res_org_id'),
        'res_org_name': data.get('res_org_name'),
        'res_org_id_path': data.get('res_org_id_path'),
        'res_org_path': data.get('res_org_path'),
        'user_id': data.get('user_id'),
        'user_name': data.get('user_name'),
        'ip_address': data.get('ip_address'),
        'operation_id': data.get('operation_id'),
        'operation_name': data.get('operation_name'),
        'status': data.get('status'),
        'created_at': data.get('created_at'),
        'origin_data': data.get('origin_data'),
        'expected_data': data.get('expected_data'),
        'result_data': data.get('result_data'),
        'extra': data.get('extra'),
        'sync_type': data.get('sync_type'),
        'related_resources': data.get('related_resources'),
        'cloud_env_id': data.get('cloud_env_id'),
    }
    return clog


@router()
class ClogViewset(ServiceBaseViewSet,
                  mixins.SpawnResourceMixin, ):
    schema_class = ClogSpawnSchema
    dump_schema_class = ClogSpawnSchema
    bulk_record_migration_schema_class = BulkClogSpawnSchema

    _atomic_functions = ()

    def perform_spawn(self, data, ids=None, query_params=None):
        """创建日志"""
        clog_data = parse_clog_data(data)
        clog_name = generate_clog_table_name_by_datetime(data['created_at'])
        try:
            clog_data['status'] = clog_data['status'] or CLOG_STATUS_RUNNING
            return get_model(clog_name, Clog).objects.create(**clog_data)
        except ProgrammingError:
            # generate sql table
            clog_model = get_model(clog_name, Clog)
            clog_model.create_table()
            clog_model.objects.create(**clog_data)
        except Exception as exc:
            msg = _("DB operation failed {message}").format(message=exc.message)
            raise ValidationError(msg)

    @action()
    def bulk_record_migration(self, data, ids, query_params):
        """同步迁移日志使用"""
        clog_data_list = data.get('clog_data_list', [])
        clog_data_map = {}
        for clog_data in clog_data_list:
            event_id_dict = clog_data['extra']
            cloud_env_id = clog_data['cloud_env_id']
            uuid = clog_data.get('uuid') or uuid1()
            clog_data.update({'uuid': uuid})
            clog_name = generate_clog_table_name_by_datetime(clog_data['created_at'])
            # TODO 查询优化，判断该日志是否被记录
            if self.clog_exist(cloud_env_id, event_id_dict, clog_name):
                continue
            if clog_name in clog_data_map:
                clog_data_map[clog_name].append(Clog(**clog_data))
            else:
                clog_data_map[clog_name] = [Clog(**clog_data)]
        for table_name, list_data in clog_data_map.iteritems():
            get_model(table_name, Clog).objects.bulk_create(list_data)
        return True

    def clog_exist(self, cloud_env_id, event_id_dict, clog_name):
        try:
            clog_model = get_model(clog_name, Clog)
            clogs = clog_model.objects.filter(cloud_env_id=cloud_env_id,
                                              extra__icontains=json.dumps(event_id_dict)[1:-1].replace(" ", "")
                                              ).first()
        except Exception:
            clogs = None
        return clogs


@router()
class ClogViewset(ServiceBaseViewSet,
                  mixins.CollectResourceMixin):
    schema_class = ClogListSchema
    dump_schema_class = ClogDumSchema

    def validate_filter_values(self, values):
        if not isinstance(values, list):
            msg = _('Invalid Filter operations {operations}').format(
                operations=str(values))
            raise ValidationError(msg)

    def validate_filter_key(self, filter_key):
        for k in clog_filter_keys:
            if filter_key.startswith(k):
                return True
        return False

    def parse_values(self, operation, value_type):
        if operation and operation.get('values'):
            if isinstance(operation.get('values'), value_type):
                return operation.get('values')

            msg = _('Invalid values {values}, '
                    'required type is {value_type}').format(
                    values=str(operation.get('values')), value_type=value_type)
            raise ValidationError(msg)

    def build_res_org_query(self, query, res_org_uuids=None):
        if self.request.user.res_org_info['type'] == RES_ORG_TYPE.SYS:
            return query
        res_org_uuids = res_org_uuids or get_res_org_uuid_list(self.request,
                                                               current=True)
        query &= Q(res_org_id__in=res_org_uuids)
        query &= ~Q(operation_id__in=SYS_CLOG_OPERATION_IDS)
        return query

    def build_filter_query(self, query, filters):
        # filters: [
        #               {"Names": "name__in", "Values": ["1", "2", "3"]},
        #               {"Names": "name__contains", "Values": ["a", "b", "c"]}
        #           ]
        if not filters:
            return query

        for i in filters:
            query_filter = Q()
            k = i.get('Name')
            values = i.get('Values')
            if not k or not values:
                continue
            self.validate_filter_values(values)
            if not isinstance(k, (str, unicode)) or not self.validate_filter_key(k):
                continue

            for value in values:
                query_filter |= Q(**{k: value})

            query &= query_filter
        return query

    def build_order_by(self, sorting):
        order_bys = []
        if sorting:
            key = sorting['key']
            order = sorting['order']
            if order == 'asc':
                oder_by = key
            else:
                oder_by = '-' + key
            order_bys.append(oder_by)
        else:
            order_bys = ['-created_at']
        return order_bys

    def build_date_query(self, query, data):
        query_args = {}
        if data.get('startTime'):
            query_args['created_at__gt'] = data.get('startTime')
        if data.get('endTime'):
            query_args['created_at__lte'] = data.get('endTime')
        if data.get('related_resources'):
            query_args['related_resources__contains'] = data.get('related_resources')
        if query_args:
            query &= Q(**query_args)
        return query

    def build_collect_query(self, data):
        query = self.build_res_org_query(Q())
        query = self.build_filter_query(query, data.get('Filters'))
        query = self.build_date_query(query, data)
        return query

    def clog_collect(self, data, limit=None, offset=None):
        query = self.build_collect_query(data)
        security = SecurityClient()
        http_success, result, http_status = security.show()
        if not http_success:
            parese_execption(result, http_status)
        security_data = result.get('data')
        clog_keep_time = security_data.get('clog_keep_time')
        start_time, end_time = service.get_limit_time(data, clog_keep_time)
        if not start_time and not end_time:
            return [], 0
        # get clog table
        total_clogs = []
        clog_total_count = 0
        clog_table_name_sorting = service.get_clog_model_name_order_mode(sorting=data.get('Sorting'))
        clog_names = generate_all_clog_table_name(start_time, end_time, clog_table_name_sorting)
        order_by = self.build_order_by(data.get('Sorting'))

        # 获取日志数据
        for clog_name in clog_names:
            clog_model = get_model(clog_name, Clog)
            clogs = service.get_clogs(clog_model, query=query)
            try:
                clog_datas_num = clogs.count()
            except Exception as e:
                continue
            clogs = clogs.order_by(*order_by)
            if limit:
                initial_limit = limit
                if clog_datas_num <= offset:
                    offset -= clog_datas_num
                else:
                    if clog_datas_num >= offset + limit:
                        clog_split_count = limit
                    else:
                        clog_split_count = clog_datas_num - offset
                    clog_split = clogs[offset: offset + limit]
                    total_clogs.append(clog_split)
                    clog_total_count += clog_split_count
                    offset -= clog_split_count
                    limit -= clog_total_count
                if clog_total_count == initial_limit:
                    break
            else:
                clog_total_count += clog_datas_num
                total_clogs = chain(total_clogs, clogs)
        return total_clogs, clog_total_count

    def perform_collect(self, data, ids=None, query_params=None):
        clogs, clog_total_count = self.clog_collect(data)
        try:
            return clogs
        except BaseException:
            return []

    def perform_paged_collect(self, data, ids=None, query_params=None,
                              limit=None, offset=None):
        clogs, clog_total_count = self.clog_collect(data, limit=limit, offset=offset)
        clog_datas = []
        for clog in clogs:
            clog_datas = chain(clog_datas, clog)
        try:
            return clog_datas
        except BaseException:
            return []

    def perform_count(self, data, ids=None, query_params=None):
        clogs, clog_total_count = self.clog_collect(data)
        try:
            return clog_total_count
        except BaseException:
            return 0


@router(parent=ClogViewset)
class ClogSpcViewset(ServiceBaseViewSet,
                     mixins.ShowResourceMixin,
                     mixins.ModifyResourceMixin):
    modify_schema_class = ClogUpdateSchema
    dump_schema_class = ClogDumSchema

    def perform_show(self, ids=None, query_params=None):
        """日志详情"""
        clog_uuid = ids['uuid']
        # get uuid create time
        create_time = service.get_uuid_create_time(clog_uuid)
        return service.get_clog(clog_uuid, create_time)

    def perform_modify(self, data, ids=None, query_params=None):
        """更新日志"""
        try:
            clog_uuid = ids['uuid']
            create_time = service.get_uuid_create_time(clog_uuid)
            clog = service.get_clog(clog_uuid, create_time)

            for k in clog_keys:
                if k in data:
                    setattr(clog, k, data.get(k))
            clog.save()
            return clog
        except Exception as exc:
            msg = _("DB operation failed {message}").format(message=exc.message)
            raise ValidationError(msg)
