from fastapi import status
from app.sqlalchemy_models.Todo import Todo
import pytest


@pytest.mark.postgresql
def test_get_todos(ClientPostgresql):
    response = ClientPostgresql.get("/postgresql")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.postgresql
def test_get_todo_not_found(ClientPostgresql):
    response = ClientPostgresql.get("/postgresql/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.postgresql
def test_get_todo(ClientPostgresql, test_postgresql):
    todo = Todo(title="test")
    test_postgresql.add(todo)
    test_postgresql.commit()
    response = ClientPostgresql.get(f"/postgresql/{todo.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == todo.id


@pytest.mark.postgresql
def test_create_todo(ClientPostgresql, test_postgresql):
    response = ClientPostgresql.post("/postgresql/", json={"title": "test"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == "test"
    id = response.json()["id"]
    assert test_postgresql.query(Todo).filter(
        Todo.id == id).first() is not None


@pytest.mark.postgresql
def test_delete_not_found_todo(ClientPostgresql, test_postgresql):
    response = ClientPostgresql.delete("/postgresql/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.postgresql
def test_delete_todo(ClientPostgresql, test_postgresql):
    todo = Todo(title="test")
    test_postgresql.add(todo)
    test_postgresql.commit()
    response = ClientPostgresql.delete(f"/postgresql/{todo.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert test_postgresql.query(Todo).filter(
        Todo.id == todo.id).first() is None


@pytest.mark.postgresql
def test_update_todo_not_found(ClientPostgresql):
    response = ClientPostgresql.patch("/postgresql/1", json={"title": "test"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.postgresql
def test_update_todo(ClientPostgresql, test_postgresql):
    todo = Todo(title="test")
    test_postgresql.add(todo)
    test_postgresql.commit()
    response = ClientPostgresql.patch(
        f"/postgresql/{todo.id}", json={"title": "test2"})
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json()["title"] == "test2"
    test_postgresql.commit()
    assert test_postgresql.query(Todo).filter(
        Todo.id == todo.id).first().title == "test2"
