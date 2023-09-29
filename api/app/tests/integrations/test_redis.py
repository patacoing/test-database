import pytest
from fastapi import status
from app.sqlalchemy_models.Todo import Todo


@pytest.mark.redis
def test_get_not_found(Client):
    response = Client.get("/redis?key=1")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.redis
def test_get(Client, redis_client):
    redis_client.setKey("1", "test")
    response = Client.get("/redis?key=1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["value"] == "test"


@pytest.mark.redis
def test_get_todo_not_found(ClientMysql):
    response = ClientMysql.get("/redis/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.redis
def test_get_todo_not_from_cache(ClientMysql, redis_client, test_mysql):
    todo = Todo(title="test")
    test_mysql.add(todo)
    test_mysql.commit()

    print(test_mysql.query(Todo).all())
    response = ClientMysql.get("/redis/1")
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["value"] == "test"


@pytest.mark.redis
def test_get_todo_from_cache(ClientMysql, redis_client, test_mysql):
    todo = Todo(title="test")
    test_mysql.add(todo)
    test_mysql.commit()

    redis_client.setKey("1", "test")

    response = ClientMysql.get("/redis/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["value"] == "test"
