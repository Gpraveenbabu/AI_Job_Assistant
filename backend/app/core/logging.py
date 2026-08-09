"""
Structured logging setup.

We configure logging once at startup via `setup_logging()`, called from the
FastAPI lifespan handler in main.py. Using JSON-ish structured fields (rather
than bare print statements) means logs are actually queryable once this ships
behind something like CloudWatch or Loki.
"""

import logging
import sys

from app.core.config import get_settings


def setup_logging() -> None:
    settings = get_settings()
    level = logging.DEBUG if settings.debug else logging.INFO

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers = [handler]

    # Quiet down noisy third-party loggers unless we're actively debugging them
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING if not settings.debug else logging.INFO)
