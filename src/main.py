import logging
import threading  # Для запуска фонового процесса
import uvicorn

from src.config.config import Config
from src.utils.helpers import setup_logging
from src.recognition.plate_recognition import (
    process_video_stream,
)  # Импорт функции обработки видео
from web.app import create_app


def main():
    # Настройка логирования
    setup_logging(logging.DEBUG)

    # Получение конфигурации из переменных окружения через класс Config
    config = Config()

    # Логирование значений конфигурации для проверки
    logging.debug(f"DATABASE_URL: {config.DATABASE_URL}")
    logging.debug(f"SECRET_KEY: {config.SECRET_KEY}")

    # Создание приложения FastAPI
    app = create_app()

    # Запуск обработки видео потока в отдельном потоке
    video_thread = threading.Thread(target=process_video_stream)
    video_thread.daemon = True  # Позволяет завершать поток при завершении программы
    video_thread.start()

    # Запуск FastAPI приложения с Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
