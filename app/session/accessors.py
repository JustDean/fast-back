from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from sqlalchemy import select

from app.session.models import Session
from app.user.models import User


class SessionAccessor:
    async def create(self, db_session: AsyncSession, user: User) -> Session:
        try:
            session_id = uuid4().hex
            new_session = Session(id=session_id, user=user.id)
            db_session.add(new_session)
            await db_session.commit()

            return new_session
        except IntegrityError as exc:
            raise exc

    async def get(self, db_session: AsyncSession, session_id: str) -> Session:
        res = await db_session.execute(
            select(Session).where(Session.id == session_id)
        )
        return res.scalar()

    async def delete(self, db_session: AsyncSession, session_id: str) -> str:
        results = await db_session.execute(
            select(Session).where(Session.id == session_id)
        )
        the_session = results.scalar()
        await db_session.delete(the_session)
        await db_session.commit()

        return session_id


session_accessor = SessionAccessor()
