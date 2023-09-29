from pydantic_settings import BaseSettings
import os
from pydantic import BaseModel


class Base(BaseSettings):
    class Config:
        env_file = os.path.abspath(".env")


class MysqlSettings(Base):
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str

    MYSQL_TEST_HOST: str
    MYSQL_TEST_PORT: int
    MYSQL_TEST_USER: str
    MYSQL_TEST_PASSWORD: str
    MYSQL_TEST_DATABASE: str


class PostgresqlSettings(Base):
    POSTGRESQL_HOST: str
    POSTGRESQL_PORT: int
    POSTGRESQL_USER: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_DATABASE: str

    POSTGRESQL_TEST_HOST: str
    POSTGRESQL_TEST_PORT: int
    POSTGRESQL_TEST_USER: str
    POSTGRESQL_TEST_PASSWORD: str
    POSTGRESQL_TEST_DATABASE: str


class RedisSettings(Base):
    REDIS_HOST: str
    REDIS_PORT: int


class Settings(MysqlSettings, PostgresqlSettings, RedisSettings):
    pass


settings = Settings()
