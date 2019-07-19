# -*- coding: utf-8 -*-
from t2cloud_rest.schema import PortalSchema, fields
from django.utils.translation import ugettext_lazy as _


class ClogSchema(PortalSchema):
    id = fields.Integer(dump_only=True, help_text=_("ID"))
    object_name = fields.String(help_text=_("Object Name"))
    object_id = fields.String(help_text=_("Object ID"))
    object_type = fields.String(help_text=_("Object Type"))
    operation_name = fields.String(help_text=_("Operation Name"))
    operation_code = fields.String(help_text=_("Operation Code"))
    status = fields.String(help_text=_("Status"))
    user_name = fields.String(help_text=_("User Name"))
    user_id = fields.String(help_text=_("User ID"))
    res_org_name = fields.String(help_text=_("Res Org Name"))
    res_org_id = fields.String(help_text=_("Res Org ID"))
    ip_address = fields.String(help_text=_("Ip Address"))
    created_at = fields.DateTime(help_text=_("Create Time"))
    updated_at = fields.DateTime(help_text=_("Update Time"))
    origin_data = fields.Dict(help_text=_("Origin Data"))
    update_data = fields.Dict(help_text=_("Update Data"))
    log_level = fields.String(help_text=_("Log Level"))
    start = fields.DateTime(help_text=_("Operate StartDate"))
    end = fields.DateTime(help_text=_("Operate EndDate"))
    extra = fields.String(help_text=_("Extra"))
    filter_keys_list = fields.List(fields.String, help_text=_("Filter Keys List"))
    filter_values_list = fields.List(fields.List(fields.String), help_text=_("Filter Values List"))
