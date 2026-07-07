import pytest
from httpx import ASGITransport, AsyncClient
from src.main import app


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("/health", {"status": "ok"}),
        ("/ready", {"status": "ready"}),
    ],
)
async def test_probe(path: str, expected: dict[str, str]) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(path)
    assert response.status_code == 200
    assert response.json() == expected
