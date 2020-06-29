# -*- coding: utf-8 -*-
import re

from django.utils.translation import ugettext_lazy as _

from portal_rest.exceptions import ValidationError
from cloud_log.utils.common import CLOG_STATUS


REQUEST_ID_REGEX = \
    r'req-[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
REQUEST_ID_PATTERN = re.compile(REQUEST_ID_REGEX)


def validate_request_id(request_id):
    if request_id:
        result = re.match(REQUEST_ID_PATTERN, request_id)
        if not result:
            raise ValidationError(_("Invalid request_id"))


def validate_clog_status(status):
    if status and status not in CLOG_STATUS:
        msg = _("Invalid clog status {status}").format(status=status)
        raise ValidationError(msg)
