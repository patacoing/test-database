from pydantic import BaseModel
from datetime import datetime


class TodoBase(BaseModel):
    title: str
    finished: bool = False


class Todo(BaseModel):
    id: int
    title: str
    finished: bool
    created_at: datetime
    updated_at: datetime


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: str = None
    finished: bool = None
