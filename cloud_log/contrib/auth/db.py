# -*- coding: utf-8 -*-
import logging
import uuid
from datetime import datetime

from django.db import models
from django.contrib.auth.hashers import make_password, check_password


LOG = logging.getLogger(__name__)

HASHER_PBKDF2_SHA256 = u'pbkdf2_sha256'
SALT = None


def _make_password(password, salt=SALT):
    return make_password(password, salt, HASHER_PBKDF2_SHA256)


def _check_password(password, ciphertext):
    return check_password(password, ciphertext)


class UserManager(models.Manager):

    def create_user(self, **kwargs):
        kwargs["password"] = _make_password(kwargs["password"], SALT)
        kwargs["created_at"] = datetime.now()
        return self.create(**kwargs)

    def update_user(self, id, **kwargs):
        if kwargs:
            kwargs.update({"updated_at": datetime.now()})
        passwd = kwargs.pop('password', None)
        user = self.filter(id=id)
        if passwd:
            kwargs["password"] = _make_password(passwd, SALT)
        return user.update(**kwargs)

    def delete_user(self, id, **kwargs):
        dict = {"updated_at": datetime.now(),
                "deleted": True}
        if kwargs:
            dict.update(kwargs)
        user = self.filter(id=id)
        return user.update(**dict)

    def show_user(self, **kwargs):
        return self.get(**kwargs)

    def get_user(self, **kwargs):
        return self.filter(**kwargs)

    def get_user_and_check_password(self, **kwargs):
        password = kwargs.pop('password', None)
        try:
            user = self.show_user(**kwargs)
        except:
            user = None
        # 验证密码
        if user:
            check = _check_password(password, user.password)
            if not check:
                user = None
        return user
