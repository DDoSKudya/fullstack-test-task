from httpx import AsyncClient


async def test_health(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_ready(client: AsyncClient) -> None:
    response = await client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready", "database": "ok"}


async def test_request_id_header(client: AsyncClient) -> None:
    response = await client.get("/health", headers={"X-Request-ID": "test-req-1"})
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "test-req-1"
