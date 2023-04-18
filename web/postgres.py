import logging
import os
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


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


engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()


async def get_session() -> AsyncGenerator:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

class BaseModel(Base):
    __abstract__ = True

    def to_dict(self) -> dict[str, Any]:
        return NotImplementedError