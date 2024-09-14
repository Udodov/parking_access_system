# src/database/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.declarative import declarative_base

from src.config.config import Config
from src.database.models import Vehicle, Base
from src.utils.logger import database_logger

# Получение конфигурации
config = Config()

# Создание асинхронного движка базы данных
engine = create_async_engine(config.DATABASE_URL, echo=True)

# Создание фабрики сессий
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def create_database():
    """
    Создает все таблицы в базе данных.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    database_logger.info("База данных создана.")

async def get_db():
    """
    Асинхронный генератор для получения сессии базы данных.
    """
    async with AsyncSessionLocal() as session:
        yield session

async def save_to_database(dataset):
    """
    Сохраняет датасет в базу данных.

    :param dataset: Список объектов LicensePlate для сохранения.
    """
    async with AsyncSessionLocal() as session:
        for plate in dataset:
            vehicle = Vehicle(
                license_plate=f"{plate.number} {plate.region}",
                vehicle_type=plate.vehicle_type.value
            )
            session.add(vehicle)
        await session.commit()
    database_logger.info(f"Сохранено {len(dataset)} записей в базу данных.")

async def get_vehicle_by_plate(plate_number: str):
    """
    Получает транспортное средство по номерному знаку.

    :param plate_number: Номерной знак транспортного средства.
    :return: Объект Vehicle или None, если не найден.
    """
    database_logger.info(f"Запрос к базе данных для номера: {plate_number}")

    async with AsyncSessionLocal() as session:
        query = select(Vehicle).where(Vehicle.license_plate == plate_number)
        result = await session.execute(query)
        vehicle = result.scalars().first()

        if vehicle:
            database_logger.info(f"Транспортное средство найдено: {vehicle}")
        else:
            database_logger.warning(
                f"Транспортное средство не найдено для номера: {plate_number}"
            )

        return vehicle
