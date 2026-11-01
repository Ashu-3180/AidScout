import pytest
from fastapi import HTTPException

from app.api.routes import health, readiness
from app.core.config import Settings


def test_health_never_needs_database() -> None:
    assert health() == {"status": "ok"}


def test_readiness_is_safe_when_database_is_not_configured() -> None:
    with pytest.raises(HTTPException) as exception:
        readiness(Settings(database_url=None))
    assert exception.value.status_code == 503
    assert exception.value.detail == "Database is not configured"
