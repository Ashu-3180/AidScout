from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import Settings, get_settings
from app.db.session import build_engine

router = APIRouter()


@router.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Liveness only: deliberately does not instantiate a database engine."""
    return {"status": "ok"}


@router.get("/ready", tags=["system"])
def readiness(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    """Read-only readiness probe with intentionally non-sensitive failures."""
    if not settings.database_url:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database is not configured")
    try:
        with build_engine().connect() as connection:
            connection.execute(text("SELECT 1"))
    except (RuntimeError, SQLAlchemyError):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database is unavailable") from None
    return {"status": "ready"}
