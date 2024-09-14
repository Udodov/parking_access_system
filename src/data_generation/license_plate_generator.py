# src.data_generation.license_plate_generator

import json
import csv
import random
from typing import List, Tuple
from dataclasses import dataclass

from src.config.config import Config
from src.database.models import Vehicle, VehicleType
from src.database.database import AsyncSessionLocal

config = Config()  # Инициализируем конфигурацию

@dataclass
class LicensePlate:
    """Класс для представления номерного знака."""
    number: str  # Номер
    region: str  # Код региона
    vehicle_type: VehicleType  # Тип транспортного средства

class LicensePlateGenerator:
    """Класс для генерации номерных знаков."""

    # Допустимые буквы для номерных знаков
    ALLOWED_LETTERS: str = "АВЕКМНОРСТУХ"
    # Список кодов регионов (от 01 до 99 и от 102 до 199)
    REGIONS: List[str] = [f"{i:02d}" for i in range(1, 100)] + [f"{i:03d}" for i in range(102, 200)]

    @staticmethod
    def generate_passenger_plate() -> Tuple[str, str]:
        """Генерирует номер для легкового автомобиля."""
        # Формат: X000XX
        letters = random.choices(LicensePlateGenerator.ALLOWED_LETTERS, k=3)
        numbers = f"{random.randint(0, 999):03d}"
        region = random.choice(LicensePlateGenerator.REGIONS)
        number = f"{letters[0]}{numbers}{letters[1]}{letters[2]}"
        return number, region

    @staticmethod
    def generate_truck_plate() -> Tuple[str, str]:
        """Генерирует номер для грузового автомобиля."""
        # Для простоты используем тот же формат, но можно изменить под нужный формат
        return LicensePlateGenerator.generate_passenger_plate()

    @staticmethod
    def generate_motorcycle_plate() -> Tuple[str, str]:
        """Генерирует номер для мотоцикла."""
        # Формат: 0000XX 00 или 0000XX 000
        letters = random.choices(LicensePlateGenerator.ALLOWED_LETTERS, k=2)
        numbers = f"{random.randint(0, 9999):04d}"
        region = random.choice(LicensePlateGenerator.REGIONS)
        number = f"{numbers}{letters[0]}{letters[1]}"
        return number, region
   
    @classmethod
    def generate_plate(cls, vehicle_type: VehicleType) -> LicensePlate:
        """Генерирует номерной знак для указанного типа транспортного средства."""
        if vehicle_type == VehicleType.CAR:
            number, region = cls.generate_passenger_plate()
        elif vehicle_type == VehicleType.TRUCK:
            number, region = cls.generate_truck_plate()
        elif vehicle_type == VehicleType.MOTORCYCLE:
            number, region = cls.generate_motorcycle_plate()
        else:
            raise NotImplementedError(f"Генерация для {vehicle_type.value} не реализована.")
        
        return LicensePlate(number, region, vehicle_type)

def generate_dataset(size: int) -> List[LicensePlate]:
    """Генерирует набор данных номерных знаков."""
    vehicle_types = [VehicleType.CAR, VehicleType.TRUCK, VehicleType.MOTORCYCLE]
    dataset = []
    for _ in range(size):
        vehicle_type = random.choice(vehicle_types)
        plate = LicensePlateGenerator.generate_plate(vehicle_type)
        dataset.append(plate)
    return dataset

async def save_to_json(dataset: List[LicensePlate], filename: str):
    """Асинхронно сохраняет датасет в JSON файл."""
    # Преобразуем данные перед записью
    data = [
        {
            'number': plate.number,
            'region': plate.region,
            'vehicle_type': plate.vehicle_type.value
        }
        for plate in dataset
    ]
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

async def save_to_csv(dataset: List[LicensePlate], filename: str):
    """Асинхронно сохраняет датасет в CSV файл."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['number', 'region', 'vehicle_type'])  # Заголовки
        for plate in dataset:
            writer.writerow([plate.number, plate.region, plate.vehicle_type.value])

async def save_to_database(dataset: List[LicensePlate]):
    """Асинхронно сохраняет датасет в базу данных PostgreSQL."""
    async with AsyncSessionLocal() as session:
        for plate in dataset:
            vehicle = Vehicle(
                license_plate=f"{plate.number}{plate.region}",
                vehicle_type=plate.vehicle_type
            )
            session.add(vehicle)
        await session.commit()
 