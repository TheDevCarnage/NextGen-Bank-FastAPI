import os
import logging
from logging.handlers import RotatingFileHandler
from backend.app.core.config import settings

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FORMAT = (
    "%(asctime)s %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_LEVEL = logging.DEBUG if settings.ENVIRONMENT == "local" else logging.INFO

# Prevent reconfiguration on import reloads
_logger_configured = False


def get_logger(name: str = __name__):
    global _logger_configured

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    if not _logger_configured:
        formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

        # Debug handler
        debug_handler = RotatingFileHandler(
            filename=os.path.join(LOG_DIR, "debug.log"),
            maxBytes=10 * 1024 * 1024,
            backupCount=10,
        )
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(formatter)
        debug_handler.addFilter(lambda record: record.levelno <= logging.WARNING)

        # Error handler
        error_handler = RotatingFileHandler(
            filename=os.path.join(LOG_DIR, "error.log"),
            maxBytes=10 * 1024 * 1024,
            backupCount=10,
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)

        logger.addHandler(debug_handler)
        logger.addHandler(error_handler)

        if settings.ENVIRONMENT == "local":
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        _logger_configured = True

    return logger
