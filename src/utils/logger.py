import logging
from logging.handlers import RotatingFileHandler
# import os


def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


# Создаем логгеры для разных компонентов системы
main_logger = setup_logger("main", "logs/main.log")
recognition_logger = setup_logger("recognition", "logs/recognition.log")
access_control_logger = setup_logger("access_control", "logs/access_control.log")
database_logger = setup_logger("database", "logs/database.log")
web_logger = setup_logger("web", "logs/web.log")
