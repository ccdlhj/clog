# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud_log', '0003_clog_sync_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='clog',
            name='cloud_env_id',
            field=models.CharField(help_text=b'\xe8\xb5\x84\xe6\xba\x90\xe5\x9f\x9fID', max_length=36, null=True, db_column=b'cloud_env_id', db_index=True),
        ),
    ]
