"""
Celery application instance.

Any function that could take more than ~1 second, or that calls an
external/unreliable service (scrapers, LLM APIs, PDF parsing), belongs in a
task module here rather than inline in a route handler. Route handlers should
enqueue the task and return a task ID immediately; the frontend polls
`/tasks/{id}` (added when the first real task lands) for status/result.
"""

from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "job_agent",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        # Task modules are registered here as they're added in later phases:
        # "app.workers.scraping_tasks",
        # "app.workers.parsing_tasks",
        # "app.workers.ai_tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)
