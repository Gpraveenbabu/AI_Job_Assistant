"""
Integration test for /health.

This is deliberately the first test in the repo: if this passes, it proves
the FastAPI app boots, routing is wired correctly, and the app can reach
both Postgres and Redis — i.e. the entire Phase 1 skeleton actually works
end to end, not just that individual files import without error.
"""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_health_check_returns_ok() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health")

    assert response.status_code == 200
    body = response.json()
    assert body["api"] == "ok"
    assert body["database"] == "ok"
    assert body["redis"] == "ok"
