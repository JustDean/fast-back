import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.session.accessors import session_accessor
from app.session.models import Session
from app.user.models import User


@pytest.mark.asyncio
class TestSessionAccessorCreate:
    async def test_success(self, session: AsyncSession, user: User) -> None:
        user_session = await session_accessor.create(session, user)
        assert (
            await session.execute(
                select(Session).where(Session.id == user_session.id)
            )
        ).scalar() is not None


@pytest.mark.asyncio
class TestSessionAccessorGet:
    async def test_no_session(self, session: AsyncSession) -> None:
        user_session = await session_accessor.get(session, "1")
        assert user_session is None

    async def test_success(
        self, session: AsyncSession, user_session: Session
    ) -> None:
        user_session = await session_accessor.get(session, user_session.id)
        assert user_session is not None


@pytest.mark.asyncio
class TestSessionAccessorDelete:
    async def test_no_session(self, session: AsyncSession) -> None:
        user_session = await session_accessor.delete(session, "1")
        assert user_session is None

    async def test_success(
        self, session: AsyncSession, user_session: Session
    ) -> None:
        deleted_session = await session_accessor.delete(
            session, user_session.id
        )
        assert deleted_session == user_session.id
        assert (
            await session.execute(
                select(Session).where(Session.id == user_session.id)
            )
        ).scalar() is None
