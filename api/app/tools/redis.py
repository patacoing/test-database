from redis import Redis as RedisClient
from app.settings import settings
from typing import Optional


class Redis:
    def __init__(self, host, port, decode_responses):
        self.client = RedisClient(
            host=host, port=port, decode_responses=decode_responses
        )

    def getValue(self, key):
        """
        Method to get a value from redis
        :param key: key to get
        :return: value
        """
        return self.client.get(key)

    def setKey(self, key, value, expiration=None) -> Optional[bool]:
        """
        Method to set a key value pair in redis
        :param key: key to set
        :param value: value to set
        :param expiration: expiration time in seconds
        :return: True if success else False
        """
        return self.client.set(key, value, ex=expiration)


redis_client = Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True
)


def get_redis_client():
    yield redis_client
