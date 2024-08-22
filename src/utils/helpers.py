import logging


def setup_logging(log_level=logging.INFO):
    """
    Настройка логирования для всего приложения.

    :param log_level: Уровень логирования, по умолчанию INFO.
    """
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.info("Логирование настроено.")
