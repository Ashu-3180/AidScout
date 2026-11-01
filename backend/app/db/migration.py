from collections.abc import Callable
from typing import Any

from app.core.config import Settings, require_database_url


def build_online_connectable(
    settings: Settings,
    configuration: dict[str, Any],
    engine_factory: Callable[..., Any],
    **engine_kwargs: Any,
) -> Any:
    """Build an Alembic connectable only after configuration is validated."""
    configuration["sqlalchemy.url"] = require_database_url(settings)
    return engine_factory(configuration, prefix="sqlalchemy.", **engine_kwargs)
