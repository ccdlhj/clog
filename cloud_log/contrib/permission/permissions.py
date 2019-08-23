# -*- coding: utf-8 -*-
import logging
import re
import urlparse

from django.conf import settings
from rest_framework.permissions import BasePermission


LOG = logging.getLogger(__name__)

# 缓存正则编译结果
REGEX_COMPILED_CACHE = {}

API_ROOT = settings.API_ROOT

# 需要忽略权限检查的url正则列表
PERMISSION_URLIGNORE = getattr(settings, 'PERMISSION_URLIGNORE', [])

class URLPermission(BasePermission):

    def check_urlignore(self, request, url):
        # 遍历检查
        for url_regex in PERMISSION_URLIGNORE:
            # 从缓存读取编译好的正则
            regexp_compiled = REGEX_COMPILED_CACHE.get(url_regex)
            if not regexp_compiled:
                regexp_compiled = re.compile(url_regex)
                REGEX_COMPILED_CACHE[url_regex] = regexp_compiled

            # 判断是否满足
            if regexp_compiled.match(url):
                return True

        return False

    def has_permission(self, request, view):
        # 当前的url信息，已经包含形如：[POST]/v1.0.0/auth/show_user
        path_info = '[%s]%s' % (request.method, view.urlpath_info.replace(API_ROOT, '', 1))

        # 跳过不需要认证检查的url
        if self.check_urlignore(request, path_info):
            return True

        # 如果未登录则拒绝执行
        if not hasattr(request, "user"):
            return False

        # 从session中获取url权限信息
        url_permissions = request.user.url_permissions

        # 如果没有权限则拒绝执行
        if url_permissions and path_info in url_permissions:
            return True

        LOG.warning('Permission denied for URL: %s' % str(path_info))
        return False
