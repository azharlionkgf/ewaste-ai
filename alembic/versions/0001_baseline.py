"""0001 — Phase 1-6 Baseline Schema (PostgreSQL & SQLite safe).

Revision ID: 0001_phase4_6_baseline
Revises:
Create Date: 2026-11-28
"""

from backend.database import Base
import backend.models.all_models  # noqa: F401
import backend.models.dataset  # noqa: F401

revision = "0001_phase4_6_baseline"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    try:
        from alembic import op
        bind = op.get_bind()
        Base.metadata.create_all(bind=bind, checkfirst=True)
    except Exception:
        pass


def downgrade() -> None:
    pass  # Non-destructive baseline — never drops user tables automatically
