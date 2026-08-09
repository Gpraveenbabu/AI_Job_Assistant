"""
Health check endpoint.

Checks real connectivity to Postgres and Redis rather than just returning
200 unconditionally — a health check that can't fail is not actually
checking anything. This is what a load balancer / orchestrator (k8s,
docker-compose healthcheck, etc.) should poll.
"""

from fastapi import APIRouter
from redis.asyncio import from_url
from sqlalchemy import text

from app.api.v1.deps import DbSession
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()


@router.get("/health")
async def health_check(db: DbSession) -> dict:
    status_report = {"api": "ok", "database": "unknown", "redis": "unknown"}

    try:
        await db.execute(text("SELECT 1"))
        status_report["database"] = "ok"
    except Exception as exc:  # noqa: BLE001 - deliberately broad for a health probe
        status_report["database"] = f"error: {exc}"

    try:
        redis_client = from_url(settings.redis_url)
        await redis_client.ping()
        await redis_client.aclose()
        status_report["redis"] = "ok"
    except Exception as exc:  # noqa: BLE001
        status_report["redis"] = f"error: {exc}"

    return status_report
