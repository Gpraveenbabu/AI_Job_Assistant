"""
Shared dependencies for v1 API routes.

Centralizing dependencies here means every endpoint module imports the same
`DbSession` / `CurrentUser` types rather than each redefining its own copy —
one place to change if, say, we swap how the DB session or auth token is
resolved.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

DbSession = Annotated[AsyncSession, Depends(get_db)]

# CurrentUser dependency is added in the Authentication phase (Phase 3).
# Placeholder left here intentionally so endpoint signatures written now
# don't need to change shape later — only this dependency's implementation does.
