from io import StringIO

from alembic import command
from alembic.config import Config

from app.core.config import get_settings


def test_initial_migration_renders_postgresql_sql_without_database_url(monkeypatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    get_settings.cache_clear()
    output = StringIO()
    config = Config("alembic.ini", output_buffer=output)
    command.upgrade(config, "head", sql=True)
    sql = output.getvalue()
    assert sql.count("CREATE TYPE record_status") == 1
    assert sql.count("CREATE TYPE criterion_support_status") == 1
    assert "fk_source_cycle_same_scholarship" in sql
    get_settings.cache_clear()
