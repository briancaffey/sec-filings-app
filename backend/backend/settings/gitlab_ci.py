"""
Django settings used in GitLab CI job `Pytest`

This file inherits from `backend/backend/settings.py`
"""

from .base import *  # noqa

# Redis

CELERY_LOCK_REDIS_CONNECTION = redis.StrictRedis(  # noqa
    host="redis", port="6379", db=4
)

GENERIC_REDIS = redis.StrictRedis(host="redis", port="6379", db=6)  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'postgres',
        'PORT': '5432',
    },
}


# Logging

log_level = "DEBUG"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),  # noqa
        },
        'portal': {
            'handlers': ['console'],
            'level': os.getenv('PORTAL_LOG_LEVEL', log_level),  # noqa
        },
    },
}

# Static files

STATIC_URL = '/static/'

STATIC_ROOT = 'static'
