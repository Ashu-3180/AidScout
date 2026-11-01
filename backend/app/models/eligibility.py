from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, CheckConstraint, Enum, ForeignKey, ForeignKeyConstraint, JSON, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import CriterionSupportStatus, CriterionValueStatus
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.scholarship import Scholarship, ScholarshipCycle
    from app.models.source import SourceEvidence


class EligibilityCriterion(TimestampMixin, Base):
    __tablename__ = "eligibility_criteria"
    __table_args__ = (
        CheckConstraint("(value_status = 'unknown' AND value_json IS NULL) OR (value_status = 'known' AND value_json IS NOT NULL)", name="ck_criterion_value_status"),
        CheckConstraint("criterion_support_status = 'supported' OR value_status = 'unknown'", name="ck_unsupported_criterion_is_unknown"),
        CheckConstraint("criterion_support_status != 'supported' OR criterion_type IN ('academic_level', 'academic_score', 'category', 'citizenship', 'course', 'gender', 'income', 'institution', 'residency')", name="ck_supported_criterion_type"),
        ForeignKeyConstraint(["cycle_id", "scholarship_id"], ["scholarship_cycles.id", "scholarship_cycles.scholarship_id"], name="fk_criterion_cycle_same_scholarship", ondelete="CASCADE"),
        ForeignKeyConstraint(["source_evidence_id", "scholarship_id"], ["source_evidence.id", "source_evidence.scholarship_id"], name="fk_criterion_source_same_scholarship", ondelete="CASCADE"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    scholarship_id: Mapped[UUID] = mapped_column(ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=False, index=True)
    cycle_id: Mapped[UUID | None] = mapped_column(nullable=True, index=True)
    source_evidence_id: Mapped[UUID | None] = mapped_column(nullable=True, index=True)
    criterion_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    operator: Mapped[str] = mapped_column(String(32), nullable=False)
    value_json: Mapped[object | None] = mapped_column(JSON(none_as_null=True), nullable=True)
    unit: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text("true"), nullable=False)
    value_status: Mapped[CriterionValueStatus] = mapped_column(Enum(CriterionValueStatus, name="criterion_value_status"), default=CriterionValueStatus.unknown, server_default=text("'unknown'"), nullable=False)
    criterion_support_status: Mapped[CriterionSupportStatus] = mapped_column(Enum(CriterionSupportStatus, name="criterion_support_status"), default=CriterionSupportStatus.unknown, server_default=text("'unknown'"), nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    scholarship: Mapped["Scholarship"] = relationship(back_populates="eligibility_criteria")
    cycle: Mapped["ScholarshipCycle | None"] = relationship(
        primaryjoin="and_(EligibilityCriterion.cycle_id == ScholarshipCycle.id, EligibilityCriterion.scholarship_id == ScholarshipCycle.scholarship_id)",
        foreign_keys=[cycle_id, scholarship_id],
        viewonly=True,
    )
    source_evidence: Mapped["SourceEvidence | None"] = relationship(
        primaryjoin="and_(EligibilityCriterion.source_evidence_id == SourceEvidence.id, EligibilityCriterion.scholarship_id == SourceEvidence.scholarship_id)",
        foreign_keys=[source_evidence_id, scholarship_id],
        viewonly=True,
    )
