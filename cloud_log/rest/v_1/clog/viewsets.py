# -*- coding: utf-8 -*-
import copy

from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from oslo_utils.uuidutils import generate_uuid

from t2cloud_rest import action
from t2cloud_rest import router
from t2cloud_rest import mixins
from t2cloud_rest import BaseViewSet
from t2cloud_rest.exceptions import ValidationError

from cloud_log.models import Clog
from cloud_log.rest.v_1.clog.schema import ClogListSchema
from cloud_log.rest.v_1.clog.schema import ClogSpawnSchema
from cloud_log.rest.v_1.clog.schema import ClogUpdateSchema
from cloud_log.rest.v_1.clog.schema import ClogDumSchema
from cloud_log.rest.v_1.clog import service
from cloud_log.utils.common import RES_ORG_TYPE
from cloud_log.utils.common import CLOG_STATUS_RUNNING
from cloud_log.utils.common import get_res_org_uuid_list


clog_filter_keys = [
    'request_id',
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
]

clog_keys = ['uuid'] + clog_filter_keys


def parse_clog_data(data):
    clog = {
        'uuid': data.get('uuid') or generate_uuid(),
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
    }
    return clog


def get_clog(clog_uuid):
    try:
        return Clog.objects.get(uuid=clog_uuid)
    except:
        msg = _('Clog {uuid} could not be found.').format(uuid=clog_uuid)
        raise ValidationError(msg)


@router()
class ClogViewset(BaseViewSet,
                  mixins.SpawnResourceMixin, ):
    schema_class = ClogSpawnSchema
    dump_schema_class = ClogSpawnSchema

    def perform_spawn(self, data, ids=None, query_params=None):
        """创建日志"""
        clog_data = parse_clog_data(data)
        try:
            clog_data['status'] = clog_data['status'] or CLOG_STATUS_RUNNING
            return Clog.objects.create(**clog_data)
        except Exception as exc:
            msg = _("DB operation failed {message}").format(message=exc.message)
            raise ValidationError(msg)


@router()
class ClogViewset(BaseViewSet,
                  mixins.CollectResourceMixin):
    schema_class = ClogListSchema
    dump_schema_class = ClogDumSchema

    def validate_operations(self, operations):
        if not isinstance(operations, list):
            msg = _('Invalid Filter operations {operations}').format(
                operations=str(operations))
            raise ValidationError(msg)

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
        return query

    def build_filter_query(self, query, filters):
        # filters: {'user_id': [{'operator': 'in', 'values': [123]}]}
        if not filters:
            return query

        query_args = {}
        for k, operations in filters.items():
            if not operations:
                continue
            self.validate_operations(operations)
            if k not in clog_filter_keys:
                continue

            for operation in operations:
                operator = operation.get('operator')
                if 'in' == operator:
                    query_args[k+'__in'] = self.parse_values(operation, list)
                elif 'contains' == operator:
                    query_args[k+'__contains'] = \
                        self.parse_values(operation, (str, unicode,))
                elif 'icontains' == operator:
                    query_args[k+'__icontains'] = \
                        self.parse_values(operation, (str, unicode,))

        if query_args:
            query &= Q(**query_args)
        return query

    def build_order_by(self, sorting):
        order_bys = []
        if not sorting:
            return order_bys
        for s in sorting:
            key = s['key']
            if key not in clog_filter_keys:
                continue
            order = s['order']
            oder_by = key if order == 'asc' else '-' + key
            order_bys.append(oder_by)
        return order_bys

    def build_date_query(self, query, data):
        query_args = {}
        if data.get('date_start'):
            query_args['created_at__gt'] = data.get('date_start')
        if data.get('date_end'):
            query_args['created_at__lte'] = data.get('date_end')
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
        clogs = Clog.objects.filter(query)
        order_by = self.build_order_by(data.get('Sorting'))
        if order_by:
            clogs = clogs.order_by(*order_by)
        return clogs

    def perform_collect(self, data, ids=None, query_params=None):
        clogs = self.clog_collect(data)
        return clogs

    def perform_paged_collect(self, data, ids=None, query_params=None,
                              limit=None, offset=None):
        clogs = self.clog_collect(data, limit=limit, offset=offset)
        clogs = clogs[offset:offset+limit]
        return clogs

    def perform_count(self, data, ids=None, query_params=None):
        clogs = self.clog_collect(data)
        return clogs.count()


@router(parent=ClogViewset)
class ClogSpcViewset(BaseViewSet,
                     mixins.ShowResourceMixin,
                     mixins.ModifyResourceMixin):
    modify_schema_class = ClogUpdateSchema
    dump_schema_class = ClogDumSchema

    def perform_show(self, ids=None, query_params=None):
        """日志详情"""
        clog_uuid = ids['uuid']
        return get_clog(clog_uuid)

    def perform_modify(self, data, ids=None, query_params=None):
        """更新日志"""
        try:
            clog_uuid = ids['uuid']
            clog = Clog.objects.filter(uuid=clog_uuid).first()

            for k in clog_keys:
                if k in data:
                    setattr(clog, k, data.get(k))
            clog.save()
            return clog
        except Exception as exc:
            msg = _("DB operation failed {message}").format(message=exc.message)
            raise ValidationError(msg)
