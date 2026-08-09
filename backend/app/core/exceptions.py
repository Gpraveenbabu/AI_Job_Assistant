"""
Application-level exceptions and their FastAPI handlers.

Services and repositories raise these domain exceptions instead of HTTPException
directly. This keeps the business-logic layer framework-agnostic (a service
shouldn't need to know it's being called from a web request — it might later
be called from a Celery task or a CLI script) while still producing clean,
consistent HTTP responses at the API boundary.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base class for all domain-level errors raised by services/repositories."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "An unexpected error occurred."

    def __init__(self, detail: str | None = None) -> None:
        if detail:
            self.detail = detail
        super().__init__(self.detail)


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Resource not found."


class AlreadyExistsError(AppError):
    status_code = status.HTTP_409_CONFLICT
    detail = "Resource already exists."


class UnauthorizedError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Not authenticated."


class ForbiddenError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Not authorized to perform this action."


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
