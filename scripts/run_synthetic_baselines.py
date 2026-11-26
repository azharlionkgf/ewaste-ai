"""
scripts/run_synthetic_baselines.py
E-WASTE AI — Phase 3 Synthetic Baseline Experiment
====================================================
Runs actual training on synthetic data to verify the pipeline works end-to-end.
Records real metrics — these are the Phase 3 research experiment baselines.

IMPORTANT: These results are from SYNTHETIC data, not from real e-waste datasets.
They are recorded for pipeline verification only, not as research results.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
from sklearn.datasets import make_classification, make_regression
from sklearn.model_selection import train_test_split

from ml.training.training_engine import TrainingEngine
from ml.evaluation.evaluator import compare_models
from ml.models.model_version_registry import ModelRegistry
from research.experiments.experiment_tracker import ExperimentTracker

SEED = 42
print("=" * 65)
print("E-WASTE AI — Phase 3 Synthetic Baseline Experiment")
print("NOTE: All results below are from SYNTHETIC data (not real datasets)")
print("=" * 65)

# ---------------------------------------------------------------------------
# 1. Classification experiment (3-class, 200 samples)
# ---------------------------------------------------------------------------
print("\n--- CLASSIFICATION: 3-class, 200 synthetic samples ---")

X, y = make_classification(
    n_samples=200, n_features=10, n_informative=6,
    n_redundant=0, n_repeated=0,
    n_classes=3, n_clusters_per_class=1,
    random_state=SEED,
)
X_tmp, X_test, y_tmp, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_tmp, y_tmp, test_size=0.2, random_state=SEED, stratify=y_tmp)

print(f"  Train: {len(X_train)} | Val: {len(X_val)} | Test: {len(X_test)}")

engine = TrainingEngine(seed=SEED)
tracker = ExperimentTracker()
registry = ModelRegistry()

clf_algorithms = ["random_forest", "logistic_regression", "hist_gradient_boosting", "extra_trees"]
clf_results = []

for algo in clf_algorithms:
    result = engine.train_tabular(
        X_train, y_train, X_val, y_val,
        algorithm=algo, task="classification",
        run_name=f"synthetic_clf_{algo}",
    )
    val_acc = result["val_metrics"].get("accuracy", 0)
    val_f1  = result["val_metrics"].get("f1_macro", 0)
    t_sec   = result.get("training_time_s", result.get("duration_sec", 0))
    print(f"  {algo:30s}  val_acc={val_acc:.4f}  val_f1={val_f1:.4f}  t={t_sec:.2f}s")

    # Register model
    registry.register(
        run_name=f"synthetic_clf_{algo}",
        model_path=result.get("model_path", ""),
        metadata={
            "algorithm": algo,
            "task": "classification",
            "train_metrics": result["train_metrics"],
            "val_metrics": result["val_metrics"],
            "seed": SEED,
            "dataset_name": "synthetic_200x10_3class",
            "dataset_version": "synthetic_v1",
        }
    )
    clf_results.append(result)

    # Track experiment
    exp_id = tracker.start_experiment(
        name=f"Synthetic CLF — {algo}",
        objective="Pipeline verification on synthetic 3-class data",
        dataset_info={"source": "synthetic", "n_samples": 200, "n_features": 10, "n_classes": 3},
        config={"algorithm": algo, "seed": SEED},
    )
    tracker.log_metrics(exp_id, {
        "val_accuracy": val_acc,
        "val_f1_macro": val_f1,
        "training_time_sec": t_sec,
    })
    tracker.end_experiment(exp_id, status="completed")

# Compare
comparison = compare_models(clf_results)
best = comparison["best_model"]
print(f"\n  Best (val f1_macro): {best.get('algorithm','?')} = {best.get('val_f1_macro', best.get('val_f1','?'))}")

# ---------------------------------------------------------------------------
# 2. Regression experiment
# ---------------------------------------------------------------------------
print("\n--- REGRESSION: 150 synthetic samples ---")

Xr, yr = make_regression(n_samples=150, n_features=8, noise=0.1, random_state=SEED)
Xr_tmp, Xr_test, yr_tmp, yr_test = train_test_split(Xr, yr, test_size=0.2, random_state=SEED)
Xr_train, Xr_val, yr_train, yr_val = train_test_split(Xr_tmp, yr_tmp, test_size=0.2, random_state=SEED)

reg_algorithms = ["random_forest", "hist_gradient_boosting", "extra_trees"]

for algo in reg_algorithms:
    result = engine.train_tabular(
        Xr_train, yr_train, Xr_val, yr_val,
        algorithm=algo, task="regression",
        run_name=f"synthetic_reg_{algo}",
    )
    val_mae = result["val_metrics"].get("mae", 0)
    val_r2  = result["val_metrics"].get("r2", 0)
    t_sec   = result.get("training_time_s", result.get("duration_sec", 0))
    print(f"  {algo:30s}  val_mae={val_mae:.4f}  val_r2={val_r2:.4f}  t={t_sec:.2f}s")

print("\n" + "=" * 65)
print("SYNTHETIC BASELINE EXPERIMENT COMPLETE")
print("All metrics above are from synthetic data — NOT from real e-waste datasets.")
print("=" * 65)
