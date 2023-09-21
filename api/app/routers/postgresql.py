from fastapi import APIRouter, Depends, HTTPException, status
from app.sqlalchemy_models.Todo import Todo
from app.tools.engine_sqlalchemy import get_db_postgresql
from app.schemas.Todo import TodoUpdate, TodoCreate
from app.schemas.Todo import Todo as TodoSchema

from app.tools.sqlalchemy import get_todo_by_id
from app.tools.sqlalchemy import create_todo as create_todo_db
from app.tools.sqlalchemy import get_todos as get_todos_db

import datetime

router = APIRouter(tags=["postgresql"])


@router.get("/")
def get_todos(db=Depends(get_db_postgresql)):
    return get_todos_db(db)


@router.get("/{todo_id}", response_model=TodoSchema)
def get_todo(todo_id: int, db=Depends(get_db_postgresql)):
    todo = get_todo_by_id(db, todo_id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db=Depends(get_db_postgresql)):
    todo = get_todo_by_id(db, todo_id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    session.delete(todo)
    session.commit()


@router.patch("/{todo_id}", status_code=status.HTTP_202_ACCEPTED, response_model=TodoSchema)
def update_todo(todo_id: int, todo: TodoUpdate, db=Depends(get_db_postgresql)):
    todo_db = get_todo_by_id(db, todo_id)
    if todo_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    if todo.title is not None:
        todo_db.title = todo.title
    if todo.finished is not None:
        todo_db.finished = todo.finished
    todo_db.updated_at = datetime.datetime.now()

    session.commit()
    return todo_db


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TodoSchema)
def create_todo(todo: TodoCreate, db=Depends(get_db_postgresql)):
    todo_db = create_todo_db(db, todo.title, todo.finished)
    db.add(todo_db)
    db.commit()
    return todo_db
