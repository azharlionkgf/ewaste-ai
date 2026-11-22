"""
scripts/verify_foundation.py
E-WASTE AI - Phase 1 Foundation Verification Script
Comprehensive check of all Phase 1 deliverables.
"""

import sys
import json
import importlib
import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.WARNING)  # Suppress noisy logs during checks

# ANSI colours (Windows 10+ supports these in modern terminals)
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

PASS = f"{GREEN}✓{RESET}"
FAIL = f"{RED}✗{RESET}"

passed = 0
failed = 0
results = []


def check(label: str, condition: bool, detail: str = ""):
    global passed, failed
    status = PASS if condition else FAIL
    line = f"  {status} {label}"
    if detail and not condition:
        line += f"  ({RED}{detail}{RESET})"
    elif detail and condition:
        line += f"  {CYAN}({detail}){RESET}"
    results.append(line)
    if condition:
        passed += 1
    else:
        failed += 1
    return condition


def section(title: str):
    results.append(f"\n{BOLD}{CYAN}{title}{RESET}")


# ===========================================================================
# 1. REQUIRED DIRECTORIES
# ===========================================================================
section("1. Required Directories")

REQUIRED_DIRS = [
    "backend", "backend/api", "backend/middleware", "backend/models",
    "backend/routers", "backend/schemas", "backend/services", "backend/utils",
    "data/raw", "data/cleaned", "data/augmented", "data/splits",
    "data/images", "data/uploads", "data/videos", "data/annotations",
    "docs", "ewaste",
    "frontend", "frontend/pages", "frontend/components",
    "industrial", "industrial/inventory", "industrial/operations",
    "industrial/compliance", "industrial/valuation",
    "intelligence",
    "ml/data/loaders", "ml/data/augmentation",
    "ml/models/cnn", "ml/models/tabular",
    "ml/training", "ml/inference", "ml/evaluation", "ml/pipeline", "ml/utils",
    "notebooks", "research/experiments", "research/baselines",
    "research/results", "research/charts", "research/papers",
    "reports", "saved_models",
    "scripts", "tests", "config", "database", "logs", "migrations",
]

for d in REQUIRED_DIRS:
    p = PROJECT_ROOT / d
    check(d, p.exists(), f"missing: {p}")

# ===========================================================================
# 2. REQUIRED FILES
# ===========================================================================
section("2. Required Files")

REQUIRED_FILES = [
    # Root config
    "app.py", "requirements.txt", "config.yaml", ".gitignore", ".env.example",
    "README.md", "TASK_STATUS.md",
    # Backend
    "backend/__init__.py", "backend/main.py", "backend/config.py",
    "backend/database.py", "backend/logger.py",
    # Backend models
    "backend/models/__init__.py", "backend/models/base.py",
    "backend/models/dataset.py", "backend/models/ml_model.py",
    "backend/models/waste_batch.py", "backend/models/research.py",
    # Backend schemas
    "backend/schemas/__init__.py", "backend/schemas/dataset.py",
    "backend/schemas/training.py",
    # ML pipeline
    "ml/data/loaders/dataset_loader.py", "ml/data/loaders/cleaner.py",
    "ml/data/loaders/preprocessor.py", "ml/data/loaders/image_dataset.py",
    "ml/models/cnn/classifier.py", "ml/models/tabular/classifier.py",
    "ml/training/trainer.py", "ml/training/callbacks.py",
    "ml/inference/predictor.py", "ml/evaluation/metrics.py",
    "ml/models/model_registry.py",
    # Intelligence
    "intelligence/device_database.py", "intelligence/material_database.py",
    "intelligence/recovery_engine.py", "intelligence/economic_engine.py",
    "intelligence/environmental_engine.py",
    # Research
    "research/experiments/experiment_tracker.py",
    "research/baselines/baseline_registry.py",
    # Industrial
    "industrial/inventory/batch_manager.py",
    "industrial/operations/classification_workflow.py",
    "industrial/compliance/hazmat_rules.py",
    "industrial/valuation/cost_calculator.py",
    # Config data
    "config/ewaste_categories.json", "config/material_prices.json",
    # Scripts
    "scripts/init_db.py", "scripts/seed_db.py",
    "scripts/verify_foundation.py", "scripts/check_env.py",
    # Docs
    "docs/PROJECT_ARCHITECTURE.md", "docs/TECHNOLOGY_STACK.md",
    "docs/DATABASE_DESIGN.md", "docs/RESEARCH_ARCHITECTURE.md",
    "docs/DEVELOPMENT_ROADMAP.md", "docs/AI_ML_ARCHITECTURE.md",
    "docs/INDUSTRIAL_WORKFLOW.md",
    # Frontend
    "frontend/theme.py", "frontend/pages/__init__.py",
    "frontend/pages/dashboard.py", "frontend/components/sidebar.py",
    # Tests
    "tests/__init__.py", "tests/test_foundation.py",
    # Streamlit
    ".streamlit/config.toml",
]

for f in REQUIRED_FILES:
    p = PROJECT_ROOT / f
    check(f, p.exists(), f"missing: {p}")

# ===========================================================================
# 3. IMPORT TESTS
# ===========================================================================
section("3. Python Module Imports")

MODULES = [
    ("backend.config", "Settings"),
    ("backend.database", "engine"),
    ("backend.models", "Dataset"),
    ("backend.models.base", "TimestampMixin"),
    ("backend.models.dataset", "Dataset"),
    ("backend.models.ml_model", "TrainingRun"),
    ("backend.models.waste_batch", "WasteBatch"),
    ("backend.models.research", "ResearchExperiment"),
    ("backend.schemas.dataset", "DatasetCreate"),
    ("backend.schemas.training", "TrainingRequest"),
    ("ml.data.loaders.dataset_loader", "load_tabular_dataset"),
    ("ml.data.loaders.cleaner", "DataCleaner"),
    ("ml.data.loaders.preprocessor", "DataPreprocessor"),
    ("ml.data.loaders.image_dataset", "EwasteImageDataset"),
    ("ml.models.cnn.classifier", "build_cnn_classifier"),
    ("ml.models.tabular.classifier", "build_tabular_classifier"),
    ("ml.training.trainer", "ModelTrainer"),
    ("ml.training.callbacks", "EarlyStopping"),
    ("ml.inference.predictor", "ModelPredictor"),
    ("ml.evaluation.metrics", "compute_classification_metrics"),
    ("ml.models.model_registry", "get_all_models"),
    ("intelligence.device_database", None),
    ("intelligence.material_database", None),
    ("intelligence.recovery_engine", None),
    ("intelligence.economic_engine", None),
    ("research.experiments.experiment_tracker", "ExperimentTracker"),
    ("research.baselines.baseline_registry", "BaselineRegistry"),
    ("industrial.inventory.batch_manager", "BatchManager"),
    ("industrial.operations.classification_workflow", "ClassificationWorkflow"),
    ("industrial.compliance.hazmat_rules", "HazmatChecker"),
    ("industrial.valuation.cost_calculator", "CostCalculator"),
]

for mod_name, attr in MODULES:
    try:
        mod = importlib.import_module(mod_name)
        if attr:
            has_attr = hasattr(mod, attr)
            check(f"import {mod_name}.{attr}", has_attr, f"missing attr '{attr}'")
        else:
            check(f"import {mod_name}", True)
    except Exception as e:
        check(f"import {mod_name}", False, str(e)[:80])

# ===========================================================================
# 4. DATABASE TEST
# ===========================================================================
section("4. Database Initialisation")

try:
    from backend.database import engine, init_db, Base
    from backend.models import (
        Dataset, TrainingRun, WasteBatch, EwasteCategory, ResearchExperiment
    )
    init_db()
    from sqlalchemy import inspect as sa_inspect
    inspector = sa_inspect(engine)
    tables = inspector.get_table_names()
    check("Database tables created", len(tables) > 0, f"{len(tables)} tables")
    for required_table in ["datasets", "training_runs", "waste_batches", "ewaste_categories", "research_experiments"]:
        check(f"Table '{required_table}' exists", required_table in tables)
except Exception as e:
    check("Database initialisation", False, str(e)[:100])

# ===========================================================================
# 5. CONFIG FILES
# ===========================================================================
section("5. Config Data Files")

try:
    cats_file = PROJECT_ROOT / "config" / "ewaste_categories.json"
    with open(cats_file, encoding="utf-8") as f:
        cats = json.load(f)
    check("ewaste_categories.json loads", True)
    check("Has 15 e-waste categories", len(cats) == 15, f"found {len(cats)}")
    has_required_fields = all(
        "category_code" in c and "name" in c and "key_materials" in c
        for c in cats
    )
    check("Categories have required fields", has_required_fields)
except Exception as e:
    check("ewaste_categories.json", False, str(e))

try:
    prices_file = PROJECT_ROOT / "config" / "material_prices.json"
    with open(prices_file, encoding="utf-8") as f:
        prices = json.load(f)
    check("material_prices.json loads", True)
    check("Has at least 10 materials", len(prices) >= 10, f"found {len(prices)}")
    check("Gold price present", "gold" in prices)
    check("All prices labeled is_estimate", all(v.get("is_estimate") for v in prices.values()))
except Exception as e:
    check("material_prices.json", False, str(e))

# ===========================================================================
# 6. FUNCTIONAL TESTS
# ===========================================================================
section("6. Functional Module Tests")

# ExperimentTracker
try:
    from research.experiments.experiment_tracker import ExperimentTracker
    tracker = ExperimentTracker()
    exp = tracker.create_experiment("Test Exp", "desc", "hyp", "meth")
    run_id = tracker.start_run(exp["id"], {"lr": 0.001}, "random_forest")
    tracker.log_metric(run_id, "accuracy", 0.85, epoch=1)
    tracker.finish_run(run_id)
    comparison = tracker.compare_runs(exp["id"])
    check("ExperimentTracker full workflow", comparison["total_runs"] == 1)
except Exception as e:
    check("ExperimentTracker full workflow", False, str(e)[:80])

# BatchManager
try:
    from industrial.inventory.batch_manager import BatchManager
    bm = BatchManager()
    batch = bm.register_batch("Test Source", weight_kg=50.0, item_count=10)
    bm.add_item_to_batch(batch["id"], "smartphone", brand="Samsung")
    bm.update_batch_status(batch["id"], "assessed")
    summary = bm.get_batch_summary(batch["id"])
    check("BatchManager full workflow", summary["total_items_registered"] == 1)
except Exception as e:
    check("BatchManager full workflow", False, str(e)[:80])

# CostCalculator
try:
    from industrial.valuation.cost_calculator import CostCalculator
    calc = CostCalculator()
    result = calc.estimate_recovery_value("smartphone", quantity=10)
    check("CostCalculator recovery estimate", result["is_estimate"] is True)
    net = calc.calculate_net_value("laptop", quantity=5, weight_kg=2.0)
    check("CostCalculator net value", "net_value_usd" in net)
except Exception as e:
    check("CostCalculator", False, str(e)[:80])

# HazmatChecker
try:
    from industrial.compliance.hazmat_rules import HazmatChecker
    hc = HazmatChecker()
    report = hc.check_device("laptop")
    check("HazmatChecker device check", len(report["hazmat_materials_present"]) > 0)
except Exception as e:
    check("HazmatChecker", False, str(e)[:80])

# BaselineRegistry
try:
    from research.baselines.baseline_registry import BaselineRegistry
    reg = BaselineRegistry()
    baselines = reg.list_baselines()
    check("BaselineRegistry lists baselines", len(baselines) >= 5)
    table = reg.generate_comparison_table([
        {"model_name": "RF", "accuracy": 0.82, "f1": 0.80}
    ])
    check("BaselineRegistry markdown table", "|" in table)
except Exception as e:
    check("BaselineRegistry", False, str(e)[:80])

# ===========================================================================
# SUMMARY
# ===========================================================================
print()
print("=" * 60)
print(f"{BOLD}E-WASTE AI — Phase 1 Verification Report{RESET}")
print("=" * 60)

for line in results:
    print(line)

total = passed + failed
print()
print("=" * 60)
print(f"  Checks passed: {GREEN}{passed}{RESET} / {total}")
if failed > 0:
    print(f"  Checks failed: {RED}{failed}{RESET} / {total}")
    print(f"\n{RED}Phase 1 verification INCOMPLETE — fix failed checks above.{RESET}")
else:
    print(f"\n{GREEN}{BOLD}✓ ALL {total} CHECKS PASSED — Phase 1 Foundation Complete!{RESET}")
print("=" * 60)

sys.exit(0 if failed == 0 else 1)
