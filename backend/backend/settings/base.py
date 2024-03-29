"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

from kombu import Exchange, Queue
import redis

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEBUG", "1")))

# Allowed Hosts
ALLOWED_HOSTS = ["*"]

# Application definition
BASE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # project apps
    "accounts",
    "core",
    "filing.apps.FilingConfig",
    # third part
    "rest_framework",
    "rest_framework.authtoken",
    "social_django",
]


AUTH_USER_MODEL = "accounts.CustomUser"

INSTALLED_APPS = BASE_APPS


# Python Social Auth

SOCIAL_AUTH_POSTGRES_JSONFIELD = True

for key in [
    "LINKEDIN_OAUTH2_KEY",
    "LINKEDIN_OAUTH2_SECRET",
]:
    # Use exec instead of eval here because we're not
    # just trying to evaluate a dynamic value here;
    # we're setting a module attribute whose name varies.
    exec(f"SOCIAL_AUTH_{key} = os.environ.get('{key}')")


AUTHENTICATION_BACKENDS = (
    "social_core.backends.linkedin.LinkedinOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    # 'social_core.pipeline.user.get_username',
    "social_core.pipeline.social_auth.associate_by_email",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)

# Add email to requested authorizations.
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ["r_liteprofile", "r_emailaddress"]
# Add the fields so they will be requested from linkedin.
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = [
    "emailAddress",
    "formattedName",
    "publicProfileUrl",
    "pictureUrl",
]
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [
    ("id", "id"),
    ("formattedName", "name"),
    ("emailAddress", "email_address"),
    ("pictureUrl", "picture_url"),
    ("publicProfileUrl", "profile_url"),
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "core.middleware.RequestLogMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "filing.middleware.PeriodMiddleware",
]

# Django REST Framework

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",  # noqa
    "PAGE_SIZE": 10,
    "DEFAULT_PERMISSION_CLASSES": (
        # 'rest_framework.permissions.IsAuthenticated',
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
        # 'rest_framework.permissions.AllowAny',
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
}

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

AUTH_USER_MODEL = "accounts.CustomUser"

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("POSTGRES_NAME", "postgres"),
        "USER": os.environ.get("POSTGRES_USERNAME", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get("POSTGRES_SERVICE_HOST", "postgres"),
        "PORT": os.environ.get("POSTGRES_SERVICE_PORT", 5432),
    }
}

REDIS_SERVICE_HOST = os.environ.get("REDIS_SERVICE_HOST", "redis")

REDIS = redis.Redis(
    host=REDIS_SERVICE_HOST,
    port=6379,
    db=3,
    charset="utf-8",
    decode_responses=True,
)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_SERVICE_HOST}:6379/4",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "djangoredis",
    }
}

# Celery

CELERY_QUEUE_DEFAULT = "default"
CELERY_QUEUE_OTHER = "other"

CELERY_BROKER_URL = f"redis://{REDIS_SERVICE_HOST}:6379/1"
CELERY_RESULT_BACKEND = f"redis://{REDIS_SERVICE_HOST}:6379/2"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACKS_LATE = True
CELERY_DEFAULT_QUEUE = CELERY_QUEUE_DEFAULT
CELERY_SEND_EVENTS = True
CELERYD_PREFETCH_MULTIPLIER = 1
CELERY_QUEUES = (
    Queue(
        CELERY_QUEUE_DEFAULT,
        Exchange(CELERY_QUEUE_DEFAULT),
        routing_key=CELERY_QUEUE_DEFAULT,
    ),
    Queue(
        CELERY_QUEUE_OTHER,
        Exchange(CELERY_QUEUE_OTHER),
        routing_key=CELERY_QUEUE_OTHER,
    ),
)

CELERY_TASK_ROUTES = {}

CELERY_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_TASK_DEFAULT_QUEUE = CELERY_QUEUE_DEFAULT
CELERY_TASK_DEFAULT_EXCHANGE = CELERY_QUEUE_DEFAULT
CELERY_TASK_DEFAULT_ROUTING_KEY = CELERY_QUEUE_DEFAULT

CELERY_BEAT_SCHEDULE = {}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "assets", "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "assets", "media")
