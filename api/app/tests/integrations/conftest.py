from app.routers.mysql import router
import pytest
from fastapi.testclient import TestClient
from main import app
from app.settings import settings
from sqlalchemy.pool import StaticPool
from app.sqlalchemy_models.Todo import Todo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.tools.engine_sqlalchemy import Base, get_db_mysql, get_db_postgresql
from app.tools.redis import redis_client as redis_client_db
from app.tools.redis import get_redis_client


engine_mysql = create_engine(
    f"mysql+mysqlconnector://{settings.MYSQL_TEST_USER}:{settings.MYSQL_TEST_PASSWORD}@{settings.MYSQL_TEST_HOST}:{settings.MYSQL_TEST_PORT}/{settings.MYSQL_TEST_DATABASE}",
    poolclass=StaticPool,
)
engine_postgresql = create_engine(
    f"postgresql+psycopg2://{settings.POSTGRESQL_TEST_USER}:{settings.POSTGRESQL_TEST_PASSWORD}@{settings.POSTGRESQL_TEST_HOST}:{settings.POSTGRESQL_TEST_PORT}/{settings.POSTGRESQL_TEST_DATABASE}",
    poolclass=StaticPool,
)
TestingSessionLocalMysql = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_mysql)
TestingSessionLocalPostgresql = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_postgresql)


def override_get_db_mysql():
    try:
        db = TestingSessionLocalMysql()
        yield db
    finally:
        db.close()


def override_get_db_postgresql():
    try:
        db = TestingSessionLocalPostgresql()
        yield db
    finally:
        db.close()


@pytest.fixture
def test_mysql():
    try:
        db = TestingSessionLocalMysql()
        yield db
    finally:
        db.close()


@pytest.fixture
def test_postgresql():
    try:
        db = TestingSessionLocalPostgresql()
        yield db
    finally:
        db.close()


@pytest.fixture
def db_mysql():
    Base.metadata.create_all(bind=engine_mysql)
    yield
    Base.metadata.drop_all(bind=engine_mysql)


@pytest.fixture
def db_postgresql():
    Base.metadata.create_all(bind=engine_postgresql)
    yield
    Base.metadata.drop_all(bind=engine_postgresql)


@pytest.fixture
def redis_client():
    yield redis_client_db
    redis_client_db.client.flushall()


@pytest.fixture
def Client(redis_client):
    return TestClient(app)


@pytest.fixture
def ClientMysql(db_mysql, redis_client):
    app.dependency_overrides[get_redis_client] = lambda: redis_client_db
    app.dependency_overrides[get_db_mysql] = override_get_db_mysql
    return TestClient(app)


@pytest.fixture
def ClientPostgresql(db_postgresql):
    app.dependency_overrides[get_db_postgresql] = override_get_db_postgresql
    return TestClient(app)
