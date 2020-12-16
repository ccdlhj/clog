# -*- coding: utf-8 -*-

from django.db import models
from jsonfield import JSONField


class Clog(models.Model):
    """日志表"""

    uuid = models.CharField(primary_key=True, db_index=True, unique=True,
                            max_length=36, null=False)
    request_id = models.CharField(db_index=True, max_length=40,
                                  null=True, help_text="操作请求ID")

    related_resources = models.TextField(max_length=1024, null=True,
                                         help_text='关联资源id')
    object_uuid = models.CharField(max_length=36, db_index=True, null=True,
                                   help_text='对象ID')
    object_name = models.CharField(max_length=64, null=True,
                                   help_text='对象名称')
    object_type = models.CharField(max_length=64, null=True, db_index=True,
                                   help_text='对象类型')
    res_org_id = models.CharField(max_length=36, db_column='res_org_id',
                                  db_index=True, null=True,
                                  help_text="资源组织ID")
    res_org_name = models.CharField(max_length=64, null=True,
                                    help_text='资源组织名称')
    res_org_id_path = models.TextField(max_length=1024, null=True,
                                       help_text='对象ID位置,所属资源组织ID完整路径')
    res_org_path = models.TextField(max_length=1024, null=True,
                                    help_text='对象位置,所属资源组织完整路径')
    # 当前最多支持 3级 VDC + 项目 + 5级目录, 最大深度为 9
    #     # 单个命名最大长度为 64, 分隔符长度为1, 总长度 = 64*9 + 1*(9-1) = 639
    user_id = models.IntegerField(db_index=True, null=True, help_text='操作人ID')
    user_name = models.CharField(max_length=64, null=True, help_text='操作人')
    ip_address = models.CharField(max_length=64, null=True, help_text='IP地址')

    operation_id = models.IntegerField(null=True, db_index=True,
                                       help_text='操作任务ID')
    operation_name = models.CharField(max_length=255, null=True,
                                      help_text='操作任务名称')
    status = models.CharField(max_length=64, null=True,
                              help_text='日志状态,执行中,成功,失败')
    created_at = models.DateTimeField(null=True, help_text='创建时间')
    updated_at = models.DateTimeField(null=True, auto_now=True,
                                      help_text='更新时间')
    origin_data = JSONField(null=True, help_text='原始数据')
    expected_data = JSONField(null=True, help_text='预期数据')
    result_data = JSONField(null=True, help_text='结果数据')
    extra = JSONField(max_length=1024, null=True, help_text='日志扩展数据json')
    sync_type = models.CharField(max_length=255, null=True, help_text='同步类型')
    cloud_env_id = models.CharField(max_length=36, db_column='cloud_env_id',
                                    db_index=True, null=True, help_text="资源域ID")

    class Meta:
        abstract = True
