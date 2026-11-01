from datetime import date, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator

from app.models.enums import CriterionSupportStatus, CriterionValueStatus, CycleStatus, RecordStatus, SourceType, VerificationStatus

SUPPORTED_CRITERION_TYPES = frozenset({"academic_level", "academic_score", "category", "citizenship", "course", "gender", "income", "institution", "residency"})


class ScholarshipCycleCreate(BaseModel):
    academic_year: str = Field(min_length=1, max_length=32)
    cycle_status: CycleStatus = CycleStatus.planned
    opening_date: date | None = None
    deadline: date | None = None
    benefits: str | None = None
    application_url: HttpUrl | None = None

    @model_validator(mode="after")
    def dates_are_in_order(self) -> "ScholarshipCycleCreate":
        if self.opening_date and self.deadline and self.opening_date > self.deadline:
            raise ValueError("opening_date must not be after deadline")
        return self


class SourceEvidenceCreate(BaseModel):
    scholarship_id: UUID
    cycle_id: UUID | None = None
    source_url: HttpUrl
    publisher: str | None = Field(default=None, max_length=300)
    source_type: SourceType
    verification_status: VerificationStatus = VerificationStatus.unverified
    checked_at: datetime | None = None
    notes: str | None = None


class EligibilityCriterionCreate(BaseModel):
    scholarship_id: UUID
    cycle_id: UUID | None = None
    criterion_type: str = Field(min_length=1, max_length=100)
    operator: str = Field(min_length=1, max_length=32)
    value: Any | None = None
    unit: str | None = Field(default=None, max_length=64)
    is_required: bool = True
    value_status: CriterionValueStatus = CriterionValueStatus.unknown
    criterion_support_status: CriterionSupportStatus = CriterionSupportStatus.unknown
    source_evidence_id: UUID | None = None
    notes: str | None = None

    @model_validator(mode="after")
    def preserve_unknowns_explicitly(self) -> "EligibilityCriterionCreate":
        if self.value_status is CriterionValueStatus.known and self.value is None:
            raise ValueError("known criteria require a value")
        if self.value_status is CriterionValueStatus.unknown and self.value is not None:
            raise ValueError("unknown criteria must not include a value")
        if self.criterion_support_status is CriterionSupportStatus.supported and self.criterion_type not in SUPPORTED_CRITERION_TYPES:
            raise ValueError("supported criteria must use a recognized criterion_type")
        if self.criterion_support_status is not CriterionSupportStatus.supported and self.value_status is not CriterionValueStatus.unknown:
            raise ValueError("unknown or unsupported criteria must retain an unknown value")
        return self


class ScholarshipCreate(BaseModel):
    canonical_name: str = Field(min_length=1, max_length=300)
    provider_name: str = Field(min_length=1, max_length=300)
    description: str | None = None
    intended_audience: str | None = None
    record_status: RecordStatus = RecordStatus.draft
    cycles: list[ScholarshipCycleCreate] = Field(default_factory=list)

    @model_validator(mode="after")
    def cycle_years_are_unique(self) -> "ScholarshipCreate":
        years = [cycle.academic_year for cycle in self.cycles]
        if len(years) != len(set(years)):
            raise ValueError("academic_year values must be unique per scholarship")
        return self


class ScholarshipRead(BaseModel):
    """Reserved for a future database-backed read API."""

    model_config = ConfigDict(from_attributes=True)
    id: UUID
    canonical_name: str
    provider_name: str
    record_status: RecordStatus
