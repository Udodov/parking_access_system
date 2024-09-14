# src/database/models.py

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum  # Используем псевдоним, чтобы избежать конфликта с SQLAlchemy Enum

Base = declarative_base()

class VehicleType(PyEnum):
    """Перечисление типов транспортных средств."""
    CAR = "car"
    TRUCK = "truck"
    MOTORCYCLE = "motorcycle"

class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True)
    license_plate = Column(String, unique=True, nullable=False)
    vehicle_type = Column(Enum(VehicleType), nullable=False)
