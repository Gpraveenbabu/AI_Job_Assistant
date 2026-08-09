"""
Shared pytest fixtures and configuration.

Kept minimal for Phase 1 — grows as the DB/auth layers land, at which point
this is where we'll add a fixture that spins up a transactional test session
(so each test runs in a rolled-back transaction and never pollutes real data).
"""

import pytest


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "asyncio: mark test as async")
