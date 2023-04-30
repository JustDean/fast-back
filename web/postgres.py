import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from web.settings import (
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_TABLE,
)


logger = logging.getLogger("uvicorn.error")


DATABASE_URL = (
    f"postgresql+asyncpg://{DATABASE_USER}"
    f":{DATABASE_PASSWORD}@{DATABASE_HOST}"
    f":{DATABASE_PORT}/{DATABASE_TABLE}"
)

engine = create_async_engine(DATABASE_URL, echo=True)


async def get_session() -> AsyncSession:  # type: ignore
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    def to_dict(self) -> dict:
        return {
            k: v
            for k, v in self.__dict__.items()
            if not k.startswith(("_", "__"))
        }
