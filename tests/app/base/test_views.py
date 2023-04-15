from starlette.testclient import TestClient


class TestPing:
    ENDPOINT = "/ping"

    def test_success(self, client: TestClient) -> None:
        resp = client.get(self.ENDPOINT)
        assert resp.status_code == 200
        assert resp.json() == {"ping": "pong"}
