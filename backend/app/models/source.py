from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import SourceType, VerificationStatus
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.scholarship import Scholarship, ScholarshipCycle


class SourceEvidence(TimestampMixin, Base):
    __tablename__ = "source_evidence"
    __table_args__ = (CheckConstraint("scholarship_id IS NOT NULL OR cycle_id IS NOT NULL", name="ck_source_has_subject"),)

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    scholarship_id: Mapped[UUID | None] = mapped_column(ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=True, index=True)
    cycle_id: Mapped[UUID | None] = mapped_column(ForeignKey("scholarship_cycles.id", ondelete="CASCADE"), nullable=True, index=True)
    source_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    publisher: Mapped[str | None] = mapped_column(String(300), nullable=True)
    source_type: Mapped[SourceType] = mapped_column(Enum(SourceType, name="source_type"), nullable=False)
    verification_status: Mapped[VerificationStatus] = mapped_column(Enum(VerificationStatus, name="verification_status"), default=VerificationStatus.unverified, nullable=False, index=True)
    checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    scholarship: Mapped["Scholarship | None"] = relationship(back_populates="sources")
    cycle: Mapped["ScholarshipCycle | None"] = relationship(back_populates="sources")
