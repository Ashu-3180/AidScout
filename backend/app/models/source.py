from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, ForeignKeyConstraint, String, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import SourceType, VerificationStatus
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.scholarship import Scholarship, ScholarshipCycle


class SourceEvidence(TimestampMixin, Base):
    __tablename__ = "source_evidence"
    __table_args__ = (
        UniqueConstraint("id", "scholarship_id", name="uq_source_evidence_id_scholarship"),
        ForeignKeyConstraint(
            ["cycle_id", "scholarship_id"],
            ["scholarship_cycles.id", "scholarship_cycles.scholarship_id"],
            name="fk_source_cycle_same_scholarship",
            ondelete="CASCADE",
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    scholarship_id: Mapped[UUID] = mapped_column(ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=False, index=True)
    cycle_id: Mapped[UUID | None] = mapped_column(nullable=True, index=True)
    source_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    publisher: Mapped[str | None] = mapped_column(String(300), nullable=True)
    source_type: Mapped[SourceType] = mapped_column(Enum(SourceType, name="source_type"), nullable=False)
    verification_status: Mapped[VerificationStatus] = mapped_column(Enum(VerificationStatus, name="verification_status"), default=VerificationStatus.unverified, server_default=text("'unverified'"), nullable=False, index=True)
    checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    scholarship: Mapped["Scholarship"] = relationship(back_populates="sources", foreign_keys=[scholarship_id])
    cycle: Mapped["ScholarshipCycle | None"] = relationship(
        back_populates="sources",
        primaryjoin="and_(SourceEvidence.cycle_id == ScholarshipCycle.id, SourceEvidence.scholarship_id == ScholarshipCycle.scholarship_id)",
        foreign_keys=[cycle_id, scholarship_id],
        viewonly=True,
    )
