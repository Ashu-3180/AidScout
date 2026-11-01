from dataclasses import dataclass, field
from datetime import date, datetime, timedelta, timezone
from enum import StrEnum


class QualityCode(StrEnum):
    missing_required_field = "missing_required_field"
    duplicate_cycle = "duplicate_cycle"
    invalid_date_range = "invalid_date_range"
    expired_cycle = "expired_cycle"
    stale_verification = "stale_verification"
    missing_official_source = "missing_official_source"
    conflicting_data = "conflicting_data"


@dataclass(frozen=True)
class QualityIssue:
    code: QualityCode
    message: str
    severity: str = "warning"


@dataclass(frozen=True)
class CycleSnapshot:
    academic_year: str
    opening_date: date | None = None
    deadline: date | None = None
    cycle_status: str = "planned"


@dataclass(frozen=True)
class SourceSnapshot:
    source_type: str
    verification_status: str
    checked_at: datetime | None = None
    claim_key: str | None = None
    claim_value: str | None = None


@dataclass(frozen=True)
class ScholarshipSnapshot:
    canonical_name: str | None
    provider_name: str | None
    cycles: list[CycleSnapshot] = field(default_factory=list)
    sources: list[SourceSnapshot] = field(default_factory=list)


def evaluate_data_quality(snapshot: ScholarshipSnapshot, *, freshness_days: int, today: date | None = None, now: datetime | None = None) -> list[QualityIssue]:
    today = today or date.today()
    now = now or datetime.now(timezone.utc)
    issues: list[QualityIssue] = []
    if not snapshot.canonical_name or not snapshot.canonical_name.strip():
        issues.append(QualityIssue(QualityCode.missing_required_field, "Scholarship canonical name is missing.", "error"))
    if not snapshot.provider_name or not snapshot.provider_name.strip():
        issues.append(QualityIssue(QualityCode.missing_required_field, "Scholarship provider is missing.", "error"))
    years: set[str] = set()
    for cycle in snapshot.cycles:
        if cycle.academic_year in years:
            issues.append(QualityIssue(QualityCode.duplicate_cycle, f"Duplicate academic year: {cycle.academic_year}.", "error"))
        years.add(cycle.academic_year)
        if cycle.opening_date and cycle.deadline and cycle.opening_date > cycle.deadline:
            issues.append(QualityIssue(QualityCode.invalid_date_range, f"Invalid dates for {cycle.academic_year}.", "error"))
        if cycle.deadline and cycle.deadline < today and cycle.cycle_status not in {"closed", "archived"}:
            issues.append(QualityIssue(QualityCode.expired_cycle, f"Past deadline for {cycle.academic_year} needs review."))
    official_sources = [source for source in snapshot.sources if source.source_type in {"official", "government", "provider"}]
    if not official_sources:
        issues.append(QualityIssue(QualityCode.missing_official_source, "No official, government, or provider source is recorded."))
    freshness_cutoff = now - timedelta(days=freshness_days)
    for source in snapshot.sources:
        if source.verification_status == "verified" and (source.checked_at is None or source.checked_at < freshness_cutoff):
            issues.append(QualityIssue(QualityCode.stale_verification, "A verified source needs rechecking."))
    claims: dict[str, set[str]] = {}
    for source in snapshot.sources:
        if source.claim_key and source.claim_value:
            claims.setdefault(source.claim_key, set()).add(source.claim_value)
    for claim_key, values in claims.items():
        if len(values) > 1:
            issues.append(QualityIssue(QualityCode.conflicting_data, f"Conflicting values recorded for {claim_key}."))
    return issues
