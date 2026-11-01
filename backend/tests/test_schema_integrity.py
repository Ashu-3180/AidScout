from pathlib import Path
import re

from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable

from app.db.base import Base
import app.models  # noqa: F401


def composite_foreign_key(table_name: str, name: str) -> ForeignKeyConstraint:
    table = Base.metadata.tables[table_name]
    return next(constraint for constraint in table.constraints if isinstance(constraint, ForeignKeyConstraint) and constraint.name == name)


def test_source_cycle_ownership_is_a_composite_foreign_key() -> None:
    constraint = composite_foreign_key("source_evidence", "fk_source_cycle_same_scholarship")
    assert [column.name for column in constraint.columns] == ["cycle_id", "scholarship_id"]
    assert [element.target_fullname for element in constraint.elements] == ["scholarship_cycles.id", "scholarship_cycles.scholarship_id"]


def test_criteria_scope_is_enforced_for_cycles_and_sources() -> None:
    cycle_constraint = composite_foreign_key("eligibility_criteria", "fk_criterion_cycle_same_scholarship")
    source_constraint = composite_foreign_key("eligibility_criteria", "fk_criterion_source_same_scholarship")
    assert [element.target_fullname for element in cycle_constraint.elements] == ["scholarship_cycles.id", "scholarship_cycles.scholarship_id"]
    assert [element.target_fullname for element in source_constraint.elements] == ["source_evidence.id", "source_evidence.scholarship_id"]


def test_owned_dependents_cascade_with_their_scoped_parent() -> None:
    source_cycle = composite_foreign_key("source_evidence", "fk_source_cycle_same_scholarship")
    criterion_cycle = composite_foreign_key("eligibility_criteria", "fk_criterion_cycle_same_scholarship")
    criterion_source = composite_foreign_key("eligibility_criteria", "fk_criterion_source_same_scholarship")
    assert {source_cycle.ondelete, criterion_cycle.ondelete, criterion_source.ondelete} == {"CASCADE"}


def test_postgresql_ddl_contains_ownership_constraints() -> None:
    ddl = str(CreateTable(Base.metadata.tables["eligibility_criteria"]).compile(dialect=postgresql.dialect()))
    assert "fk_criterion_cycle_same_scholarship" in ddl
    assert "fk_criterion_source_same_scholarship" in ddl
    assert "ck_unsupported_criterion_is_unknown" in ddl


def test_migration_creates_every_orm_declared_index() -> None:
    model_indexes = {index.name for table in Base.metadata.tables.values() for index in table.indexes}
    migration_source = Path("migrations/versions/20261028_0001_initial_schema.py").read_text(encoding="utf-8")
    migration_indexes = set(re.findall(r'op\.create_index\("([^"]+)"', migration_source))
    assert model_indexes <= migration_indexes
