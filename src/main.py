# src/main.py

import os
import logging
import threading
import uvicorn
import asyncio
from typing import List

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config.config import Config
from src.utils.helpers import setup_logging
from src.utils.logger import main_logger
from src.recognition.plate_recognition import process_video_stream
from web.app import create_app
from src.database.database import create_database, save_to_database, get_vehicle_by_plate
from src.database.models import Vehicle, VehicleType, Base

from src.data_generation.license_plate_generator import (
    generate_dataset,
    LicensePlate,
    save_to_json,
    save_to_csv
)

async def generate_and_save_dataset():
    # Создание асинхронного движка и сессии
    engine = create_async_engine(Config().DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    
    async with async_session() as session:
        # Проверяем, есть ли записи в таблице Vehicle
        result = await session.execute('SELECT COUNT(*) FROM vehicles')
        count = result.scalar()

        if count == 0:
            main_logger.info("База данных пуста. Генерируем новый датасет.")

            dataset_size = 1000
            dataset = generate_dataset(dataset_size)

            # Определяем директорию для хранения файлов
            output_dir = 'data'
            os.makedirs(output_dir, exist_ok=True)  # Создаем директорию, если ее нет

            # Пути и имена файлов
            json_filename = os.path.join(output_dir, 'license_plates.json')
            csv_filename = os.path.join(output_dir, 'license_plates.csv')

            # Сохранение в JSON
            await save_to_json(dataset, json_filename)
            main_logger.info(f"Датасет сохранен в JSON файл: {json_filename}")

            # Сохранение в CSV
            await save_to_csv(dataset, csv_filename)
            main_logger.info(f"Датасет сохранен в CSV файл: {csv_filename}")

            # Сохранение в базу данных
            await save_to_database(dataset)
            main_logger.info(f"Датасет сохранен в базу данных. Всего записей: {dataset_size}")
        else:
            main_logger.info(f"В базе данных уже есть {count} записей.")
            # Спрашиваем у пользователя, хочет ли он добавить новые данные
            user_input = input("Хотите добавить новые данные в базу данных? (y/n): ").strip().lower()
            if user_input == 'y':
                additional_dataset_size = int(input("Сколько новых записей сгенерировать?: "))
                additional_dataset = generate_dataset(additional_dataset_size)

                # Сохранение новых данных в файлы
                output_dir = 'data'
                os.makedirs(output_dir, exist_ok=True)

                json_filename = os.path.join(output_dir, 'additional_license_plates.json')
                csv_filename = os.path.join(output_dir, 'additional_license_plates.csv')

                await save_to_json(additional_dataset, json_filename)
                await save_to_csv(additional_dataset, csv_filename)

                # Сохранение в базу данных
                await save_to_database(additional_dataset)
                main_logger.info(f"Добавлено {additional_dataset_size} новых записей в базу данных.")
            else:
                main_logger.info("Новые данные не будут добавлены.")

async def add_plate_manually():
    number = input("Введите номер автомобиля (формат: А123ВС): ").strip().upper()
    region = input("Введите регион (формат: 77): ").strip()
    vehicle_type_input = input("Введите тип транспортного средства (car, truck, motorcycle): ").strip().lower()

    # Преобразуем ввод пользователя в VehicleType
    vehicle_type_map = {
        'car': VehicleType.CAR,
        'truck': VehicleType.TRUCK,
        'motorcycle': VehicleType.MOTORCYCLE
    }
    vehicle_type = vehicle_type_map.get(vehicle_type_input)

    if not vehicle_type:
        print("Некорректный тип транспортного средства.")
        return

    license_plate = f"{number}{region}"

    # Создаем объект Vehicle
    vehicle = Vehicle(
        license_plate=license_plate,
        vehicle_type=vehicle_type
    )

    # Сохраняем в базу данных
    engine = create_async_engine(Config().DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        session.add(vehicle)
        await session.commit()
        main_logger.info(f"Добавлен новый автомобиль: {license_plate}, тип: {vehicle_type.value}")

async def main_async():
    # Генерация и сохранение датасета
    await generate_and_save_dataset()

    # Спрашиваем у администратора, хочет ли он добавить номера вручную
    admin_input = input("Хотите добавить номер вручную? (y/n): ").strip().lower()
    while admin_input == 'y':
        await add_plate_manually()
        admin_input = input("Хотите добавить еще номер? (y/n): ").strip().lower()

def main():
    # Настройка логирования
    setup_logging(logging.DEBUG)
    main_logger.info("Система управления доступом на парковку запущена")

    # Получение конфигурации из переменных окружения через класс Config
    config = Config()

    # Логирование значений конфигурации для проверки
    main_logger.debug(f"DATABASE_URL: {config.DATABASE_URL}")
    main_logger.debug(f"SECRET_KEY: {config.SECRET_KEY}")

    # Создание базы данных и таблиц (если необходимо)
    create_database()

    # Запуск основного асинхронного метода
    asyncio.run(main_async())

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
