from functools import lru_cache
import os

from pydantic import BaseModel, Field, field_validator


class Settings(BaseModel):
    database_url: str | None = None
    database_readiness_timeout_seconds: int = Field(default=3, ge=1, le=30)
    verification_freshness_days: int = Field(default=90, ge=1, le=3650)

    @field_validator("database_url", mode="before")
    @classmethod
    def blank_database_url_is_unset(cls, value: object) -> object:
        return None if isinstance(value, str) and not value.strip() else value

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
            database_url=os.getenv("DATABASE_URL"),
            database_readiness_timeout_seconds=os.getenv("DATABASE_READYNESS_TIMEOUT_SECONDS", "3"),
            verification_freshness_days=os.getenv("VERIFICATION_FRESHNESS_DAYS", "90"),
        )


@lru_cache
def get_settings() -> Settings:
    return Settings.from_environment()
