# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from django.utils.translation import ugettext_lazy as _
from t2cloud.utils import enum
from rest_framework.exceptions import APIException

CODE = enum(
    SERVER_ERROR_CODE=-1,
    USERNOTFOUND_CODE=-2,
    TOKEN_ERROR_CODE=-3,
    LINKUNAVAILABLE_ERROR_CODE=-4,
    OPERATIONFREQUENTLY_ERROR_CODE=-5,
    USERNAMEORPASSWORD_ERROR_CODE=403,
    PASSWORD_ERROR_CODE=-7,
    USERNOTACTIVATED_EXCEPTION_CODE=-11,
    USERDISABLED_EXCEPTION_CODE=-12,
    PASSWORD_NEED_RESET_CODE=-13,
    TEMPORARY_PASSWORD_CODE=-14,
    PASSWORD_HISTORY_REPETITION_CODE=-15,
    USER_DORMANCY_EXCEPTION_CODE=-16,
    THETEMPORARYUSERHAS=-17,
)


class PortalAuthException(APIException):
    """Generic error class to identify and catch our own errors."""
    code = CODE.SERVER_ERROR_CODE
    status_code = 500
    title = 'Internal Server Error'
    message_format = _('Internal Server Error')

    def __init__(self, exc=None, message=None, status_code=None, **kwargs):
        self.message = message or self.message_format
        self.status_code = status_code or self.status_code
        self.__dict__.update(kwargs)
        self._parse(exc)
        self.detail = str(self.message)

    def _parse(self, exc):
        if exc:
            self.message = getattr(exc, "message", None) or self.message
            self.message_format = getattr(exc, "message_format", None) or self.message_format
            self.status_code = getattr(exc, "status_code", None) or self.status_code
            self.title = getattr(exc, "title", None) or self.title
            self.code = getattr(exc, "code", None) or self.code
            self.__dict__.update(exc.__dict__)

    def __str__(self):
        return self.detail


class ValidationError(PortalAuthException):
    message_format = _("Validation Error.")
    status_code = 400
    title = 'Validation Error'


class Unauthorized(PortalAuthException):
    message_format = _("The request you have made requires authentication.")
    status_code = 401
    title = 'Unauthorized'


class UserNotActivatedException(Unauthorized):
    # code = CODE.USERNOTACTIVATED_EXCEPTION_CODE
    message_format = _('User Not Activated')
    title = 'User Not Activated'


class UserDormancyException(Unauthorized):
    code = CODE.USER_DORMANCY_EXCEPTION_CODE
    message_format = _('User Dormancy')
    title = 'User Dormancy'


class UserDisabledException(Unauthorized):
    code = CODE.USERDISABLED_EXCEPTION_CODE
    message_format = _('User has been frozen')


class NotFound(PortalAuthException):
    message_format = _('Not Found')
    status_code = 404
    title = 'Not Found'


class UserNotFound(NotFound):
    code = CODE.USERNOTFOUND_CODE
    message_format = _('User Not Found')

    def __init__(self, user=None):
        super(UserNotFound, self).__init__()
        if user:
            self.message_format = _("Could not find user: %s") % user


class ForbiddenException(PortalAuthException):
    status_code = 403
    message_format = _('Forbidden')
    title = 'Forbidden'


class PasswordVerificationError(ForbiddenException):
    message_format = _("The password length must be less than or equal "
                       "to %(size)i. The server could not comply with the "
                       "request because the password is invalid.")
    code = CODE.USERNOTFOUND_CODE

    def __init__(self, format=None):
        super(PasswordVerificationError, self).__init__()
        if format:
            self.message_format = self.message_format % format


class TokenError(ForbiddenException):
    code = CODE.TOKEN_ERROR_CODE
    message_format = _('Token invalid')


class LinkUnavailableError(ForbiddenException):
    code = CODE.LINKUNAVAILABLE_ERROR_CODE
    message_format = _('Link Unavailable')


class OperationFrequentlyError(ForbiddenException):
    code = CODE.OPERATIONFREQUENTLY_ERROR_CODE
    message_format = _('operation frequently')


class UsernameOrPasswordError(ForbiddenException):
    code = CODE.USERNAMEORPASSWORD_ERROR_CODE
    message_format = _('The username or password invalid')


class PasswordError(ForbiddenException):
    code = CODE.PASSWORD_ERROR_CODE
    message_format = _('The password invalid')


class MethodNotAllowedError(PortalAuthException):
    status_code = 405
    code = CODE.SERVER_ERROR_CODE
    message_format = _('Method Not Allowed')


class TemporaryPasswordException(ForbiddenException):
    # code = CODE.TEMPORARY_PASSWORD_CODE
    message_format = _('For the first time login, The password needs to be reset')
    title = 'User Password Need Reset'


class PasswordNeedResetException(ForbiddenException):
    # code = CODE.PASSWORD_NEED_RESET_CODE
    message_format = _('The password has not been changed for a long time, The password needs to be reset.')
    title = 'User Password Need Reset'


class PasswordHistoryRepetitionException(ForbiddenException):
    code = CODE.PASSWORD_HISTORY_REPETITION_CODE
    message_format = _('The password has been used in the past')
    title = 'User Password History Repetition'


class TheTemporaryUserHasExpiredException(ForbiddenException):
    code = CODE.THETEMPORARYUSERHAS
    message_format = _('User expired')
    title = 'User expired'
