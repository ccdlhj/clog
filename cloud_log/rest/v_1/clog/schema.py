# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from t2cloud_rest.schema import PortalSchema, fields
from cloud_log.utils.validate import validate_clog_status
from cloud_log.utils.validate import validate_request_id


class ClogSchema(PortalSchema):
    request_id = fields.String(validate=validate_request_id,
                               help_text=_("Request ID"))
    object_uuid = fields.String(help_text=_("Object UUID"))
    object_name = fields.String(max_len=64, help_text=_("Object Name"))
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
    operation_name = fields.String(help_text=_("Operation Name"))
    status = fields.String(validate=validate_clog_status,
                           help_text=_("Clog Status"))
    created_at = fields.DateTime(allow_none=True, help_text=_("Create Time"))
    updated_at = fields.DateTime(allow_none=True, help_text=_("Update Time"))
    origin_data = fields.Dict(allow_none=True, help_text=_("Origin Data"))
    expected_data = fields.Dict(allow_none=True, help_text=_("Expected Data"))
    result_data = fields.Dict(allow_none=True, help_text=_("Result Data"))
    extra = fields.Dict(allow_none=True, help_text=_("Extra"))


class ClogSpawnSchema(ClogSchema):
    uuid = fields.UUID(allow_none=True, help_text=_('Clog UUID'))


class ClogUpdateSchema(ClogSchema):
    uuid = fields.UUID(allow_none=True, dump_only=True,
                       help_text=_('Clog UUID'))


class ClogListSchema(PortalSchema):
    date_start = fields.DateTime(load_only=True,
                                 help_text=_("Operate StartDate"))
    date_end = fields.DateTime(load_only=True, help_text=_("Operate EndDate"))
    Filters = fields.Dict(allow_none=True, help_text=_("Filters"))
    Sorting = fields.List(fields.Dict, load_only=True, help_text=_("Sorting"))
    Paged = fields.Bool(load_only=True, help_text=_("Paged"))
    Limit = fields.Integer(load_only=True, help_text=_("Limit"))
    Offset = fields.Integer(load_only=True, help_text=_("Offset"))


class ClogDumSchema(ClogSchema):
    uuid = fields.UUID(dump_only=True, help_text=_('Clog UUID'))
