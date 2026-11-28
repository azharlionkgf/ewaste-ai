"""
E-Waste AI — Safe Database Migration Engine
===========================================
Idempotent, zero-data-loss schema migration runner compatible with both
local SQLite and production PostgreSQL (`DATABASE_URL`). Never drops tables
or deletes existing rows; creates a backup snapshot prior to applying changes.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, Integer, String, inspect, text

from backend.database import Base, backup_database, engine

logger = logging.getLogger(__name__)


class SchemaMigration(Base):
    __tablename__ = "schema_migrations"

    revision = Column(String(64), primary_key=True)
    description = Column(String(256), nullable=False)
    dialect = Column(String(32), nullable=False)
    tables_after = Column(Integer, nullable=False, default=0)
    applied_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# Missing-column extensions on the 5 reused Phase 4 tables
_EXTENDED_COLUMNS: list[tuple[str, str, str]] = [
    ("audit_logs", "company_id", "VARCHAR(128)"),
    ("audit_logs", "branch_id", "VARCHAR(128)"),
    ("audit_logs", "employee_id", "VARCHAR(128)"),
    ("audit_logs", "module", "VARCHAR(64)"),
    ("audit_logs", "before_state", "TEXT"),
    ("audit_logs", "after_state", "TEXT"),
    ("audit_logs", "status", "VARCHAR(32)"),
    ("components", "company_id", "VARCHAR(128)"),
    ("components", "branch_id", "VARCHAR(128)"),
    ("components", "component_category_id", "VARCHAR(128)"),
    ("components", "device_model_id", "VARCHAR(128)"),
    ("components", "is_deleted", "BOOLEAN DEFAULT 0"),
    ("components", "updated_at", "DATETIME"),
    ("ai_predictions", "company_id", "VARCHAR(128)"),
    ("ai_predictions", "branch_id", "VARCHAR(128)"),
    ("ai_predictions", "incoming_batch_id", "VARCHAR(128)"),
    ("ai_predictions", "ai_model_version_id", "VARCHAR(128)"),
    ("ai_predictions", "review_status", "VARCHAR(32)"),
    ("ai_predictions", "human_verified", "BOOLEAN DEFAULT 0"),
    ("ai_predictions", "verified_by", "VARCHAR(128)"),
    ("ai_predictions", "verified_at", "DATETIME"),
    ("ai_predictions", "final_measured_outcome", "TEXT"),
    ("environmental_reports", "company_id", "VARCHAR(128)"),
    ("environmental_reports", "branch_id", "VARCHAR(128)"),
    ("environmental_reports", "compliance_category", "VARCHAR(128)"),
    ("environmental_reports", "jurisdiction_ref", "VARCHAR(256)"),
    ("environmental_reports", "supporting_document_id", "VARCHAR(128)"),
    ("environmental_reports", "is_deleted", "BOOLEAN DEFAULT 0"),
    ("environmental_reports", "updated_at", "DATETIME"),
    ("generated_reports", "company_id", "VARCHAR(128)"),
    ("generated_reports", "branch_id", "VARCHAR(128)"),
    ("generated_reports", "template_id", "VARCHAR(128)"),
    ("generated_reports", "is_deleted", "BOOLEAN DEFAULT 0"),
]


def _pg_or_sqlite_type(sql_type: str, dialect: str) -> str:
    if dialect == "postgresql":
        return (
            sql_type.replace("BOOLEAN DEFAULT 0", "BOOLEAN DEFAULT FALSE")
            .replace("DATETIME", "TIMESTAMP")
        )
    return sql_type


def _add_missing_columns(target_engine) -> list[str]:
    insp = inspect(target_engine)
    existing_tables = set(insp.get_table_names())
    dialect = target_engine.dialect.name
    added: list[str] = []

    with target_engine.begin() as conn:
        for table_name, col_name, col_type in _EXTENDED_COLUMNS:
            if table_name not in existing_tables:
                continue
            existing_cols = {c["name"] for c in insp.get_columns(table_name)}
            if col_name not in existing_cols:
                ddl_type = _pg_or_sqlite_type(col_type, dialect)
                conn.execute(text(f'ALTER TABLE "{table_name}" ADD COLUMN "{col_name}" {ddl_type}'))
                added.append(f"{table_name}.{col_name}")
    return added


MIGRATIONS: list[tuple[str, str]] = [
    ("0001_phase4_6_baseline", "Verify Phase 1-6 core & dataset ORM tables"),
    ("0002_erp_non_breaking_extensions", "Safely extend reused tables with nullable company/branch/audit columns"),
    ("0003_industrial_erp_15_modules", "Create all 15-module Industrial ERP tables without altering existing rows"),
    ("0004_erp_composite_indexes", "Verify and ensure hot-query relational indexes"),
]


def apply_migrations(target_engine=None, pre_backup: bool = False) -> dict[str, Any]:
    """Run all pending safe migrations against target_engine without deleting records."""
    import backend.models  # noqa: F401 — ensure full metadata is registered

    eng = target_engine or engine
    dialect = eng.dialect.name

    backup_info = backup_database(target_engine=eng) if pre_backup else None

    # Ensure migration history table exists first
    SchemaMigration.__table__.create(bind=eng, checkfirst=True)

    with eng.connect() as conn:
        applied = {
            row[0]
            for row in conn.execute(text("SELECT revision FROM schema_migrations")).fetchall()
        }

    executed: list[str] = []
    added_columns: list[str] = []

    if "0001_phase4_6_baseline" not in applied:
        Base.metadata.create_all(bind=eng, checkfirst=True)
        executed.append("0001_phase4_6_baseline")

    if "0002_erp_non_breaking_extensions" not in applied:
        added_columns = _add_missing_columns(eng)
        executed.append("0002_erp_non_breaking_extensions")

    if "0003_industrial_erp_15_modules" not in applied:
        Base.metadata.create_all(bind=eng, checkfirst=True)
        executed.append("0003_industrial_erp_15_modules")

    if "0004_erp_composite_indexes" not in applied:
        index_stmts = [
            'CREATE INDEX IF NOT EXISTS ix_audit_company_branch ON audit_logs (company_id, branch_id)',
            'CREATE INDEX IF NOT EXISTS ix_pred_company_batch ON ai_predictions (company_id, incoming_batch_id)',
            'CREATE INDEX IF NOT EXISTS ix_env_rep_company_branch ON environmental_reports (company_id, branch_id)',
        ]
        with eng.begin() as conn:
            for stmt in index_stmts:
                conn.execute(text(stmt))
        executed.append("0004_erp_composite_indexes")

    total_tables = len(inspect(eng).get_table_names())
    if executed:
        desc_map = dict(MIGRATIONS)
        with eng.begin() as conn:
            for rev in executed:
                conn.execute(
                    text(
                        "INSERT INTO schema_migrations (revision, description, dialect, tables_after, applied_at) "
                        "VALUES (:rev, :desc, :dial, :cnt, :ts)"
                    ),
                    {
                        "rev": rev,
                        "desc": desc_map[rev],
                        "dial": dialect,
                        "cnt": total_tables,
                        "ts": datetime.utcnow(),
                    },
                )

    return {
        "dialect": dialect,
        "executed_revisions": executed,
        "added_columns": added_columns,
        "total_tables": total_tables,
        "backup": backup_info,
    }


def get_migration_status(target_engine=None) -> dict[str, Any]:
    """Return applied revisions, pending revisions, and registered table counts."""
    import backend.models  # noqa: F401

    eng = target_engine or engine
    insp = inspect(eng)
    existing_tables = sorted(insp.get_table_names())
    applied_rows: list[dict[str, Any]] = []

    if "schema_migrations" in existing_tables:
        with eng.connect() as conn:
            rows = conn.execute(
                text("SELECT revision, description, dialect, tables_after, applied_at FROM schema_migrations ORDER BY applied_at")
            ).fetchall()
            applied_rows = [
                {
                    "revision": r[0],
                    "description": r[1],
                    "dialect": r[2],
                    "tables_after": r[3],
                    "applied_at": str(r[4]),
                }
                for r in rows
            ]

    applied_set = {r["revision"] for r in applied_rows}
    pending = [rev for rev, _ in MIGRATIONS if rev not in applied_set]
    return {
        "dialect": eng.dialect.name,
        "existing_tables_count": len(existing_tables),
        "orm_registered_count": len(Base.metadata.tables),
        "applied_migrations": applied_rows,
        "pending_migrations": pending,
        "is_up_to_date": len(pending) == 0,
    }
