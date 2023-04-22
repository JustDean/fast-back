import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.models import User


@pytest.fixture
def user_password() -> str:
    return "TestPass123"


@pytest_asyncio.fixture
async def user(session: AsyncSession, user_password: str) -> User:
    new_user = User(name="TestUser", password=user_password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
