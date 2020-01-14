# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clog',
            fields=[
                ('uuid', models.CharField(max_length=36, unique=True, serialize=False, primary_key=True, db_index=True)),
                ('request_id', models.CharField(help_text=b'\xe6\x93\x8d\xe4\xbd\x9c\xe8\xaf\xb7\xe6\xb1\x82ID', max_length=40, null=True, db_index=True)),
                ('object_uuid', models.CharField(help_text=b'\xe5\xaf\xb9\xe8\xb1\xa1ID', max_length=36, null=True, db_index=True)),
                ('object_name', models.CharField(help_text=b'\xe5\xaf\xb9\xe8\xb1\xa1\xe5\x90\x8d\xe7\xa7\xb0', max_length=64, null=True)),
                ('object_type', models.CharField(help_text=b'\xe5\xaf\xb9\xe8\xb1\xa1\xe7\xb1\xbb\xe5\x9e\x8b', max_length=64, null=True, db_index=True)),
                ('res_org_id', models.CharField(help_text=b'\xe8\xb5\x84\xe6\xba\x90\xe7\xbb\x84\xe7\xbb\x87ID', max_length=36, null=True, db_column=b'res_org_id', db_index=True)),
                ('res_org_name', models.CharField(help_text=b'\xe8\xb5\x84\xe6\xba\x90\xe7\xbb\x84\xe7\xbb\x87\xe5\x90\x8d\xe7\xa7\xb0', max_length=64, null=True)),
                ('res_org_id_path', models.TextField(help_text=b'\xe5\xaf\xb9\xe8\xb1\xa1\xe4\xbd\x8d\xe7\xbd\xae,\xe6\x89\x80\xe5\xb1\x9e\xe8\xb5\x84\xe6\xba\x90\xe7\xbb\x84\xe7\xbb\x87ID\xe5\xae\x8c\xe6\x95\xb4\xe8\xb7\xaf\xe5\xbe\x84', max_length=1024, null=True)),
                ('res_org_path', models.TextField(help_text=b'\xe5\xaf\xb9\xe8\xb1\xa1\xe4\xbd\x8d\xe7\xbd\xae,\xe6\x89\x80\xe5\xb1\x9e\xe8\xb5\x84\xe6\xba\x90\xe7\xbb\x84\xe7\xbb\x87\xe5\xae\x8c\xe6\x95\xb4\xe8\xb7\xaf\xe5\xbe\x84', max_length=1024, null=True)),
                ('user_id', models.IntegerField(help_text=b'\xe6\x93\x8d\xe4\xbd\x9c\xe4\xba\xbaID', null=True, db_index=True)),
                ('user_name', models.CharField(help_text=b'\xe6\x93\x8d\xe4\xbd\x9c\xe4\xba\xba', max_length=128, null=True)),
                ('ip_address', models.CharField(help_text=b'IP\xe5\x9c\xb0\xe5\x9d\x80', max_length=64, null=True)),
                ('operation_id', models.CharField(help_text=b'\xe6\x93\x8d\xe4\xbd\x9c\xe4\xbb\xbb\xe5\x8a\xa1ID', max_length=36, null=True, db_index=True)),
                ('operation_name', models.CharField(help_text=b'\xe6\x93\x8d\xe4\xbd\x9c\xe4\xbb\xbb\xe5\x8a\xa1\xe5\x90\x8d\xe7\xa7\xb0', max_length=255, null=True)),
                ('status', models.CharField(help_text=b'\xe6\x97\xa5\xe5\xbf\x97\xe7\x8a\xb6\xe6\x80\x81,\xe6\x89\xa7\xe8\xa1\x8c\xe4\xb8\xad,\xe6\x88\x90\xe5\x8a\x9f,\xe5\xa4\xb1\xe8\xb4\xa5', max_length=64, null=True)),
                ('created_at', models.DateTimeField(help_text=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4', null=True)),
                ('updated_at', models.DateTimeField(help_text=b'\xe6\x9b\xb4\xe6\x96\xb0\xe6\x97\xb6\xe9\x97\xb4', auto_now=True, null=True)),
                ('origin_data', jsonfield.fields.JSONField(help_text=b'\xe5\x8e\x9f\xe5\xa7\x8b\xe6\x95\xb0\xe6\x8d\xae', null=True)),
                ('expected_data', jsonfield.fields.JSONField(help_text=b'\xe9\xa2\x84\xe6\x9c\x9f\xe6\x95\xb0\xe6\x8d\xae', null=True)),
                ('result_data', jsonfield.fields.JSONField(help_text=b'\xe7\xbb\x93\xe6\x9e\x9c\xe6\x95\xb0\xe6\x8d\xae', null=True)),
                ('extra', jsonfield.fields.JSONField(help_text=b'\xe6\x97\xa5\xe5\xbf\x97\xe6\x89\xa9\xe5\xb1\x95\xe6\x95\xb0\xe6\x8d\xaejson', max_length=1024, null=True)),
            ],
            options={
                'db_table': 'clog',
            },
        ),
    ]
