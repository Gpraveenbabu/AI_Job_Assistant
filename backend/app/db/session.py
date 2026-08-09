"""
Async SQLAlchemy engine and session management.

We use the async engine/session throughout because nearly every request in
this system is I/O-bound (DB queries, then often an LLM call or an external
API call on top). A sync engine would block a worker thread for the full
duration of each of those calls; async lets FastAPI serve other requests
while waiting.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,  # Recycle dead connections instead of raising on them
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields a request-scoped DB session.

    Using `yield` (rather than `return`) lets us guarantee the session is
    closed after the request finishes, even if an exception is raised partway
    through a route handler.
    """
    async with AsyncSessionLocal() as session:
        yield session
