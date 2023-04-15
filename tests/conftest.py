import os
import pytest
import pytest_asyncio
from distutils.util import strtobool
from typing import AsyncGenerator
from starlette.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from web.settings import app
from web.postgres import engine, Base

from .fixtures import *  # noqa


test_client = TestClient(app)


@pytest.fixture
def client() -> TestClient:
    return test_client


@pytest_asyncio.fixture(autouse=True)
async def db() -> None:
    reuse = strtobool(os.getenv("REUSE_DB", "true"))
    if not reuse:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture(autouse=True, scope="function")
async def clear_db() -> None:
    yield
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()


@pytest_asyncio.fixture
async def session() -> AsyncGenerator:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
