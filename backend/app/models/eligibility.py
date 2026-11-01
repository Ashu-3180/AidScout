from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, CheckConstraint, Enum, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import CriterionValueStatus
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.scholarship import Scholarship


class EligibilityCriterion(TimestampMixin, Base):
    __tablename__ = "eligibility_criteria"
    __table_args__ = (CheckConstraint("value_status = 'unknown' OR value_json IS NOT NULL", name="ck_known_criterion_has_value"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    scholarship_id: Mapped[UUID] = mapped_column(ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=False, index=True)
    cycle_id: Mapped[UUID | None] = mapped_column(ForeignKey("scholarship_cycles.id", ondelete="CASCADE"), nullable=True, index=True)
    source_evidence_id: Mapped[UUID | None] = mapped_column(ForeignKey("source_evidence.id", ondelete="SET NULL"), nullable=True, index=True)
    criterion_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    operator: Mapped[str] = mapped_column(String(32), nullable=False)
    value_json: Mapped[object | None] = mapped_column(JSON, nullable=True)
    unit: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    value_status: Mapped[CriterionValueStatus] = mapped_column(Enum(CriterionValueStatus, name="criterion_value_status"), default=CriterionValueStatus.unknown, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    scholarship: Mapped["Scholarship"] = relationship(back_populates="eligibility_criteria")
