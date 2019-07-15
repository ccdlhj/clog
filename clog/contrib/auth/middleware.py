# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.contrib.sessions import middleware
from django.core.cache import cache
from rest_framework.authentication import SessionAuthentication as BaseAuthentication

LOG = logging.getLogger(__name__)


class SessionMiddleware(middleware.SessionMiddleware):
    def process_request(self, request):
        session_key = None
        token = request.META.get('HTTP_X_AUTH_TOKEN', None)
        if not token:
            session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
        else:

            try:
                session_key = cache.get(token)
            except Exception as e:
                LOG.error('Session [token:%s] not found', token)

        request.session = self.SessionStore(session_key)


class SessionAuthentication(BaseAuthentication):
    """
    drf中通过共享session与cmp进行认证
    """

    def authenticate(self, request):
        """
        Returns a `User` if the request session currently has a logged in user.
        Otherwise returns `None`.
        """

        # TODO: 认证通过的判断需要整理，目前只是根据session中保存的用户状态判断
        user_attr = ['id', 'name', 'email', 'status', 'is_superuser', 'type']
        user = {attr: request.session.get('CMP_USER_%s' % attr.upper(), None) for attr in user_attr}
        if user['status'] != 'ACTIVE':
            return None

        # csrf防御
        self.enforce_csrf(request)

        return (user, None)
