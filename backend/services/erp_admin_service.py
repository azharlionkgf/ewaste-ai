"""
E-Waste AI — ERP Database Administration Service
================================================
Inspects live database tables/row counts, migration revisions, document
registry metrics, and coordinates safe backups and recovery checks.
"""

from __future__ import annotations

from typing import Any

from sqlalchemy import inspect, text

from backend.database import backup_database, engine, get_db_dialect
from backend.migrations.runner import apply_migrations, get_migration_status


class ERPAdminService:
    """System & database administration tools restricted to admin roles."""

    def get_database_overview(self, target_engine=None) -> dict[str, Any]:
        eng = target_engine or engine
        insp = inspect(eng)
        tables = sorted(insp.get_table_names())
        counts: dict[str, int] = {}
        with eng.connect() as conn:
            for t in tables:
                counts[t] = conn.execute(text(f'SELECT COUNT(*) FROM "{t}"')).scalar() or 0
        mig = get_migration_status(target_engine=eng)
        return {
            "dialect": get_db_dialect(target_engine=eng),
            "total_tables": len(tables),
            "tables": counts,
            "migration_status": mig,
        }

    def run_safe_migration(self, pre_backup: bool = True, target_engine=None) -> dict[str, Any]:
        return apply_migrations(target_engine=target_engine or engine, pre_backup=pre_backup)

    def create_backup(self, backup_dir=None, target_engine=None) -> dict[str, Any]:
        return backup_database(backup_dir=backup_dir, target_engine=target_engine or engine)
