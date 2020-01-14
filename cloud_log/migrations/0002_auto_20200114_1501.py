# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud_log', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clog',
            name='operation_id',
            field=models.IntegerField(help_text=b'\xe6\x93\x8d\xe4\xbd\x9c\xe4\xbb\xbb\xe5\x8a\xa1ID', null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='clog',
            name='res_org_id_path',
            field=models.TextField(help_text=b'\xe5\xaf\xb9\xe8\xb1\xa1ID\xe4\xbd\x8d\xe7\xbd\xae,\xe6\x89\x80\xe5\xb1\x9e\xe8\xb5\x84\xe6\xba\x90\xe7\xbb\x84\xe7\xbb\x87ID\xe5\xae\x8c\xe6\x95\xb4\xe8\xb7\xaf\xe5\xbe\x84', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='clog',
            name='user_name',
            field=models.CharField(help_text=b'\xe6\x93\x8d\xe4\xbd\x9c\xe4\xba\xba', max_length=64, null=True),
        ),
    ]
