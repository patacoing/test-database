from sqlalchemy.orm import Session


def get_todo_by_id(id: int, db: Session) -> Todo:
    return db.query(Todo).filter(Todo.id == id).first()


def get_todos(db: Session) -> list[Todo]:
    return db.query(Todo).all()


def create_todo(db: Session, title: str, finished: bool) -> Todo:
    return Todo(
        title=title,
        finished=finished
    )
