from pydantic_settings import BaseSettings
import os
from pydantic import BaseModel


class Base(BaseSettings):
    class Config:
        env_file = ".env"


class MysqlSettings(Base):
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str


class PostgresqlSettings(Base):
    POSTGRESQL_HOST: str
    POSTGRESQL_PORT: int
    POSTGRESQL_USER: str
    POSTGRESQL_PASSWORD: str
    POSTGRESQL_DATABASE: str


class Settings(MysqlSettings, PostgresqlSettings):
    pass


settings = Settings()
