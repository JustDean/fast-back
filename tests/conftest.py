from distutils.util import strtobool
import os
from typing import AsyncGenerator
import pytest
import pytest_asyncio
from sqlmodel import SQLModel
from starlette.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from web.settings import app
from web.db import engine

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
            await conn.run_sync(SQLModel.metadata.drop_all)
            await conn.run_sync(SQLModel.metadata.create_all)
    return None


@pytest_asyncio.fixture
async def session() -> AsyncGenerator:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
        for table in reversed(SQLModel.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()
