# -*- coding: utf-8 -*-
"""
URL patterns for the Clog Portal.
"""

from django.conf import settings
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns  # noqa

from portal_rest import PortalDocsView, PortalRouter

# 注册路由
PortalRouter.auto_register_package()

urlpatterns = PortalRouter.urlpatterns  # 装载url

# Development static app and project media serving using the staticfiles app.
urlpatterns += staticfiles_urlpatterns()  # 静态文件

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^docs/', PortalDocsView.as_view(), name='portal-docs'),  # api文档
        url(r'^500/$', 'django.views.defaults.server_error')  # 调试错误页
    )
