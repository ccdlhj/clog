# -*- coding: utf-8 -*-
import functools
import logging

from django.db import close_old_connections
from django.db import connections
from django.db import models

logger = logging.getLogger(__name__)


def generate_clog_table_name(clog_datetime):
    # generate clog table name
    year = str(clog_datetime.year)
    month = str(clog_datetime.month)
    return 'clog-' + year + '-' + month


def close_db_connections(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            close_old_connections()
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.error('The db operation failure: %s' % e.message)

    return wrapper


def get_model(table_name, base_model, options=None):
    class DynamicModelMetaclass(models.base.ModelBase):
        def __new__(cls, name, bases, attrs):
            return models.base.ModelBase.__new__(cls, str(table_name), bases, attrs)

    class DynamicModel(base_model):
        __metaclass__ = DynamicModelMetaclass

        @staticmethod
        def is_exists(alias='default'):
            return table_name in connections[alias].introspection.table_names()

        @staticmethod
        def get_tables(prefix, alias='default'):
            return [t for t in connections[alias].introspection.table_names() if t.startswith(prefix)]

        @classmethod
        def create_table(model_cls, alias='default'):
            if not model_cls.is_exists():
                with connections[alias].schema_editor() as schema_editor:
                    schema_editor.create_model(model_cls)

        @classmethod
        def drop_table(model_cls, alias='default'):
            if model_cls.is_exists():
                with connections[alias].schema_editor() as schema_editor:
                    schema_editor.delete_model(model_cls)

        class Meta:
            db_table = table_name

        if options:
            for key, value in options.items():
                setattr(Meta, key, value)  # 设置模型的属性

    return DynamicModel
