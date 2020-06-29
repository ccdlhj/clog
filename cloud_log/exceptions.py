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
from portal_core.utils import enum
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


class InternalServerError(APIException):
    status_code = 500
    title = 'Internal Server Error'
    message_format = _('Internal Server Error {message}')

    def __init__(self, message=None, exc=None, status_code=None, **kwargs):
        self.message = message
        self.status_code = status_code or self.status_code
        self.__dict__.update(kwargs)
        self._parse(exc)
        self.detail = str(self.message)

    def _parse(self, exc):
        if exc:
            self.message_format = \
                getattr(exc, "message_format", None) or self.message_format
            message = getattr(exc, "message", None) or self.message or ''
            self.message = self.message_format.format(message=message)
            self.status_code = \
                getattr(exc, "status_code", None) or self.status_code
            self.title = getattr(exc, "title", None) or self.title
            self.__dict__.update(exc.__dict__)

    def __str__(self):
        return self.detail
