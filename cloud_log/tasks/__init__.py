# -*- coding:utf-8 -*-
import os

import django

# noqa
if not os.environ.get("DJANGO_SETTINGS_MODULE"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloud_log.settings")
    from cloud_log.tasks.clog.tasks import *

django.setup()
