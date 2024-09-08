import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")
    REDIS_URL: str | None = os.getenv("REDIS_URL")
    SECRET_KEY: str | None = os.getenv("SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    JWT_EXPIRY: int = 60 * 24 * 7

    class Config:
        case_sensitive = True


config: Config = Config()
