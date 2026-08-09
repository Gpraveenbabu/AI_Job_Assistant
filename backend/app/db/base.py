"""
Shared declarative base for all ORM models.

Every model in app/models/ inherits from this Base. Alembic's env.py imports
this Base (plus every model module, so they register themselves on it) to
autogenerate migrations by diffing the ORM metadata against the live schema.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
