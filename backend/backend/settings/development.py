from .base import *  # noqa

DEBUG_APPS = ["debug_toolbar", "django_extensions"]

INSTALLED_APPS = DEBUG_APPS + BASE_APPS  # noqa

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
] + MIDDLEWARE  # noqa


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}

# for jupyter notebooks
NOTEBOOK_ARGUMENTS = [
    "--ip",
    "0.0.0.0",
    "--allow-root",
    "--no-browser",
]

GRAPH_MODELS = {
    "all_applications": True,
    "group_models": True,
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),  # noqa
        },
    },
}
