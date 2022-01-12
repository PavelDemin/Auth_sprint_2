import logging
import logging.config

from app.settings.logger import LOGGING


def init_log_config():
    logging.config.dictConfig(LOGGING) # type: ignore


def get_logger():
    return logging.getLogger('auth_logger')

