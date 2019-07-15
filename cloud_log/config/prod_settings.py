DEBUG = False
VUE_DEBUG = False

LOCAL_PATH = "/tmp"

PORTAL_VERSION = "beta"

WEB_ROOT = '/portal'

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
            'level': 'INFO',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            # Set the level to "DEBUG" for verbose output logging.
            'level': 'INFO',
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
            'level': 'INFO',
            'propagate': False,
        },
        'portal_rest': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'pcitc_openstack': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'portal_celery': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'portal_pcitc': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

