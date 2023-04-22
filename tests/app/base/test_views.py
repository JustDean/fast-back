import pytest
from httpx import AsyncClient


class TestPing:
    ENDPOINT = "/ping"

    @pytest.mark.asyncio
    async def test_success(self, client: AsyncClient) -> None:
        resp = await client.get(self.ENDPOINT)
        assert resp.status_code == 200
        assert resp.json() == {"ping": "pong"}
