from fastapi import FastAPI
from uvicorn import run
from app.settings import settings
from app.tools.engine_sqlalchemy import Base, engine_mysql, engine_postgresql
from app.sqlalchemy_models.Todo import Todo

import argparse

from app.routers.mysql import router as mysql_router
from app.routers.postgresql import router as postgresql_router
from app.routers.redis import router as redis_router
# If we want to auto build the tables we have to import the table models and then run the Base.metadat.create_all function

app = FastAPI()

app.include_router(mysql_router, prefix="/mysql")
app.include_router(postgresql_router, prefix="/postgresql")
app.include_router(redis_router, prefix="/redis")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-mysql", action="store_true")
    parser.add_argument("--build-postgresql", action="store_true")

    args = parser.parse_args()
    if args.build_mysql:
        Base.metadata.create_all(bind=engine_mysql)
    if args.build_postgresql:
        Base.metadata.create_all(bind=engine_postgresql)
