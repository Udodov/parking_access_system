from sqlalchemy.future import select

from src.database.models import Vehicle


class AccessManager:
    def __init__(self):
        self.allowed_plates = set()

    def add_allowed_plate(self, license_plate):
        self.allowed_plates.add(license_plate)

    async def check_access(self, license_plate, db_session):
        query = select(Vehicle).where(Vehicle.license_plate == license_plate)
        result = await db_session.execute(query)
        vehicle = result.scalars().first()
        return vehicle is not None or license_plate in self.allowed_plates

    def grant_access(self, license_plate):
        return license_plate in self.allowed_plates
