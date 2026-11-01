"""Initial verified-scholarship data foundation.

Revision ID: 20261028_0001
Revises:
Create Date: 2026-10-28
"""

from alembic import op
import sqlalchemy as sa

revision = "20261028_0001"
down_revision = None
branch_labels = None
depends_on = None

record_status = sa.Enum("draft", "active", "archived", name="record_status")
cycle_status = sa.Enum("planned", "open", "closed", "archived", name="cycle_status")
source_type = sa.Enum("official", "provider", "government", "secondary", name="source_type")
verification_status = sa.Enum("unverified", "verified", "disputed", "stale", name="verification_status")
criterion_value_status = sa.Enum("known", "unknown", name="criterion_value_status")


def upgrade() -> None:
    bind = op.get_bind()
    for enum_type in (record_status, cycle_status, source_type, verification_status, criterion_value_status):
        enum_type.create(bind, checkfirst=True)
    op.create_table("scholarships", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("canonical_name", sa.String(300), nullable=False, unique=True), sa.Column("provider_name", sa.String(300), nullable=False), sa.Column("description", sa.Text()), sa.Column("intended_audience", sa.Text()), sa.Column("record_status", record_status, nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False))
    op.create_index("ix_scholarships_canonical_name", "scholarships", ["canonical_name"])
    op.create_index("ix_scholarships_provider_name", "scholarships", ["provider_name"])
    op.create_table("scholarship_cycles", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("scholarship_id", sa.Uuid(), sa.ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=False), sa.Column("academic_year", sa.String(32), nullable=False), sa.Column("cycle_status", cycle_status, nullable=False), sa.Column("opening_date", sa.Date()), sa.Column("deadline", sa.Date()), sa.Column("benefits", sa.Text()), sa.Column("application_url", sa.String(2048)), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False), sa.UniqueConstraint("scholarship_id", "academic_year", name="uq_cycle_scholarship_academic_year"), sa.CheckConstraint("opening_date IS NULL OR deadline IS NULL OR opening_date <= deadline", name="ck_cycle_date_order"))
    op.create_index("ix_scholarship_cycles_scholarship_id", "scholarship_cycles", ["scholarship_id"])
    op.create_table("source_evidence", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("scholarship_id", sa.Uuid(), sa.ForeignKey("scholarships.id", ondelete="CASCADE")), sa.Column("cycle_id", sa.Uuid(), sa.ForeignKey("scholarship_cycles.id", ondelete="CASCADE")), sa.Column("source_url", sa.String(2048), nullable=False), sa.Column("publisher", sa.String(300)), sa.Column("source_type", source_type, nullable=False), sa.Column("verification_status", verification_status, nullable=False), sa.Column("checked_at", sa.DateTime(timezone=True)), sa.Column("notes", sa.Text()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False), sa.CheckConstraint("scholarship_id IS NOT NULL OR cycle_id IS NOT NULL", name="ck_source_has_subject"))
    op.create_index("ix_source_evidence_scholarship_id", "source_evidence", ["scholarship_id"])
    op.create_index("ix_source_evidence_cycle_id", "source_evidence", ["cycle_id"])
    op.create_index("ix_source_evidence_verification_status", "source_evidence", ["verification_status"])
    op.create_index("ix_source_evidence_checked_at", "source_evidence", ["checked_at"])
    op.create_table("eligibility_criteria", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("scholarship_id", sa.Uuid(), sa.ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=False), sa.Column("cycle_id", sa.Uuid(), sa.ForeignKey("scholarship_cycles.id", ondelete="CASCADE")), sa.Column("source_evidence_id", sa.Uuid(), sa.ForeignKey("source_evidence.id", ondelete="SET NULL")), sa.Column("criterion_type", sa.String(100), nullable=False), sa.Column("operator", sa.String(32), nullable=False), sa.Column("value_json", sa.JSON()), sa.Column("unit", sa.String(64)), sa.Column("is_required", sa.Boolean(), nullable=False), sa.Column("value_status", criterion_value_status, nullable=False), sa.Column("notes", sa.Text()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False), sa.CheckConstraint("value_status = 'unknown' OR value_json IS NOT NULL", name="ck_known_criterion_has_value"))
    op.create_index("ix_eligibility_criteria_scholarship_id", "eligibility_criteria", ["scholarship_id"])
    op.create_index("ix_eligibility_criteria_cycle_id", "eligibility_criteria", ["cycle_id"])
    op.create_index("ix_eligibility_criteria_source_evidence_id", "eligibility_criteria", ["source_evidence_id"])
    op.create_index("ix_eligibility_criteria_criterion_type", "eligibility_criteria", ["criterion_type"])


def downgrade() -> None:
    op.drop_table("eligibility_criteria")
    op.drop_table("source_evidence")
    op.drop_table("scholarship_cycles")
    op.drop_table("scholarships")
    bind = op.get_bind()
    for enum_type in (criterion_value_status, verification_status, source_type, cycle_status, record_status):
        enum_type.drop(bind, checkfirst=True)
