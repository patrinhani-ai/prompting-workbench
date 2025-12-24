import logging.config

PROMPTING_WORKBENCH_LOGGING_KEY = ""
PROMPTING_WORKBENCH_LOGGING_DEFAULT_LEVEL = logging.INFO

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "(%(name)s) [%(process)d:%(threadName)s]: %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "formatter": "console",
            "markup": True,
            "rich_tracebacks": True,
            "tracebacks_show_locals": True,
        },
    },
    "loggers": {
        PROMPTING_WORKBENCH_LOGGING_KEY: {
            "handlers": ["console"],
            "level": PROMPTING_WORKBENCH_LOGGING_DEFAULT_LEVEL,
            "propagate": True,
        }
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
