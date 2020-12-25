# -*- coding: utf-8 -*

import requests
import time

from django.conf import settings

from portal_audit_log.utils.response_utils import service_response_wrapper


TOKEN_EXPIRY_TIME = getattr(settings, 'TOKEN_EXPIRY_TIME', 500)


class SecurityClient(object):
    version = 'v1.0.0'

    def __init__(self, request=None, version='v1.0.0', token=None, url=None):
        self.version = version
        self.base_url = url or settings.SECURITY_API_BASE_URL
        self.session = request.session if request else {}
        self._token = token
        if not token and request and hasattr(request, 'auth'):
            self._token = request.auth

    def _get_token(self):
        if not self._token:
            if self.session.get("service_token_expiry", 0) > time.time():
                self.session['service_token_expiry'] =\
                    time.time() + TOKEN_EXPIRY_TIME
                self._token = self.session['service_token']
            else:
                TOKEN_AUTH_CREDENTIAL = settings.TOKEN_AUTH_CREDENTIAL
                CREDENTIAL = TOKEN_AUTH_CREDENTIAL.get('CREDENTIAL')
                username = CREDENTIAL.get('username')
                password = CREDENTIAL.get('password')
                auth_data = {'username': username, 'password': password}
                r = requests.post(TOKEN_AUTH_CREDENTIAL.get('OBTAIN_TOKEN_URL'),
                                  json=auth_data)
                data = r.json().get('data')
                self.session['service_token'] = data.get('token')
                self.session['service_token_expiry'] = data.get('token_expiry')
                self._token = self.session['service_token']

        return 'Token %s' % self._token

    token = property(_get_token)

    def _compose_url(self, action, url_prefix=None):
        url = (url_prefix or self.base_url) + 'api/' + self.version + action
        return url

    @service_response_wrapper
    def show(self, data=None):
        url = self._compose_url('/config/security_config/show')
        r = requests.get(url, headers={'Authorization': self.token})
        return r
