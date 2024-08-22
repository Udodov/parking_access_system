import os


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")


config = Config()
