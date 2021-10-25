import logging

from config import Settings

def get_logger(logger_name: str) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    settings = Settings()

    log_format = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        '%d/%m/%Y %H:%M:%S'
    )

    c_handler = logging.StreamHandler()
    c_handler.setLevel(settings.log_level)
    c_handler.setFormatter(log_format)

    f_handler = logging.FileHandler('errors.log', encoding='utf-8')
    f_handler.setLevel(logging.WARNING)
    f_handler.setFormatter(log_format)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    logger.setLevel(settings.log_level)

    return logger
