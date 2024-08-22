import logging

import uvicorn

from src.config.config import Config
from src.utils.helpers import setup_logging
from web.app import create_app


def main():
    # Настройка логирования
    setup_logging(logging.DEBUG)  # Устанавливаем уровень логирования на DEBUG для более подробной информации

    # Получение конфигурации из переменных окружения через класс Config
    config = Config()

    # Логирование значений конфигурации для проверки
    logging.debug(f"DATABASE_URL: {config.DATABASE_URL}")
    logging.debug(f"SECRET_KEY: {config.SECRET_KEY}")

    # Создание приложения FastAPI
    app = create_app()

    # Запуск FastAPI приложения с Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
