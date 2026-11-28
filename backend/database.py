"""
E-Waste AI — Unified Database Engine & Transaction Layer
========================================================
Supports PostgreSQL in production (via DATABASE_URL) and SQLite for local/testing
development without duplicating databases. Includes safe transaction context,
health checks, and SQLite hot-backup / logical JSON snapshot backup & restore.
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import sqlite3
from contextlib import contextmanager
from datetime import date, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import create_engine, event, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from backend.config import DATABASE_URL, ROOT_DIR

logger = logging.getLogger(__name__)


def is_sqlite_url(url: str) -> bool:
    return url.lower().startswith("sqlite")


def build_engine(url: str | None = None):
    """Create SQLAlchemy engine configured safely for PostgreSQL or SQLite."""
    target_url = url or DATABASE_URL
    if is_sqlite_url(target_url):
        eng = create_engine(
            target_url,
            connect_args={"check_same_thread": False},
            echo=False,
        )

        @event.listens_for(eng, "connect")
        def _set_sqlite_pragma(dbapi_connection, _connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        return eng

    # PostgreSQL / production pooled engine
    return create_engine(
        target_url,
        pool_pre_ping=True,
        pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
        max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20")),
        echo=False,
    )


engine = build_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI dependency: yields a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def db_session():
    """Context manager for atomic transactional database operations."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db(target_engine=None):
    """Create/migrate all ORM tables safely without modifying existing data."""
    import backend.models  # noqa: F401 — registers all Core + ERP ORM models
    from backend.migrations.runner import apply_migrations

    bind_eng = target_engine or engine
    apply_migrations(target_engine=bind_eng, pre_backup=False)
    logger.info("Database tables created/verified (%d registered tables).", len(Base.metadata.tables))


def check_db_health() -> bool:
    """Return True if database is reachable."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as exc:
        logger.error("DB health check failed: %s", exc)
        return False


def get_db_dialect(target_engine=None) -> str:
    """Return active SQLAlchemy dialect name ('sqlite', 'postgresql', etc.)."""
    return (target_engine or engine).dialect.name


def _json_default(obj: Any):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return str(obj)


def _sqlite_path_from_url(url: str) -> Path | None:
    if not is_sqlite_url(url) or ":memory:" in url:
        return None
    raw = url.split("sqlite:///")[-1]
    p = Path(raw)
    if not p.is_absolute():
        p = ROOT_DIR / raw
    return p


def backup_database(backup_dir: Path | None = None, target_engine=None) -> dict[str, Any]:
    """
    Create a safe non-destructive database backup.
    - On SQLite file DBs: performs atomic sqlite3 online hot backup AND JSON logical snapshot.
    - On PostgreSQL / in-memory DBs: writes structured JSON logical snapshot with row counts.
    """
    eng = target_engine or engine
    out_dir = Path(backup_dir or (ROOT_DIR / "database" / "backups"))
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")

    result: dict[str, Any] = {
        "timestamp": ts,
        "dialect": eng.dialect.name,
        "sqlite_backup_path": None,
        "snapshot_path": None,
        "tables_backed_up": 0,
        "total_rows": 0,
    }

    # SQLite hot-backup if backing file exists
    if eng is engine:
        src_path = _sqlite_path_from_url(DATABASE_URL)
        if src_path and src_path.exists():
            dst_db = out_dir / f"ewaste_ai_backup_{ts}.db"
            with sqlite3.connect(str(src_path)) as src_conn:
                with sqlite3.connect(str(dst_db)) as dst_conn:
                    src_conn.backup(dst_conn)
            result["sqlite_backup_path"] = str(dst_db)

    # Logical JSON snapshot across tables (works for SQLite, in-memory, PostgreSQL)
    insp = inspect(eng)
    table_names = sorted(insp.get_table_names())
    snapshot: dict[str, Any] = {"created_at": ts, "dialect": eng.dialect.name, "tables": {}}
    total_rows = 0
    with eng.connect() as conn:
        for tname in table_names:
            rows = conn.execute(text(f'SELECT * FROM "{tname}"')).mappings().all()
            row_dicts = [dict(r) for r in rows]
            snapshot["tables"][tname] = row_dicts
            total_rows += len(row_dicts)

    snap_path = out_dir / f"ewaste_ai_snapshot_{ts}.json"
    snap_path.write_text(json.dumps(snapshot, indent=2, default=_json_default), encoding="utf-8")
    result["snapshot_path"] = str(snap_path)
    result["tables_backed_up"] = len(table_names)
    result["total_rows"] = total_rows
    return result


def restore_sqlite_backup(backup_file: str | Path, target_db_path: str | Path) -> dict[str, Any]:
    """
    Restore an SQLite backup file safely to target_db_path using sqlite3 backup API.
    Never modifies the running DB unless explicitly targeted.
    """
    src = Path(backup_file)
    dst = Path(target_db_path)
    if not src.exists():
        raise FileNotFoundError(f"Backup file not found: {src}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(src)) as src_conn:
        with sqlite3.connect(str(dst)) as dst_conn:
            src_conn.backup(dst_conn)
    with sqlite3.connect(str(dst)) as verify_conn:
        tables = [r[0] for r in verify_conn.execute("SELECT name FROM sqlite_master WHERE type='table'")]
    return {"restored_to": str(dst), "tables_restored": len(tables), "verified": True}
