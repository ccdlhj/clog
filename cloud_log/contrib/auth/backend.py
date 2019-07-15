# -*- coding: utf-8 -*-
import logging

from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _

from portal_identity.models import User
from portal_identity import exceptions


LOG = logging.getLogger(__name__)


class CMPBackend(object):
    """Django authentication backend for use with ``django.contrib.auth``."""

    def get_user(self, user_id):
        """Returns the current user from the session data.

        If authenticated, this return the user object based on the user ID
        and session data.

        Note: this required monkey-patching the ``contrib.auth`` middleware
        to make the ``request`` object available to the auth backend class.
        """
        if (hasattr(self, 'request') and int(user_id) == self.request.session.get('USER_ID')):
            user = User.objects.get(pk=int(user_id))
            return user
        else:
            return None

    def authenticate(self, request, username, password, **kwargs):
        if not username and not password:
            raise exceptions.UsernameOrPasswordError()
        user = User.objects.get_user_and_check_password(user_name=username, password=password)
        if user and request:
            request.session['USER_ID'] = user.id
            # Update the user object cached in the request
            request._cached_user = user
            request.user = user

        LOG.info('Authentication completed.')
        return user
