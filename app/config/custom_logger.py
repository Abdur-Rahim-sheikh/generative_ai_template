import logging
import sys

from .settings_config import settings

LEVEL = "DEBUG" if settings.DEBUG else "WARNING"


def get_logger(module_name: str = "database"):
    app_logger = logging.getLogger(name="custom." + module_name)
    app_logger.setLevel(level=LEVEL)

    console_handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        fmt="\x1b[38;20m{levelname} - {name} - {asctime} - {filename} - {funcName} - line({lineno:3d}) - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
    )

    console_handler.setFormatter(formatter)

    if not app_logger.handlers:
        app_logger.addHandler(console_handler)
        app_logger.propagate = False

    return app_logger


app_logger = get_logger()
