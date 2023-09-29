from fastapi import APIRouter, Depends, HTTPException, status
from app.tools.redis import get_redis_client
from app.schemas.Todo import Todo
from app.tools.engine_sqlalchemy import get_db_mysql
from app.tools.sqlalchemy import get_todo_by_id as get_todo_by_id_sqlalchemy
from json import loads

router = APIRouter(tags=["redis"])


@router.get("/", response_model=dict, status_code=status.HTTP_200_OK)
async def get_redis_value(key: str, redis_client=Depends(get_redis_client)):
    value = redis_client.getValue(key)
    if value is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Key not found"
        )
    return {"key": key, "value": value}


@router.post("/", response_model=dict, status_code=status.HTTP_200_OK)
async def set_redis_value(key: str, value: str, expiration: int = None, redis_client=Depends(get_redis_client)):
    result = redis_client.setKey(key, value, expiration)
    if result is False:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to set key"
        )
    return {"key": key, "value": value}


@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(todo_id: int, redis_client=Depends(get_redis_client), db=Depends(get_db_mysql)):
    value = redis_client.getValue(todo_id)
    if value is None:
        todo = get_todo_by_id_sqlalchemy(id=todo_id, db=db)
        if todo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found"
            )
        redis_client.setKey(todo_id, str(todo.to_json()), expiration=5)
        return todo
    else:
        value = value.replace("\'", "\"")
        return loads(value)
