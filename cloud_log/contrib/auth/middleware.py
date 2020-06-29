# -*- coding: utf-8 -*-
import json
import logging
import time

import requests
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication as BaseTokenAuthentication
from rest_framework.authentication import get_authorization_header

from portal_core.utils import ResourceWrapper

LOG = logging.getLogger(__name__)

TOKEN_AUTH_CREDENTIAL = getattr(settings, 'TOKEN_AUTH_CREDENTIAL', {})


class TokenAuthentication(BaseTokenAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(request, token)

    def verify_token(self, key):
        # 验证token
        try:
            AUTH_TOKEN = TOKEN_AUTH_CREDENTIAL.get('AUTH_TOKEN', None)
            if AUTH_TOKEN:
                auth_token = AUTH_TOKEN
            else:
                OBTAIN_TOKEN_URL = TOKEN_AUTH_CREDENTIAL['OBTAIN_TOKEN_URL']
                CREDENTIAL = TOKEN_AUTH_CREDENTIAL['CREDENTIAL']
                auth_token_re = requests.post(OBTAIN_TOKEN_URL,
                                              data=json.dumps(CREDENTIAL),
                                              headers={'content-type': 'application/json;charset=UTF-8', },
                                              verify=False)
                auth_token = json.loads(auth_token_re.content)['data']['token']

            VERIFY_TOKEN_URL = TOKEN_AUTH_CREDENTIAL['VERIFY_TOKEN_URL']
            re = requests.post(VERIFY_TOKEN_URL,
                               data=json.dumps({'token': key}),
                               headers={'content-type': 'application/json;charset=UTF-8',
                                        'Authorization': 'Token %s' % auth_token},
                               verify=False)
            info = json.loads(re.content)['data']
            return info
        except Exception as e:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

    def authenticate_credentials(self, request, key):
        token_info = request.session.get('_TOKEN_CACHE', None)
        # 从session中获取缓存的认证信息，并判断是否超时需要重新验证
        if token_info and token_info['token'] == key and token_info['expire_date'] > time.time():
            user_info = token_info['user_info']
        else:
            # 验证token
            user_info = self.verify_token(key)
            # 默认60后重新验证
            expiry = TOKEN_AUTH_CREDENTIAL.get('expiry', 60)
            request.session['_TOKEN_CACHE'] = {
                'token': key,
                'user_info': user_info,
                'expire_date': time.time() + expiry,
            }

        if user_info:
            # 返回用户
            return ResourceWrapper(user_info), key

        raise exceptions.AuthenticationFailed(_('Invalid token.'))
