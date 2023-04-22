from httpx import AsyncClient
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.session.models import Session

from app.user.models import User
from tests.converters.user import user_to_dict


@pytest.mark.asyncio
class TestUserSignup:
    ENDPOINT = "user/signup"

    async def test_name_is_unavailable(
        self, client: AsyncClient, session: AsyncSession, user: User
    ) -> None:
        payload = {"name": user.name, "password": "TestPass123"}
        resp = await client.post(self.ENDPOINT, json=payload)
        assert resp.status_code == 400
        assert resp.json() == {"detail": "User with this name already exists"}

    async def test_success(
        self, client: AsyncClient, session: AsyncSession
    ) -> None:
        username = "TestUser"
        password = "aboba"
        payload = {"name": username, "password": password}
        resp = await client.post(self.ENDPOINT, json=payload)
        assert resp.status_code == 200

        retrieved_user: User = (
            await session.execute(select(User).where(User.name == username))
        ).scalar()
        assert retrieved_user.name == username
        assert retrieved_user.compare_passwords(password)


@pytest.mark.asyncio
class TestUserLogin:
    ENDPOINT = "user/login"

    async def test_user_does_not_exist(
        self, client: AsyncClient, session: AsyncSession
    ) -> None:
        payload = {"name": "Test", "password": "TestPass123"}
        resp = await client.post(self.ENDPOINT, json=payload)
        assert resp.status_code == 400
        assert resp.json() == {"detail": "Incorrect user data"}

    async def test_invalid_password(
        self, client: AsyncClient, session: AsyncSession, user: User
    ) -> None:
        payload = {"name": user.name, "password": "InvalidPassword"}
        resp = await client.post(self.ENDPOINT, json=payload)
        assert resp.status_code == 400
        assert resp.json() == {"detail": "Incorrect user data"}

    async def test_success(
        self,
        client: AsyncClient,
        session: AsyncSession,
        user: User,
        user_password: str,
    ) -> None:
        payload = {"name": user.name, "password": user_password}
        resp = await client.post(self.ENDPOINT, json=payload)
        assert resp.status_code == 200
        session_id = resp.cookies.get("sessionid")
        assert session_id is not None
        assert resp.json() == user_to_dict(user)
        assert (
            await session.execute(
                select(Session.id).where(Session.id == session_id)
            )
        ).scalar() == session_id


@pytest.mark.asyncio
class TestUserLogout:
    ENDPOINT = "user/logout"

    async def test_no_cookie_provided(self, client: AsyncClient) -> None:
        resp = await client.post(self.ENDPOINT)
        assert resp.status_code == 401
        assert resp.json() == {"detail": "Unauthorized"}

    async def test_invalid_sessionid(self, client: AsyncClient) -> None:
        resp = await client.post(
            self.ENDPOINT, cookies={"sessionid": "sessionidid"}
        )
        assert resp.status_code == 200
        assert resp.json() is None

    async def test_success(
        self, client: AsyncClient, session: AsyncSession, user_session: Session
    ) -> None:
        resp = await client.post(
            self.ENDPOINT, cookies={"sessionid": user_session.id}
        )
        assert resp.status_code == 200
        assert resp.json() is None
        assert (
            await session.execute(
                select(Session).where(Session.id == user_session.id)
            )
        ).scalar() is None


@pytest.mark.asyncio
class TestUserCurrent:
    ENDPOINT = "user/current"

    async def test_not_authed(self, client: AsyncClient) -> None:
        resp = await client.get(self.ENDPOINT)
        assert resp.status_code == 401
        assert resp.json() == {"detail": "Unauthorized"}

    async def test_invalid_sessionid(self, client: AsyncClient) -> None:
        resp = await client.get(
            self.ENDPOINT, cookies={"sessionid": "sessionidid"}
        )
        assert resp.status_code == 401
        assert resp.json() == {"detail": "Unauthorized"}

    async def test_success(
        self,
        client: AsyncClient,
        session: AsyncSession,
        user: User,
        user_session: Session,
    ) -> None:
        resp = await client.get(
            self.ENDPOINT, cookies={"sessionid": user_session.id}
        )
        assert resp.status_code == 200
        assert resp.json() == user_to_dict(user)
