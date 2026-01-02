import logging.config

from langchain_core.globals import set_debug, set_verbose

PROMPTING_WORKBENCH_LOGGING_KEY = ""
PROMPTING_WORKBENCH_LOGGING_DEFAULT_LEVEL = logging.INFO

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "(%(name)s) [%(process)d:%(threadName)s]: %(message)s",
        },
        "file": {
            "format": "%(asctime)s (%(name)s) [%(process)d:%(threadName)s] {%(filename)s:%(lineno)d}: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "formatter": "console",
            "markup": True,
            "omit_repeated_times": False,
            "rich_tracebacks": True,
            "tracebacks_show_locals": True,
        },
        "file": {
            # Use RotatingFileHandler to manage file size automatically
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "file",
            "filename": "prompting_workbench.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "encoding": "utf8",
        },
    },
    "loggers": {
        PROMPTING_WORKBENCH_LOGGING_KEY: {
            "handlers": ["file"],
            "level": PROMPTING_WORKBENCH_LOGGING_DEFAULT_LEVEL,
            "propagate": True,
        }
    },
}

logging.config.dictConfig(LOGGING_CONFIG)

# Silence LangChain and LangGraph
logging.getLogger("langchain").setLevel(logging.WARNING)
logging.getLogger("langgraph").setLevel(logging.WARNING)

# Often, noise comes from underlying HTTP clients used by these libs
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)

# Disable the specific internal LangChain console handlers
set_debug(False)
set_verbose(False)
