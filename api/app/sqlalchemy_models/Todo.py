from app.tools.engine_sqlalchemy import Base
from sqlalchemy import Column, Integer, DateTime, Boolean, String
import datetime


class Todo(Base):
    __tablename__ = "todos"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String(255))
    finished: bool = Column(Boolean, default=False)
    created_at: DateTime = Column(DateTime, default=datetime.datetime.now)
    updated_at: DateTime = Column(DateTime, default=datetime.datetime.now)

    def to_json(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
