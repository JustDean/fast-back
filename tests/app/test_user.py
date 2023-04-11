from starlette.testclient import TestClient

from app.user.models import User
from tests.serializers.user import serialize_user


class TestUserList:
    ENDPOINT = "/user"

    def test_success(self, client: TestClient, user: User) -> None:
        resp = client.get(self.ENDPOINT)
        assert resp.status_code == 200
        assert resp.json() == [serialize_user(user)]
