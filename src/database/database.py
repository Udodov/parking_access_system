from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

from src.config.config import config
from src.database.models import Vehicle
from src.utils.logger import database_logger

# Создание асинхронного движка базы данных
engine = create_async_engine(config.DATABASE_URL, echo=True)

# Создание фабрики сессий
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    """
    Асинхронный генератор для получения сессии базы данных.
    """
    async with AsyncSessionLocal() as session:
        yield session


async def get_vehicle_by_plate(plate_number: str):
    """
    Получает транспортное средство по номерному знаку.

    :param plate_number: Номерной знак транспортного средства.
    :return: Объект Vehicle или None, если не найден.
    """
    database_logger.info(f"Запрос к базе данных для номера: {plate_number}")

    async with AsyncSessionLocal() as session:
        # Создаем запрос для поиска автомобиля по номерному знаку
        query = select(Vehicle).where(Vehicle.license_plate == plate_number)

        # Выполняем асинхронный запрос
        result = await session.execute(query)

        # Получаем первую запись из результата
        vehicle = result.scalars().first()

        if vehicle:
            database_logger.info(f"Транспортное средство найдено: {vehicle}")
        else:
            database_logger.warning(
                f"Транспортное средство не найдено для номера: {plate_number}"
            )

        return vehicle
