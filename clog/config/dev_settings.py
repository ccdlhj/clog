"""Development settings and globals."""

DEBUG = True
VUE_DEBUG = True

PORTAL_VERSION = "alpha"

WEB_ROOT = '/'

ALLOWED_HOSTS = ['*']

PERMISSION_URLIGNORE = ['.']

LOGGING = {
    'version': 1,
    # When set to True this will disable all logging except
    # for loggers specified in this configuration dictionary. Note that
    # if nothing is specified here and disable_existing_loggers is True,
    # django.db.backends will still log unless it is disabled explicitly.
    'disable_existing_loggers': False,
    'formatters': {
       'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
       }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            # Set the level to "DEBUG" for verbose output logging.
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        # Logging from django.db.backends is VERY verbose, send to null
        # by default.
        'django.db.backends': {
            'handlers': ['null'],
            'propagate': False,
        },
        'stevedore.extension': {
            'handlers': ['null'],
            'propagate': False,
        },
        'requests': {
            'handlers': ['null'],
            'propagate': False,
        },
        'portal_common': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'portal_rest': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'pcitc_openstack': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'portal_pcitc': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'portal_celery': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
