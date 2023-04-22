import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.accessors import user_accessor
from app.user.forms import UserCreateForm
from app.user.models import User


@pytest.mark.asyncio
class TestUserAccessorGetByName:
    async def test_not_found(self, session: AsyncSession) -> None:
        res = await user_accessor.get_by_name(session, "Unavailable name")
        assert res is None

    async def test_success(self, session: AsyncSession, user: User) -> None:
        res = await user_accessor.get_by_name(session, user.name)
        assert res == user


@pytest.mark.asyncio
class TestUserAccessorGetById:
    async def test_not_found(self, session: AsyncSession) -> None:
        res = await user_accessor.get_by_id(session, 1)
        assert res is None

    async def test_success(self, session: AsyncSession, user: User) -> None:
        res = await user_accessor.get_by_id(session, user.id)
        assert res == user


@pytest.mark.asyncio
class TestUserAccessorCreate:
    async def test_success(self, session: AsyncSession) -> None:
        user_name = "Aboba"
        user_password = "123"
        user_data = UserCreateForm(name=user_name, password=user_password)
        res = await user_accessor.create(session, user_data)

        retrieved_user: User = (
            await session.execute(select(User).where(User.id == res.id))
        ).scalar()
        assert retrieved_user.name == user_name
        assert retrieved_user.password != user_password  # password is hashed
        assert retrieved_user.compare_passwords(user_password)
