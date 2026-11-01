from datetime import date, datetime, timezone

from app.services.data_quality import CycleSnapshot, QualityCode, ScholarshipSnapshot, SourceSnapshot, evaluate_data_quality


def issue_codes(snapshot: ScholarshipSnapshot) -> set[QualityCode]:
    return {issue.code for issue in evaluate_data_quality(snapshot, freshness_days=90, today=date(2026, 10, 28), now=datetime(2026, 10, 28, tzinfo=timezone.utc))}


def test_reports_missing_required_fields_and_source() -> None:
    codes = issue_codes(ScholarshipSnapshot(canonical_name=None, provider_name=""))
    assert QualityCode.missing_required_field in codes
    assert QualityCode.missing_official_source in codes


def test_reports_duplicate_invalid_and_expired_cycles() -> None:
    snapshot = ScholarshipSnapshot(canonical_name="Synthetic", provider_name="Synthetic", cycles=[CycleSnapshot("2025-26", date(2026, 8, 1), date(2026, 7, 1), "open"), CycleSnapshot("2025-26", deadline=date(2026, 1, 1), cycle_status="open")])
    codes = issue_codes(snapshot)
    assert {QualityCode.duplicate_cycle, QualityCode.invalid_date_range, QualityCode.expired_cycle} <= codes


def test_reports_stale_verified_source_and_conflicting_claims() -> None:
    snapshot = ScholarshipSnapshot(canonical_name="Synthetic", provider_name="Synthetic", sources=[SourceSnapshot("official", "verified", datetime(2026, 1, 1, tzinfo=timezone.utc), "deadline", "A"), SourceSnapshot("provider", "verified", datetime(2026, 10, 1, tzinfo=timezone.utc), "deadline", "B")])
    codes = issue_codes(snapshot)
    assert QualityCode.stale_verification in codes
    assert QualityCode.conflicting_data in codes
    assert QualityCode.missing_official_source not in codes
