# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud_log', '0002_auto_20200114_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='clog',
            name='sync_type',
            field=models.CharField(help_text=b'\xe5\x90\x8c\xe6\xad\xa5\xe7\xb1\xbb\xe5\x9e\x8b', max_length=255, null=True),
        ),
    ]
