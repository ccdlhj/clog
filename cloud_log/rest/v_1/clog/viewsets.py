# -*- coding: utf-8 -*-
import copy

from t2cloud_rest import NoAuthViewSet
from t2cloud_rest import router
from t2cloud_rest import mixins
from cloud_log.models import ClogDBM
from cloud_log.rest.v_1.clog.schema import ClogSchema
from t2cloud_rest.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from cloud_log.rest.v_1.clog import service


@router()
class ClogViewset(NoAuthViewSet,
                  mixins.CollectResourceMixin,
                  mixins.SpawnResourceMixin, ):
    schema_class = ClogSchema
    dump_schema_class = ClogSchema

    def perform_spawn(self, data, ids=None, query_params=None):
        """创建日志"""
        return ClogDBM.objects.create(**data)

    def perform_count(self, data, ids=None, query_params=None):
        """日志总数"""
        search_data = copy.deepcopy(data)
        params = service.build_clog_query(search_data)
        clogs = ClogDBM.objects.filter(**params)
        return clogs.count()

    def perform_paged_collect(self, data, ids=None, query_params=None, limit=None, offset=None):
        """分页查询"""
        search_data = copy.deepcopy(data)
        params = service.build_clog_query(search_data)
        clogs = ClogDBM.objects.filter(**params)
        return clogs[offset:offset + limit]


@router(prefix='conditionList')
class ConditionListViewset(NoAuthViewSet,
                           mixins.CollectResourceMixin,
                           ):
    schema_class = ClogSchema
    dump_schema_class = ClogSchema

    def perform_count(self, data, ids=None, query_params=None):
        """查询数目"""
        search_data = copy.deepcopy(data)
        filters = {}
        filter_keys_list = search_data.pop('filter_keys_list', [])
        filter_value_list = search_data.pop('filter_values_list', [])
        for i in range(len(filter_keys_list)):
            filter_key = filter_keys_list[i] + "__in"
            filters[filter_key] = filter_value_list[i]
        params = service.build_clog_query(search_data)
        params.update(filters)
        clogs_count = ClogDBM.objects.filter(**params).count()
        return clogs_count

    def perform_paged_collect(self, data, ids=None, query_params=None, limit=None, offset=None):
        """通过字段列表过滤
        format: {'filter_keys': ['res_org_id', 'user_id'], 'filter_values': [['1', '2', '3'],['4', '5', '6']]}
        """
        search_data = copy.deepcopy(data)
        filters = {}
        filter_keys_list = search_data.pop('filter_keys_list', [])
        filter_value_list = search_data.pop('filter_values_list', [])
        for i in range(len(filter_keys_list)):
            filter_key = filter_keys_list[i] + "__in"
            filters[filter_key] = filter_value_list[i]
        params = service.build_clog_query(search_data)
        params.update(filters)
        clogs = ClogDBM.objects.filter(**params)
        clogs = clogs[offset:offset + limit]
        return clogs


@router(parent=ClogViewset)
class ClogSpcViewset(NoAuthViewSet,
                     mixins.ShowResourceMixin,
                     mixins.ModifyResourceMixin
                     ):
    schema_class = ClogSchema
    dump_schema_class = ClogSchema

    def perform_show(self, ids=None, query_params=None):
        """日志详情"""
        clog_id = ids['uuid']
        try:
            clog = ClogDBM.objects.get(id=clog_id)
        except:
            raise ValidationError(_('Not found the clog data'))
        return clog

    def perform_modify(self, data, ids=None, query_params=None):
        """修改"""
        clog_id = ids['uuid']
        ClogDBM.objects.filter(id=clog_id).update(**data)
        return True
