from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings, get_settings, require_database_url


def build_engine(settings: Settings | None = None) -> Engine:
    settings = settings or get_settings()
    database_url = require_database_url(settings)
    return create_engine(
        database_url,
        pool_pre_ping=True,
        connect_args={
            "connect_timeout": settings.database_readiness_timeout_seconds,
            "options": f"-c statement_timeout={settings.database_readiness_statement_timeout_milliseconds}",
        },
    )


def get_session() -> Generator[Session, None, None]:
    session_factory = sessionmaker(bind=build_engine(), autoflush=False, expire_on_commit=False)
    with session_factory() as session:
        yield session
