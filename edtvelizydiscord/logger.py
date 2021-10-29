import logging

import colorlog
from config import Settings

LOG_CONSOLE_FORMAT = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    "%d/%m/%Y %H:%M:%S",
)

LOG_FILE_FORMAT = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    "%d/%m/%Y %H:%M:%S",
)


def get_logger(logger_name: str) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    settings = Settings()

    c_handler = colorlog.StreamHandler()
    c_handler.setLevel(settings.log_level)
    c_handler.setFormatter(LOG_CONSOLE_FORMAT)

    f_handler = logging.FileHandler("errors.log", encoding="utf-8")
    f_handler.setLevel(logging.WARNING)
    f_handler.setFormatter(LOG_FILE_FORMAT)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    logger.setLevel(settings.log_level)

    return logger
