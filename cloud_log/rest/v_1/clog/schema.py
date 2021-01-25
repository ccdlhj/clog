# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from portal_rest.schema import PortalSchema, fields
from cloud_log.utils.validate import validate_clog_status
from cloud_log.utils.validate import validate_request_id


class FiltersSchema(PortalSchema):
    Name = fields.String(load_only=True, help_text=_("Name"))
    Values = fields.List(fields.String, load_only=True, help_text=_("Values"))


class SortFiltersSchema(PortalSchema):
    """包含排序与过滤条件"""
    Sorting = fields.Dict(load_only=True, help_text=_("Sorting"))
    Filters = fields.Nested(FiltersSchema, many=True, load_only=True,
                            help_text=_("Filters"))


class ClogSchema(PortalSchema):
    request_id = fields.String(validate=validate_request_id,
                               help_text=_("Request ID"))
    object_uuid = fields.String(help_text=_("Object UUID"))
    object_name = fields.String(max_len=255, help_text=_("Object Name"))
    object_type = fields.String(help_text=_("Object Type"))
    res_org_id = fields.UUID(help_text=_("Res Org ID"))
    res_org_name = fields.String(max_len=64, help_text=_("Res Org Name"))
    res_org_id_path = fields.String(max_len=1024,
                                    help_text=_("Res Org ID Path"))
    res_org_path = fields.String(max_len=1024, help_text=_("Res Org Name Path"))
    user_id = fields.Integer(help_text=_("User ID"))
    user_name = fields.String(max_len=64, help_text=_("User Name"))
    ip_address = fields.IPAddress(allow_none=True, help_text=_("Ip Address"))
    operation_id = fields.Integer(help_text=_("Operation ID"))
    operation_name = fields.String(max_len=255, help_text=_("Operation Name"))
    status = fields.String(validate=validate_clog_status,
                           help_text=_("Clog Status"))
    created_at = fields.DateTime(allow_none=True, help_text=_("Create Time"))
    updated_at = fields.DateTime(allow_none=True, help_text=_("Update Time"))
    origin_data = fields.Dict(allow_none=True, help_text=_("Origin Data"))
    expected_data = fields.Dict(allow_none=True, help_text=_("Expected Data"))
    result_data = fields.Dict(allow_none=True, help_text=_("Result Data"))
    extra = fields.Dict(allow_none=True, help_text=_("Extra"))
    sync_type = fields.String(max_len=255, help_text=_("Sync Type"))
    related_resources = fields.String(max_len=-1, allow_none=True, help_text=_("Related Resources"))
    cloud_env_id = fields.UUID(help_text=_("Cloud Env ID"))


class ClogSpawnSchema(ClogSchema):
    uuid = fields.UUID(allow_none=True, help_text=_('Clog UUID'))


class BulkClogSpawnSchema(PortalSchema):
    clog_data_list = fields.Nested("ClogSchema", many=True, load_only=True, help_text=_('Clog Data List'))


class ClogUpdateSchema(ClogSchema):
    uuid = fields.UUID(allow_none=True, dump_only=True,
                       help_text=_('Clog UUID'))


class ClogListSchema(SortFiltersSchema):
    startTime = fields.DateTime(load_only=True,
                                help_text=_("Operate StartDate"))
    endTime = fields.DateTime(load_only=True, help_text=_("Operate EndDate"))
    cloud_env_id = fields.UUID(help_text=_("Cloud Env ID"))
    Paged = fields.Bool(load_only=True, help_text=_("Paged"))
    Limit = fields.Integer(load_only=True, help_text=_("Limit"))
    Offset = fields.Integer(load_only=True, help_text=_("Offset"))
    related_resources = fields.String(load_only=True, help_text=_("related_resources"))


class ClogDumSchema(ClogSchema):
    uuid = fields.UUID(dump_only=True, help_text=_('Clog UUID'))


class GenerateExportClogTaskSchema(PortalSchema):
    export_clog_log_start_time = fields.String(help_text=_("Export Clog Log Start Time"))
    export_clog_log_end_time = fields.String(help_text=_("Export Clog Log End Time"))
    startTime = fields.String(help_text=_("Start Time"))
    endTime = fields.String(help_text=_("End Time"))
    export_clog_flag = fields.String(help_text=_("Export Clog Flag"))
    log_infos = fields.List(fields.Dict(), help_text=_("Log Infos"))
    filters = fields.List(fields.Dict(), load_only=True, help_text=_("Filters"))

class GenerateExportClogTaskDumpSchema(PortalSchema):
    uuid = fields.UUID(dump_only=True, help_text=_("Task UUID"))
    name = fields.String(dump_only=True, help_text=_("Task Name"))
    context = fields.Dict(dump_only=True, help_text=_("Context"))
    depends_on = fields.List(fields.String, allow_none=True,
                             help_text=_("Depends On"))
    param = fields.Dict(fields.String, help_text="Param")
    export_clog_log_start_time = fields.String(help_text=_("Export Clog Log Start Time"))
    export_clog_log_end_time = fields.String(help_text=_("Export Clog Log End Time"))
    startTime = fields.String(help_text=_("Start Time"))
    endTime = fields.String(help_text=_("End Time"))
    Filters = fields.Nested(FiltersSchema, many=True, load_only=True,
                            help_text=_("Filters"))
    export_clog_log_infos = fields.List(fields.Dict(), help_text=_("Export Clog Log Infos"))
    export_clog_flag = fields.String(help_text=_("Export Clog Flag"))
    obj_type = fields.String(dump_only=True, help_text=_("Obj Type"))
    obj_id = fields.UUID(dump_only=True, help_text=_("Obj UUID"))
    related_obj = fields.String(dump_only=True, help_text=_("Related Obj"))