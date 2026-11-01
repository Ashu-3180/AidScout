from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings


def build_engine() -> Engine:
    settings = get_settings()
    if not settings.database_url:
        raise RuntimeError("Database is not configured")
    return create_engine(
        settings.database_url,
        pool_pre_ping=True,
        connect_args={"connect_timeout": settings.database_readiness_timeout_seconds},
    )


def get_session() -> Generator[Session, None, None]:
    session_factory = sessionmaker(bind=build_engine(), autoflush=False, expire_on_commit=False)
    with session_factory() as session:
        yield session
