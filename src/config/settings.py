import os
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
dot_env = os.path.join(BASE_DIR, '.env')


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=dot_env,
        env_file_encoding='utf-8',
        extra='ignore',
    )


class AppSettings(EnvSettings):
    DEBUG: bool = False
    CORS_ORIGIN: List[str] = ['*']
    BACK_URL: str
    FRONT_URL: str


class DatabaseSettings(EnvSettings):
    POSTGRES_DB: str
    POSTGRES_NAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    POSTGRES_TEST_DB: str
    POSTGRES_TEST_NAME: str
    POSTGRES_TEST_PASSWORD: str
    POSTGRES_TEST_HOST: str
    POSTGRES_TEST_PORT: str

    @property
    def database_url(self):
        """URL базы данных"""
        return (f'postgresql+asyncpg://{self.POSTGRES_NAME}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:'
                f'{self.POSTGRES_PORT}/{self.POSTGRES_DB}')

    @property
    def test_database_url(self):
        """URL тестовой базы данных"""
        return (
            f'postgresql+asyncpg://{self.POSTGRES_TEST_NAME}:{self.POSTGRES_TEST_PASSWORD}@{self.POSTGRES_TEST_HOST}:'
            f'{self.POSTGRES_TEST_PORT}/{self.POSTGRES_TEST_DB}')

    @property
    def test_sqlite_db_url(self):
        """URL тестовой базы данных SQLite."""
        return 'sqlite+aiosqlite:///:memory:'


class DateTimeSettings(EnvSettings):
    TIME_ZONE: str = 'UTC'
    DATE_FORMAT: str = '%Y-%m-%d'
    TIME_FORMAT: str = '%H:%M'
    SECOND_FORMAT: str = ':%S'

    @property
    def datetime_format(self):
        return f'{self.DATE_FORMAT} {self.TIME_FORMAT}{self.SECOND_FORMAT}'


class Config(EnvSettings):
    app: AppSettings = AppSettings()
    database: DatabaseSettings = DatabaseSettings()
    date_time: DateTimeSettings = DateTimeSettings()


config = Config()
