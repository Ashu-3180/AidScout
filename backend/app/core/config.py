from functools import lru_cache
import os

from pydantic import BaseModel, Field, field_validator
from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError


class DatabaseConfigurationError(RuntimeError):
    """Raised before database access when required configuration is absent."""


class Settings(BaseModel):
    database_url: str | None = None
    expected_database_name: str = Field(default="aidscout_dev", min_length=1, max_length=63)
    database_readiness_timeout_seconds: int = Field(default=3, ge=1, le=30)
    database_readiness_statement_timeout_milliseconds: int = Field(default=3000, ge=100, le=30000)
    verification_freshness_days: int = Field(default=90, ge=1, le=3650)

    @field_validator("database_url", mode="before")
    @classmethod
    def blank_database_url_is_unset(cls, value: object) -> object:
        return None if isinstance(value, str) and not value.strip() else value

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
            database_url=os.getenv("DATABASE_URL"),
            expected_database_name=os.getenv("AIDSCOUT_EXPECTED_DATABASE_NAME", "aidscout_dev"),
            database_readiness_timeout_seconds=os.getenv("DATABASE_READINESS_TIMEOUT_SECONDS", "3"),
            database_readiness_statement_timeout_milliseconds=os.getenv("DATABASE_READINESS_STATEMENT_TIMEOUT_MILLISECONDS", "3000"),
            verification_freshness_days=os.getenv("VERIFICATION_FRESHNESS_DAYS", "90"),
        )


@lru_cache
def get_settings() -> Settings:
    return Settings.from_environment()


def require_database_url(settings: Settings) -> str:
    if not settings.database_url:
        raise DatabaseConfigurationError("DATABASE_URL is not configured")
    try:
        url = make_url(settings.database_url)
    except ArgumentError as error:
        raise DatabaseConfigurationError("DATABASE_URL is invalid") from error
    if url.drivername != "postgresql+psycopg":
        raise DatabaseConfigurationError("DATABASE_URL must use the postgresql+psycopg driver")
    if not url.database:
        raise DatabaseConfigurationError("DATABASE_URL must include a database name")
    if url.database != settings.expected_database_name:
        raise DatabaseConfigurationError("DATABASE_URL database name does not match the configured AidScout database")
    return settings.database_url
