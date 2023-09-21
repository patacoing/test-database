from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.settings import settings

engine = create_engine(
    f"mysql+mysqlconnector://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}",
    echo=False)


Base = declarative_base()
Session = sessionmaker(bind=engine)


def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()
