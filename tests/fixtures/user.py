import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.models import User


@pytest_asyncio.fixture
async def user(session: AsyncSession) -> User:
    new_user = User(name="Zupa", password="Lupa")
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    yield new_user
