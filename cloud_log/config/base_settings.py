# -*- coding: utf-8 -*-
"""T2cloud settings and globals."""

import sys
import os
import warnings

warnings.formatwarning = lambda message, category, *args, **kwargs: \
    '%s: %s' % (category.__name__, message)

ROOT_URLCONF = 'cloud_log.urls'
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if ROOT_PATH not in sys.path:
    sys.path.append(ROOT_PATH)

BIN_DIR = os.path.abspath(os.path.join(ROOT_PATH, 'bin'))

WEB_ROOT = '/portal/'
LOGOUT_URL = None
LOCAL_PATH = None

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
VUE_DEBUG = False

LOGIN_URL = None
LOGIN_REDIRECT_URL = None
STATIC_ROOT = None
STATIC_URL = None
SECRET_KEY = None


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                'django.core.context_processors.debug',
                'django.core.context_processors.i18n',
                'django.core.context_processors.request',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

# AUTHENTICATION_BACKENDS = ('cloud_log.contrib.auth.backend.CMPBackend',)
# AUTH_USER_MODEL = 'cloud_log.User'

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = False

# when doing upgrades, it may be wise to stick to PickleSerializer
# NOTE(berendt): Check during the K-cycle if this variable can be removed.
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

SESSION_TIMEOUT = 1800

# A token can be near the end of validity when a page starts loading, and
# invalid during the rendering which can cause errors when a page load.
# TOKEN_TIMEOUT_MARGIN defines a time in seconds we retrieve from token
# validity to avoid this issue. You can adjust this time depending on the
# performance of the infrastructure.
TOKEN_TIMEOUT_MARGIN = 10

# When using cookie-based sessions, log error when the session cookie exceeds
# the following size (common browsers drop cookies above a certain size):
SESSION_COOKIE_MAX_SIZE = 4093


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGES = (
    ('en', 'English'),
    ('zh-CN', 'Simplified Chinese'),
)
LANGUAGE_CODE = 'zh-CN'
USE_I18N = True
USE_L10N = True
USE_TZ = True

TIME_ZONE = 'Asia/Shanghai'


SITE_BRANDING = 'Portal'


# cors config. https://github.com/ottoyiu/django-cors-headers
CORS_ALLOW_HEADERS = ['X-Access-Module', 'X-Auth-Token', 'Content-Type', 'X-Auth-Trust', 'Prepay-API-Auth', 'Authorization']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True



# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'corsheaders',
    'rest_framework',
    'rest_framework_docs',
    't2cloud_rest',
    'cloud_log',
)


MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    't2cloud_rest.middleware.RestMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)



REST_FRAMEWORK_DOCS = {
    'HIDE_DOCS': False
}

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 使DRF接口获得认证
        't2cloud_rest.auth.middleware.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 't2cloud_rest.auth.permissions.URLPermission',
    ),
}

API_ROOT = 'api'
T2CLOUD_REST = {
    'register_package': [
        (API_ROOT, 'cloud_log.rest', True),
    ],
    'except_csrf': False,
    'view_middleware_class': (
        # 'cloud_log.contrib.auth.middleware.ClogAuthTokenMiddleware',
    ),
    'exception_handler_method': {
        # 't2cloud_portal.rest_handler.handle_nova_exception':
        #     (
        #         'novaclient.exceptions.UnsupportedVersion',
        #         'novaclient.exceptions.CommandError',
        #     ),
    },
}

# 忽略所有GET请求。
PERMISSION_URLIGNORE = ['^\[GET\]']
