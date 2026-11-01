from datetime import date

import pytest
from pydantic import ValidationError

from app.models.enums import CriterionValueStatus
from app.schemas.scholarship import EligibilityCriterionCreate, ScholarshipCreate, ScholarshipCycleCreate


def test_cycle_rejects_inverted_dates() -> None:
    with pytest.raises(ValidationError, match="opening_date"):
        ScholarshipCycleCreate(academic_year="2026-27", opening_date=date(2026, 8, 1), deadline=date(2026, 7, 1))


def test_scholarship_rejects_duplicate_cycle_years() -> None:
    with pytest.raises(ValidationError, match="academic_year"):
        ScholarshipCreate(canonical_name="Synthetic record", provider_name="Synthetic provider", cycles=[ScholarshipCycleCreate(academic_year="2026-27"), ScholarshipCycleCreate(academic_year="2026-27")])


def test_unknown_criterion_is_explicit_and_value_free() -> None:
    criterion = EligibilityCriterionCreate(criterion_type="income", operator="equals", value_status=CriterionValueStatus.unknown)
    assert criterion.value is None
    with pytest.raises(ValidationError, match="unknown criteria"):
        EligibilityCriterionCreate(criterion_type="income", operator="equals", value=1, value_status=CriterionValueStatus.unknown)


def test_known_criterion_requires_value() -> None:
    with pytest.raises(ValidationError, match="known criteria"):
        EligibilityCriterionCreate(criterion_type="income", operator="equals", value_status=CriterionValueStatus.known)
