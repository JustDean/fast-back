import pytest_asyncio
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from app.session.models import Session
from app.user.models import User


@pytest_asyncio.fixture
async def user_session(session: AsyncSession, user: User) -> User:
    session_id = uuid4().hex
    new_session = Session(id=session_id, user=user.id)
    session.add(new_session)
    await session.commit()

    return new_session
