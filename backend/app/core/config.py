"""
Centralized, typed application settings.

Every config value the app needs is declared here exactly once. This is the
single source of truth for environment configuration — no `os.getenv()` calls
should appear anywhere else in the codebase. That keeps configuration
discoverable (read this one file to know every setting the app needs) and
validated at startup (pydantic will fail fast if a required value is missing
or malformed, rather than surfacing a cryptic error deep in a request).
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # --- App ---
    app_name: str = "AI Job Application Agent"
    environment: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"

    # --- Security ---
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # --- Database ---
    database_url: str

    # --- Redis / Celery ---
    redis_url: str
    celery_broker_url: str
    celery_result_backend: str

    # --- AI providers ---
    openai_api_key: str = ""

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings accessor.

    FastAPI's dependency-injection system will call this once and reuse the
    same Settings instance across the app's lifetime (lru_cache makes this a
    singleton), rather than re-parsing environment variables on every request.
    """
    return Settings()
