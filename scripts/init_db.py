"""
E-Waste AI — Database Initialization Script
============================================
Run this script once to create the SQLite database and all tables.

Usage:
    python scripts/init_db.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from pathlib import Path
from backend.config import settings
from backend.database import engine, Base, init_db
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


def main():
    logger.info("=" * 60)
    logger.info("  E-Waste AI — Database Initialization")
    logger.info("=" * 60)

    # Ensure required directories exist
    settings.ensure_directories()
    logger.info("✅ Project directories verified")

    # Initialize DB (creates tables)
    init_db()
    logger.info("✅ Database initialized at: database/ewaste_ai.db")

    # Verify
    db_path = Path("database/ewaste_ai.db")
    if db_path.exists():
        size_kb = db_path.stat().st_size / 1024
        logger.info(f"✅ Database file created ({size_kb:.1f} KB)")
    else:
        logger.warning("⚠️  Database file not found — check DATABASE_URL in .env")

    logger.info("=" * 60)
    logger.info("  Initialization complete!")
    logger.info("  Next steps:")
    logger.info("  1. uvicorn backend.main:app --port 8000 --reload")
    logger.info("  2. streamlit run app.py")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
