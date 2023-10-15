from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.settings import settings

engine_mysql = create_engine(
    f"mysql+mysqlconnector://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}",
    echo=False,
)

engine_postgresql = create_engine(
    f"postgresql+psycopg2://{settings.POSTGRESQL_USER}:{settings.POSTGRESQL_PASSWORD}@{settings.POSTGRESQL_HOST}:{settings.POSTGRESQL_PORT}/{settings.POSTGRESQL_DATABASE}",
    echo=False,
)


Base = declarative_base()
SessionMysql = sessionmaker(bind=engine_mysql)
SessionPostgresql = sessionmaker(bind=engine_postgresql)


def get_db_mysql():
    try:
        db = SessionMysql()
        yield db
    finally:
        db.close()


def get_db_postgresql():
    try:
        db = SessionPostgresql()
        yield db
    finally:
        db.close()
