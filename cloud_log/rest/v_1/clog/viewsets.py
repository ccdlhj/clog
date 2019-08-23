# -*- coding: utf-8 -*-
import copy

from t2cloud_rest import BaseViewSet, action
from t2cloud_rest import router
from t2cloud_rest import mixins
from cloud_log.models import ClogDBM
from cloud_log.rest.v_1.clog.schema import ClogSchema
from t2cloud_rest.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from cloud_log.rest.v_1.clog import service


@router()
class ClogViewset(BaseViewSet,
                  mixins.CollectResourceMixin,
                  mixins.SpawnResourceMixin, ):
    schema_class = ClogSchema
    dump_schema_class = ClogSchema

    def perform_spawn(self, data, ids=None, query_params=None):
        """创建日志"""
        return ClogDBM.objects.create(**data)

    @action()
    def get_list(self, data, ids=None, query_params=None):
        search_data = copy.deepcopy(data)
        sort = search_data.pop("sort", [])
        paged = search_data.pop('Paged', False)
        limit = search_data.pop('Limit', 0)
        offset = search_data.pop('Offset', 0)
        params = service.build_clog_query(search_data)
        clogs = ClogDBM.objects.filter(**params)
        if sort:
            clogs = clogs.order_by(*sort)
        if paged:
            return clogs[offset:offset + limit]
        return clogs

    @action()
    def get_list_count(self, data, ids=None, query_params=None):
        """日志总数"""
        search_data = copy.deepcopy(data)
        params = service.build_clog_query(search_data)
        clogs_count = ClogDBM.objects.filter(**params).count()
        return {'total': clogs_count}


@router(prefix='conditionList')
class ConditionListViewset(BaseViewSet,
                           mixins.CollectResourceMixin,
                           ):
    schema_class = ClogSchema
    dump_schema_class = ClogSchema

    @action()
    def get_list(self, data, ids=None, query_params=None):
        search_data = copy.deepcopy(data)
        filters = {}
        filter_keys_list = search_data.pop('filter_keys_list', [])
        filter_value_list = search_data.pop('filter_values_list', [])
        for i in range(len(filter_keys_list)):
            filter_key = filter_keys_list[i] + "__in"
            filters[filter_key] = filter_value_list[i]
        sort = search_data.pop("sort", [])
        paged = search_data.pop('Paged', False)
        limit = search_data.pop('Limit', 0)
        offset = search_data.pop('Offset', 0)
        params = service.build_clog_query(search_data)
        params.update(filters)
        clogs = ClogDBM.objects.filter(**params)
        if sort:
            clogs = clogs.order_by(*sort)
        if paged:
            return list(clogs[offset:offset + limit])
        return list(clogs)

    @action()
    def get_list_count(self, data, ids=None, query_params=None):
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
        return {'total': clogs_count}


@router(parent=ClogViewset)
class ClogSpcViewset(BaseViewSet,
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
        try:
            clog_id = ids['uuid']
            ClogDBM.objects.filter(id=clog_id).update(**data)
            return True
        except:
            return False