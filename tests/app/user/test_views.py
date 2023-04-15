import pytest
from starlette.testclient import TestClient

from app.user.accessors import user_accessor
from app.user.models import User


class TestUserSignup:
    ENDPOINT = "user/signup"

    @pytest.mark.asyncio
    async def test_success(self, client: TestClient, session, user: User) -> None:
        username = "TestUser"
        password = "aboba"
        payload = {"name": username, "password": password}
        resp = client.post(self.ENDPOINT, json=payload)
        assert resp.status_code == 200

        retrieved_user = await user_accessor.get_by_name(session, username)
        assert retrieved_user.name == username
        assert retrieved_user.compare_passwords(password)
