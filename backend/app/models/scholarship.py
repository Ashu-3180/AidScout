from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, Date, Enum, ForeignKey, String, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import CycleStatus, RecordStatus
from app.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.models.eligibility import EligibilityCriterion
    from app.models.source import SourceEvidence


class Scholarship(TimestampMixin, Base):
    __tablename__ = "scholarships"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    __table_args__ = (UniqueConstraint("canonical_name", name="uq_scholarship_canonical_name"),)

    canonical_name: Mapped[str] = mapped_column(String(300), nullable=False)
    provider_name: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    intended_audience: Mapped[str | None] = mapped_column(Text, nullable=True)
    record_status: Mapped[RecordStatus] = mapped_column(Enum(RecordStatus, name="record_status"), default=RecordStatus.draft, server_default=text("'draft'"), nullable=False)

    cycles: Mapped[list["ScholarshipCycle"]] = relationship(back_populates="scholarship", cascade="all, delete-orphan")
    sources: Mapped[list["SourceEvidence"]] = relationship(back_populates="scholarship")
    eligibility_criteria: Mapped[list["EligibilityCriterion"]] = relationship(back_populates="scholarship", cascade="all, delete-orphan")


class ScholarshipCycle(TimestampMixin, Base):
    __tablename__ = "scholarship_cycles"
    __table_args__ = (
        UniqueConstraint("scholarship_id", "academic_year", name="uq_cycle_scholarship_academic_year"),
        UniqueConstraint("id", "scholarship_id", name="uq_cycle_id_scholarship"),
        CheckConstraint("opening_date IS NULL OR deadline IS NULL OR opening_date <= deadline", name="ck_cycle_date_order"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    scholarship_id: Mapped[UUID] = mapped_column(ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=False)
    academic_year: Mapped[str] = mapped_column(String(32), nullable=False)
    cycle_status: Mapped[CycleStatus] = mapped_column(Enum(CycleStatus, name="cycle_status"), default=CycleStatus.planned, server_default=text("'planned'"), nullable=False)
    opening_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    deadline: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)
    benefits: Mapped[str | None] = mapped_column(Text, nullable=True)
    application_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)

    scholarship: Mapped[Scholarship] = relationship(back_populates="cycles")
    sources: Mapped[list["SourceEvidence"]] = relationship(back_populates="cycle", viewonly=True)
