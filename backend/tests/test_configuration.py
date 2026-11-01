import pytest

from app.core.config import DatabaseConfigurationError, Settings, require_database_url
from app.db.migration import build_online_connectable


def test_missing_database_url_prevents_online_engine_creation() -> None:
    calls: list[object] = []

    def engine_factory(*args: object, **kwargs: object) -> object:
        calls.append((args, kwargs))
        return object()

    with pytest.raises(DatabaseConfigurationError, match="DATABASE_URL is not configured"):
        build_online_connectable(Settings(database_url=None), {}, engine_factory)
    assert calls == []


def test_invalid_database_url_prevents_online_engine_creation() -> None:
    calls: list[object] = []

    def engine_factory(*args: object, **kwargs: object) -> object:
        calls.append((args, kwargs))
        return object()

    with pytest.raises(DatabaseConfigurationError, match="DATABASE_URL is invalid"):
        build_online_connectable(Settings(database_url="not a database url"), {}, engine_factory)
    assert calls == []


def test_unrelated_database_name_prevents_online_engine_creation() -> None:
    calls: list[object] = []

    def engine_factory(*args: object, **kwargs: object) -> object:
        calls.append((args, kwargs))
        return object()

    settings = Settings(database_url="postgresql+psycopg://user:secret@localhost:5432/shopsphere_dev")
    with pytest.raises(DatabaseConfigurationError, match="database name does not match"):
        build_online_connectable(settings, {}, engine_factory)
    assert calls == []


def test_missing_database_name_is_rejected() -> None:
    with pytest.raises(DatabaseConfigurationError, match="include a database name"):
        require_database_url(Settings(database_url="postgresql+psycopg://user:secret@localhost"))


def test_readiness_environment_variable_uses_correct_spelling(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_READINESS_TIMEOUT_SECONDS", "7")
    settings = Settings.from_environment()
    assert settings.database_readiness_timeout_seconds == 7


def test_readiness_statement_timeout_is_configurable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_READINESS_STATEMENT_TIMEOUT_MILLISECONDS", "7000")
    settings = Settings.from_environment()
    assert settings.database_readiness_statement_timeout_milliseconds == 7000
