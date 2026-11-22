"""
scripts/seed_db.py
E-WASTE AI - Database Seeding Script
Seeds e-waste categories, material prices, and sample research experiments.
"""

import sys
import json
import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def seed_categories(session, categories_file: Path) -> int:
    """Seed EwasteCategory records."""
    from backend.models.waste_batch import EwasteCategory

    if not categories_file.exists():
        logger.warning(f"Categories file not found: {categories_file}")
        return 0

    with open(categories_file, encoding="utf-8") as f:
        categories = json.load(f)

    seeded = 0
    for cat in categories:
        exists = session.query(EwasteCategory).filter_by(
            category_code=cat["category_code"]
        ).first()
        if not exists:
            session.add(EwasteCategory(
                category_code=cat["category_code"],
                name=cat["name"],
                category_name=cat["name"],
                description=cat.get("description", ""),
                hazmat_level=cat.get("hazmat_level", "low"),
            ))
            seeded += 1

    logger.info(f"Categories: seeded {seeded} / {len(categories)} total.")
    return seeded


def seed_research_experiments(session) -> int:
    """Seed sample research experiment records."""
    from backend.models.research import ResearchExperiment
    import uuid

    sample_experiments = [
        {
            "experiment_code": "EXP-001-CNN-BASELINE",
            "experiment_name": "Baseline CNN Classification Study",
            "research_question": "Which CNN architecture achieves the best accuracy for e-waste image classification on CPU?",
            "hypothesis": "EfficientNet-B0 will achieve higher accuracy than MobileNetV3-Small on e-waste images, with acceptable CPU inference time.",
            "methodology": "Transfer learning on custom e-waste dataset. 70/15/15 train/val/test split. Stratified by category. Evaluated with accuracy, F1-macro, confusion matrix.",
            "status": "planned",
        },
        {
            "experiment_code": "EXP-002-TABULAR-VS-CNN",
            "experiment_name": "Tabular vs Image Classification Comparison",
            "research_question": "Do tabular-feature classifiers achieve comparable accuracy to CNNs for e-waste categorisation?",
            "hypothesis": "Tabular classifiers achieve comparable accuracy to CNNs for structured e-waste data, with significantly faster training.",
            "methodology": "Train RF, XGBoost, MobileNetV3 on matched dataset. Compare F1, accuracy, training time, inference latency.",
            "status": "planned",
        },
        {
            "experiment_code": "EXP-003-RECOVERY-VALIDATION",
            "experiment_name": "Recovery Quantity Estimation Validation",
            "research_question": "How closely do AI-estimated material quantities match physically measured recovery data?",
            "hypothesis": "AI estimates derived from device classification will be within 15% of measured material quantities for high-volume streams.",
            "methodology": "Process 50+ device batches. Compare estimated vs. actual recovery weights. Calculate MAPE.",
            "status": "planned",
        },
    ]

    seeded = 0
    for exp_data in sample_experiments:
        exists = session.query(ResearchExperiment).filter_by(
            experiment_code=exp_data["experiment_code"]
        ).first()
        if not exists:
            session.add(ResearchExperiment(**exp_data))
            seeded += 1

    logger.info(f"Research experiments: seeded {seeded} sample experiments.")
    return seeded


def main():
    from backend.database import engine, init_db
    from backend.models import (
        Dataset, DatasetVersion, CleaningRun, PreprocessingConfig,
        TrainingRun, ModelEvaluation, Prediction,
        WasteBatch, BatchItem, ItemClassification, ItemComponent,
        MaterialRecovery, EconomicValuation, OperationalCost, EwasteCategory,
        ResearchExperiment, ExperimentRun, ExperimentMetric,
        BaselineComparison, ResearchReport,
    )
    from sqlalchemy.orm import Session

    # Ensure tables exist
    init_db()

    categories_file = PROJECT_ROOT / "config" / "ewaste_categories.json"

    with Session(engine) as session:
        try:
            n_cats = seed_categories(session, categories_file)
            n_exps = seed_research_experiments(session)
            session.commit()

            print(f"\n✓ Seeding complete:")
            print(f"  E-waste categories: {n_cats} seeded")
            print(f"  Research experiments: {n_exps} seeded")

        except Exception as e:
            session.rollback()
            logger.error(f"Seeding failed, rolled back: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    main()
