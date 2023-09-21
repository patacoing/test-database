from sqlalchemy.orm import Session
from app.sqlalchemy_models.Todo import Todo
from typing import List


def get_todo_by_id(id: int, db: Session) -> Todo:
    return db.query(Todo).filter(Todo.id == id).first()


def get_todos(db: Session) -> List[Todo]:
    return db.query(Todo).all()


def create_todo(db: Session, title: str, finished: bool) -> Todo:
    return Todo(
        title=title,
        finished=finished
    )
