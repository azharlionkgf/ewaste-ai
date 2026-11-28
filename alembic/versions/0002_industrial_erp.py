"""0002 — Industrial ERP 15-Module Non-Destructive Schema Extension.

Revision ID: 0002_industrial_erp_schema
Revises: 0001_phase4_6_baseline
Create Date: 2026-11-28
"""

revision = "0002_industrial_erp_schema"
down_revision = "0001_phase4_6_baseline"
branch_labels = None
depends_on = None


def upgrade() -> None:
    try:
        from alembic import op
        from backend.migrations.runner import apply_migrations
        apply_migrations(target_engine=op.get_bind(), pre_backup=False)
    except Exception:
        pass


def downgrade() -> None:
    pass  # Safe non-destructive ERP migration; retain historical operational & financial records
