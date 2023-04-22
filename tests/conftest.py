import os
import asyncio
import pytest_asyncio
import pytest
from httpx import AsyncClient
from distutils.util import strtobool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from web.app import app
from web.postgres import DATABASE_URL, Base

from .fixtures import *  # noqa


@pytest.yield_fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest_asyncio.fixture()
async def db_engine() -> AsyncEngine:  # type: ignore
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
async def session(db_engine: AsyncEngine) -> AsyncSession:
    async_session = sessionmaker(
        db_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(autouse=True, scope="function")
async def clear_db(session: AsyncSession) -> None:
    yield
    await session.rollback()  # rollback all ongoing actions
    for table in reversed(Base.metadata.sorted_tables):
        await session.execute(table.delete())
    await session.commit()
