from typing import Any, Callable

import logging
import os
import pickle
import aioredis
import functools

from web.settings import REDIS_HOST, REDIS_DATABASE_INDEX


logger = logging.getLogger("uvicorn.error")


REDIS_URL = f"redis://{REDIS_HOST}/{REDIS_DATABASE_INDEX}"


class RedisClient:
    def __init__(self) -> None:
        self.connection = aioredis.from_url(
            REDIS_URL,  # username=REDIS_USERNAME, password=REDIS_PASSWORD,
        )

    async def set(
        self, key: str, value: Any, *, ttl_minutes: int | None = None
    ) -> None:
        value = pickle.dumps(value)
        logger.info(f"Put {key} data to cache with ttl={ttl_minutes}")
        if ttl_minutes:
            ttl_seconds = ttl_minutes * 60
            await self.connection.set(key, value, ex=ttl_seconds)
        else:
            await self.connection.set(key, value)

    async def get(self, key: str) -> Any:
        data = await self.connection.get(key)
        if not data:
            return None
        logger.info(f"Took {key} from cache")
        return pickle.loads(data)


redis = RedisClient()


def cacher(key_name: str, ttl_minutes: int | None = None) -> Callable:
    def decorator_cacher(func):
        @functools.wraps(func)
        async def wrapper_cacher(*args, **kwargs):
            data = await redis.get(key_name)
            if data:
                return data
            value = await func(*args, **kwargs)
            await redis.set(key_name, value, ttl_minutes=ttl_minutes)
            return value

        return wrapper_cacher

    return decorator_cacher
