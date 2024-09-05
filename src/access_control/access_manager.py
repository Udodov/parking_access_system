from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database.models import Vehicle


class AccessManager:
    def __init__(self):
        # Множество для хранения разрешенных номерных знаков
        self.allowed_plates: set[str] = set()

    def add_allowed_plate(self, license_plate: str) -> None:
        """
        Добавляет номерной знак в список разрешенных.

        :param license_plate: Номерной знак, который нужно добавить.
        """
        self.allowed_plates.add(license_plate)

    async def check_access(self, license_plate: str, db_session: AsyncSession) -> bool:
        """
        Проверяет, имеет ли номерной знак доступ.

        :param license_plate: Номерной знак для проверки.
        :param db_session: Асинхронная сессия базы данных.
        :return: True, если доступ разрешен, иначе False.
        """
        # Создаем запрос для поиска автомобиля по номерному знаку в базе данных
        query = select(Vehicle).where(Vehicle.license_plate == license_plate)

        # Выполняем асинхронный запрос
        result = await db_session.execute(query)

        # Получаем первую запись из результата
        vehicle = result.scalars().first()

        # Возвращаем True, если автомобиль найден в базе данных или номерной знак в разрешенном списке
        return vehicle is not None or license_plate in self.allowed_plates

    def grant_access(self, license_plate: str) -> bool:
        """
        Проверяет, находится ли номерной знак в списке разрешенных.

        :param license_plate: Номерной знак для проверки.
        :return: True, если доступ разрешен, иначе False.
        """
        return license_plate in self.allowed_plates
