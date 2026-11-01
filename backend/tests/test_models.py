from app.db.base import Base
import app.models  # noqa: F401


def test_expected_tables_are_registered() -> None:
    assert {"scholarships", "scholarship_cycles", "source_evidence", "eligibility_criteria"} <= set(Base.metadata.tables)
