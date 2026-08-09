"""
Aggregates every endpoint module's router into one v1 API router.

main.py only needs to know about this single router, not about every
individual endpoint module — new endpoint files just register themselves
here, one line each.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import health

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])

# Registered in later phases:
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
# api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
# api_router.include_router(matching.router, prefix="/matching", tags=["matching"])
# api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
# api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
