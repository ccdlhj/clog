# -*- coding: utf-8 -*-
from cloud_log.rest.v_1.clog import schema, template
from cloud_log.rest.v_1.clog.viewsets import ClogViewset
from cloud_log.utils.constants import MESSAGE_TYPE
from cloud_log.utils.create_job import create_context
from cloud_log.utils.common import get_res_org_uuid_list

from portal_rest import router
from portal_rest import action


@router()
class ClogOperationViewSet(ClogViewset):
    generate_export_clog_task_schema_class = schema.GenerateExportClogTaskSchema
    generate_export_clog_task_dump_schema_class = schema.GenerateExportClogTaskDumpSchema

    @action()
    def generate_export_clog_task(self, data, ids=None, query_params=None):
        res_org_id = data.get('res_org_id')
        res_org_type = data.get('res_org_type')
        res_org_uuids = data.get('res_org_uuids')
        start_time = data.get('startTime')
        end_time = data.get('endTime')
        filters = data.get('filters')
        sorting = data.get('sorting')
        export_clog_log_start_time = data.get('export_clog_log_start_time')
        export_clog_log_end_time = data.get('export_clog_log_end_time')
        export_clog_flag = data.get('export_clog_flag')
        export_clog_log_infos = data.get('log_infos')
        context = create_context(self.request, message_type=MESSAGE_TYPE.PORTAL_CLOG)
        # generate export clog task
        export_clog_task = template.generate_export_clog_task(context, res_org_id,
                                                              start_time,
                                                              end_time, export_clog_flag,
                                                              sorting=sorting, filters=filters,
                                                              export_clog_log_infos=export_clog_log_infos,
                                                              export_clog_log_start_time=export_clog_log_start_time,
                                                              export_clog_log_end_time=export_clog_log_end_time,
                                                              res_org_type=res_org_type,
                                                              res_org_uuids=res_org_uuids)

        return export_clog_task
