from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.forms import UserCreateForm
from app.user.models import User


class UserAccessor:
    async def get_by_name(self, session: AsyncSession, name: str) -> User:
        res = await session.execute(select(User).where(User.name == name))
        return res.scalar()  # type: ignore

    async def get_by_id(self, session: AsyncSession, user_id: int) -> User:
        res = await session.execute(select(User).where(User.id == user_id))
        return res.scalar()  # type: ignore

    async def create(
        self, session: AsyncSession, data: UserCreateForm
    ) -> User:
        try:
            new_user = User(**data.dict())
            session.add(new_user)
            await session.commit()

            await session.refresh(new_user)
            return new_user
        except IntegrityError as exc:
            raise exc


user_accessor = UserAccessor()
