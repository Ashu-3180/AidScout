"""Initial verified-scholarship data foundation.

Revision ID: 20261028_0001
Revises:
Create Date: 2026-10-28
"""

from alembic import context, op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "20261028_0001"
down_revision = None
branch_labels = None
depends_on = None

record_status = postgresql.ENUM("draft", "active", "archived", name="record_status", create_type=False)
cycle_status = postgresql.ENUM("planned", "open", "closed", "archived", name="cycle_status", create_type=False)
source_type = postgresql.ENUM("official", "provider", "government", "secondary", name="source_type", create_type=False)
verification_status = postgresql.ENUM("unverified", "verified", "disputed", "stale", name="verification_status", create_type=False)
criterion_value_status = postgresql.ENUM("known", "unknown", name="criterion_value_status", create_type=False)
criterion_support_status = postgresql.ENUM("supported", "unknown", "unsupported", name="criterion_support_status", create_type=False)


def _create_enum_types(bind: sa.Connection) -> None:
    for enum_type in (record_status, cycle_status, source_type, verification_status, criterion_value_status, criterion_support_status):
        enum_type.create(bind, checkfirst=not context.is_offline_mode())


def upgrade() -> None:
    bind = op.get_bind()
    _create_enum_types(bind)
    op.create_table(
        "scholarships",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("canonical_name", sa.String(300), nullable=False),
        sa.Column("provider_name", sa.String(300), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("intended_audience", sa.Text()),
        sa.Column("record_status", record_status, server_default=sa.text("'draft'"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("canonical_name", name="uq_scholarship_canonical_name"),
    )
    op.create_index("ix_scholarships_provider_name", "scholarships", ["provider_name"])
    op.create_table(
        "scholarship_cycles",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("scholarship_id", sa.Uuid(), sa.ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=False),
        sa.Column("academic_year", sa.String(32), nullable=False),
        sa.Column("cycle_status", cycle_status, server_default=sa.text("'planned'"), nullable=False),
        sa.Column("opening_date", sa.Date()),
        sa.Column("deadline", sa.Date()),
        sa.Column("benefits", sa.Text()),
        sa.Column("application_url", sa.String(2048)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("scholarship_id", "academic_year", name="uq_cycle_scholarship_academic_year"),
        sa.UniqueConstraint("id", "scholarship_id", name="uq_cycle_id_scholarship"),
        sa.CheckConstraint("opening_date IS NULL OR deadline IS NULL OR opening_date <= deadline", name="ck_cycle_date_order"),
    )
    op.create_index("ix_scholarship_cycles_deadline", "scholarship_cycles", ["deadline"])
    op.create_table(
        "source_evidence",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("scholarship_id", sa.Uuid(), sa.ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=False),
        sa.Column("cycle_id", sa.Uuid()),
        sa.Column("source_url", sa.String(2048), nullable=False),
        sa.Column("publisher", sa.String(300)),
        sa.Column("source_type", source_type, nullable=False),
        sa.Column("verification_status", verification_status, server_default=sa.text("'unverified'"), nullable=False),
        sa.Column("checked_at", sa.DateTime(timezone=True)),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.UniqueConstraint("id", "scholarship_id", name="uq_source_evidence_id_scholarship"),
        sa.ForeignKeyConstraint(["cycle_id", "scholarship_id"], ["scholarship_cycles.id", "scholarship_cycles.scholarship_id"], name="fk_source_cycle_same_scholarship", ondelete="CASCADE"),
    )
    op.create_index("ix_source_evidence_scholarship_id", "source_evidence", ["scholarship_id"])
    op.create_index("ix_source_evidence_cycle_id", "source_evidence", ["cycle_id"])
    op.create_index("ix_source_evidence_verification_status", "source_evidence", ["verification_status"])
    op.create_index("ix_source_evidence_checked_at", "source_evidence", ["checked_at"])
    op.create_table(
        "eligibility_criteria",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("scholarship_id", sa.Uuid(), sa.ForeignKey("scholarships.id", ondelete="CASCADE"), nullable=False),
        sa.Column("cycle_id", sa.Uuid()),
        sa.Column("source_evidence_id", sa.Uuid()),
        sa.Column("criterion_type", sa.String(100), nullable=False),
        sa.Column("operator", sa.String(32), nullable=False),
        sa.Column("value_json", sa.JSON(none_as_null=True)),
        sa.Column("unit", sa.String(64)),
        sa.Column("is_required", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("value_status", criterion_value_status, server_default=sa.text("'unknown'"), nullable=False),
        sa.Column("criterion_support_status", criterion_support_status, server_default=sa.text("'unknown'"), nullable=False),
        sa.Column("notes", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("(value_status = 'unknown' AND value_json IS NULL) OR (value_status = 'known' AND value_json IS NOT NULL)", name="ck_criterion_value_status"),
        sa.CheckConstraint("criterion_support_status = 'supported' OR value_status = 'unknown'", name="ck_unsupported_criterion_is_unknown"),
        sa.CheckConstraint("criterion_support_status != 'supported' OR criterion_type IN ('academic_level', 'academic_score', 'category', 'citizenship', 'course', 'gender', 'income', 'institution', 'residency')", name="ck_supported_criterion_type"),
        sa.ForeignKeyConstraint(["cycle_id", "scholarship_id"], ["scholarship_cycles.id", "scholarship_cycles.scholarship_id"], name="fk_criterion_cycle_same_scholarship", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["source_evidence_id", "scholarship_id"], ["source_evidence.id", "source_evidence.scholarship_id"], name="fk_criterion_source_same_scholarship", ondelete="CASCADE"),
    )
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
    for enum_type in (criterion_support_status, criterion_value_status, verification_status, source_type, cycle_status, record_status):
        enum_type.drop(bind, checkfirst=not context.is_offline_mode())
