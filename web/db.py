import functools
from typing import Any, Callable

import logging
import os
import pickle
from typing import AsyncGenerator
import aioredis

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


logger = logging.getLogger("uvicorn.error")


DATABASE_HOST = os.environ.get("DATABASE_HOST", "127.0.0.1")
DATABASE_PORT = os.environ.get("DATABASE_PORT", 5432)
DATABASE_USER = os.environ.get("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "postgres")
DATABASE_TABLE = os.environ.get("DATABASE_TABLE", "test")

DATABASE_URL = (
    f"postgresql+asyncpg://{DATABASE_USER}"
    f":{DATABASE_PASSWORD}@{DATABASE_HOST}"
    f":{DATABASE_PORT}/{DATABASE_TABLE}"
)

REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_DATABASE_INDEX = os.environ.get("REDIS_DATABASE_INDEX", 7)
REDIS_USERNAME = os.environ.get("REDIS_USERNAME", "user")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "password")

REDIS_URL = f"redis://{REDIS_HOST}/{REDIS_DATABASE_INDEX}"

engine = create_async_engine(DATABASE_URL, echo=True)


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


async def get_session() -> AsyncGenerator:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
