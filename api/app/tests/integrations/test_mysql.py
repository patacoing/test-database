from fastapi import status
from app.sqlalchemy_models.Todo import Todo
import pytest


@pytest.mark.mysql
def test_get_todos(ClientMysql):
    response = ClientMysql.get("/mysql")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.mysql
def test_get_todo_not_found(ClientMysql):
    response = ClientMysql.get("/mysql/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.mysql
def test_get_todo(ClientMysql, test_mysql):
    todo = Todo(title="test")
    test_mysql.add(todo)
    test_mysql.commit()
    response = ClientMysql.get(f"/mysql/{todo.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == todo.id


@pytest.mark.mysql
def test_create_todo(ClientMysql, test_mysql):
    response = ClientMysql.post("/mysql/", json={"title": "test"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == "test"
    id = response.json()["id"]
    assert test_mysql.query(Todo).filter(Todo.id == id).first() is not None


@pytest.mark.mysql
def test_delete_not_found_todo(ClientMysql, test_mysql):
    response = ClientMysql.delete("/mysql/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.mysql
def test_delete_todo(ClientMysql, test_mysql):
    todo = Todo(title="test")
    test_mysql.add(todo)
    test_mysql.commit()
    response = ClientMysql.delete(f"/mysql/{todo.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert test_mysql.query(Todo).filter(Todo.id == todo.id).first() is None


@pytest.mark.mysql
def test_update_todo_not_found(ClientMysql):
    response = ClientMysql.patch("/mysql/1", json={"title": "test"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.mysql
def test_update_todo(ClientMysql, test_mysql):
    todo = Todo(title="test")
    test_mysql.add(todo)
    test_mysql.commit()
    response = ClientMysql.patch(f"/mysql/{todo.id}", json={"title": "test2"})
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json()["title"] == "test2"
    test_mysql.commit()
    assert test_mysql.query(Todo).filter(
        Todo.id == todo.id).first().title == "test2"
