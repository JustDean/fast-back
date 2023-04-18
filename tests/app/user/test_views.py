import pytest
from starlette.testclient import TestClient

from app.user.accessors import user_accessor


@pytest.mark.asyncio
class TestUserSignup:
    ENDPOINT = "user/signup"

    async def test_success(self, client: TestClient, session) -> None:
        username = "TestUser"
        password = "aboba"
        payload = {"name": username, "password": password}
        resp = client.post(self.ENDPOINT, json=payload)
        assert resp.status_code == 200

        retrieved_user = await user_accessor.get_by_name(session, username)
        assert retrieved_user.name == username
        assert retrieved_user.compare_passwords(password)
