from typing import AsyncGenerator

import os
import pytest
import pytest_asyncio
from distutils.util import strtobool
from starlette.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from web.app import app
from web.postgres import DATABASE_URL, Base

from .fixtures import *  # noqa


test_client = TestClient(app)


@pytest.fixture
def client() -> TestClient:
    return test_client


@pytest_asyncio.fixture()
async def db_engine() -> AsyncEngine:
    yield create_async_engine(DATABASE_URL, echo=True)


@pytest_asyncio.fixture(autouse=True)
async def db(db_engine: AsyncEngine) -> None:
    reuse = strtobool(os.getenv("REUSE_DB", "true"))
    if not reuse:
        async with db_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture
async def session(db_engine: AsyncEngine) -> AsyncGenerator:
    async_session = sessionmaker(
        db_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(autouse=True, scope="function")
async def clear_db(session: AsyncGenerator) -> None:
    yield
    await session.rollback()  # rollback all ongoing actions
    for table in reversed(Base.metadata.sorted_tables):
        await session.execute(table.delete())
    await session.commit()
