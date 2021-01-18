# -*- coding: utf-8 -*-
from cloud_log.rest.v_1.clog import schema, template
from cloud_log.rest.v_1.clog.viewsets import ClogViewset
from cloud_log.utils.constants import MESSAGE_TYPE
from cloud_log.utils.create_job import create_context
from portal_rest import router
from portal_rest import action


@router()
class ClogOperationViewSet(ClogViewset):
    generate_export_clog_task_schema_class = schema.GenerateExportClogTaskSchema
    generate_export_clog_task_dump_schema_class = schema.GenerateExportClogTaskDumpSchema

    @action()
    def generate_export_clog_task(self, data, ids=None, query_params=None):
        start_time = data.get('startTime')
        end_time = data.get('endTime')
        filters = data.get('filters')
        sorting = data.get('sorting')
        export_clog_flag = data.get('export_clog_flag')
        export_clog_log_infos = data.get('log_infos')
        context = create_context(self.request, message_type=MESSAGE_TYPE.PORTAL_CLOG)
        # generate export clog task
        export_clog_task = template.generate_export_clog_task(context, start_time,
                                                       end_time, export_clog_flag, sorting=sorting, filters=filters,
                                                       export_clog_log_infos=export_clog_log_infos)

        return export_clog_task
