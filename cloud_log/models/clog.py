# -*- coding: utf-8 -*-
from django.db import models
import jsonfield

class ClogDBM(models.Model):
    '''日志表'''

    id = models.AutoField(primary_key=True)
    object_name = models.CharField(max_length=255, null=True, help_text='对象名称')
    object_id = models.CharField(max_length=32, null=True, help_text='对象ID')
    object_type = models.CharField(max_length=255, null=True, help_text='对象类型')
    operation_name = models.CharField(max_length=255, null=True, help_text='操作任务名称')
    operation_code = models.CharField(max_length=32, null=True, help_text='操作任务编码')
    status = models.CharField(max_length=64, null=True, help_text='状态')
    user_name = models.CharField(max_length=255, null=True, help_text='用户名称')
    user_id = models.CharField(max_length=32, null=True, help_text='用户ID')
    res_org_name = models.CharField(max_length=255, null=True, help_text='资源组织名称')
    res_org_id = models.CharField(max_length=32, null=True, help_text='资源组织ID')
    ip_address = models.CharField(max_length=64, null=True, help_text='IP地址')
    created_at = models.DateTimeField(null=True, help_text='创建时间')
    updated_at = models.DateTimeField(null=True, help_text='更新时间')
    origin_data = jsonfield.JSONField(null=True, help_text='原始数据')
    update_data = jsonfield.JSONField(null=True, help_text='更新数据')
    log_level = models.CharField(max_length=64, null=True, help_text='日志等级')
    extra = models.TextField(max_length=64, null=True, help_text='扩展')

    class Meta:
        db_table = 'clog'