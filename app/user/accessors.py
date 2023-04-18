from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.forms import UserCreateForm
from app.user.models import User
from app.session.accessors import session_accessor


class UserAccessor:
    async def get_by_name(self, db_session: AsyncSession, name: str) -> User:
        res = await db_session.execute(select(User).where(User.name == name))
        return res.scalar()

    async def get_by_id(self, db_session: AsyncSession, user_id: int) -> User:
        res = await db_session.execute(select(User).where(User.id == user_id))
        return res.scalar()

    async def get_by_cookie(
        self, db_session: AsyncSession, cookie: str | None
    ) -> User | None:
        if not cookie:
            return None
        user_session = await session_accessor.get(db_session, cookie)
        if not user_session:
            return None
        res = await db_session.execute(
            select(User).where(User.id == user_session.user)
        )
        return res.scalar()

    async def create(
        self, db_session: AsyncSession, data: UserCreateForm
    ) -> User:
        try:
            new_user = User(**data.dict())
            db_session.add(new_user)
            await db_session.commit()

            await db_session.refresh(new_user)
            return new_user
        except IntegrityError as exc:
            raise exc


user_accessor = UserAccessor()
