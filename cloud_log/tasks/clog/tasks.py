# -*- coding:utf-8 -*-
import os
import shutil

from celery import task

from cloud_log.utils.constants import NFS_CLOG_PATH
from portal_common.utils.util import except_handler

from cloud_log.tasks.clog import manager


def export_clog_failed(context, param):
    ds = list(os.listdir(NFS_CLOG_PATH))
    for d in ds:
        if os.path.getmtime(d):
            os.remove(d)
    else:
        shutil.rmtree(d)
    return True


@task(name="export_clog")
@except_handler(name='export_clog_failed')
def export_clog(context, param):
    manager.export_clog(context, param)
