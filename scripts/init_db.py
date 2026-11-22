"""
scripts/init_db.py
E-WASTE AI - Database Initialisation Script
Creates all SQLAlchemy tables and optionally seeds initial data.
"""

import sys
import logging
from pathlib import Path

# Ensure project root is on path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def init_db():
    """Create all database tables."""
    logger.info("Initialising E-WASTE AI database...")

    # Import engine and Base
    from backend.database import engine, Base

    # Import ALL models so SQLAlchemy registers them before create_all
    from backend.models import (
        Dataset, DatasetVersion, CleaningRun, PreprocessingConfig,
        TrainingRun, ModelEvaluation, Prediction,
        WasteBatch, BatchItem, ItemClassification, ItemComponent,
        MaterialRecovery, EconomicValuation, OperationalCost, EwasteCategory,
        ResearchExperiment, ExperimentRun, ExperimentMetric,
        BaselineComparison, ResearchReport,
    )

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # List tables created
    from sqlalchemy import inspect as sa_inspect
    inspector = sa_inspect(engine)
    tables = inspector.get_table_names()
    logger.info(f"Database initialised. Tables ({len(tables)}): {tables}")
    return tables


def seed_categories():
    """Seed e-waste categories from config/ewaste_categories.json."""
    import json
    from sqlalchemy.orm import Session
    from backend.database import engine
    from backend.models.waste_batch import EwasteCategory

    categories_file = PROJECT_ROOT / "config" / "ewaste_categories.json"
    if not categories_file.exists():
        logger.warning(f"Categories file not found: {categories_file}")
        return 0

    with open(categories_file, encoding="utf-8") as f:
        categories = json.load(f)

    seeded = 0
    with Session(engine) as session:
        for cat in categories:
            exists = session.query(EwasteCategory).filter_by(
                category_code=cat["category_code"]
            ).first()
            if not exists:
                new_cat = EwasteCategory(
                    category_code=cat["category_code"],
                    name=cat["name"],
                    description=cat.get("description", ""),
                    hazmat_level=cat.get("hazmat_level", "low"),
                    recovery_complexity=cat.get("recovery_complexity", "low"),
                )
                session.add(new_cat)
                seeded += 1
        session.commit()

    logger.info(f"Seeded {seeded} e-waste categories (skipped {len(categories) - seeded} existing).")
    return seeded


if __name__ == "__main__":
    try:
        tables = init_db()
        print(f"\n✓ Database initialised successfully.")
        print(f"  Tables created: {len(tables)}")
        for t in sorted(tables):
            print(f"    - {t}")

        # Seed categories
        try:
            n = seed_categories()
            print(f"\n✓ Seeded {n} e-waste categories.")
        except Exception as e:
            print(f"\n⚠ Category seeding failed (non-critical): {e}")

        print("\nDatabase ready at: database/ewaste_ai.db")

    except Exception as e:
        logger.error(f"Database initialisation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
