"""
Model Evaluator — Phase 3: AI/ML Training Laboratory
======================================================
Unified evaluation for tabular (classification + regression) and CNN models.
Extends Phase 1 ml/evaluation/metrics.py.
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)


def evaluate_tabular(
    model,
    X: np.ndarray,
    y: np.ndarray,
    task: str = "classification",
    split: str = "test",
    class_names: list[str] | None = None,
) -> dict:
    """
    Full evaluation for tabular model on a dataset split.

    Returns dict with all metrics appropriate for classification or regression.
    """
    y_pred = model.predict(X)
    y_proba = None
    if task == "classification" and hasattr(model, "predict_proba"):
        try:
            y_proba = model.predict_proba(X)
        except Exception:
            pass

    if task == "classification":
        return _classification_metrics(y, y_pred, y_proba, class_names, split)
    else:
        return _regression_metrics(y, y_pred, split)


def _classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: np.ndarray | None,
    class_names: list[str] | None,
    split: str,
) -> dict:
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score,
        confusion_matrix, classification_report, cohen_kappa_score,
        roc_auc_score, average_precision_score,
    )

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    n_classes = len(np.unique(y_true))
    avg = "binary" if n_classes == 2 else "macro"

    metrics: dict[str, Any] = {
        "split":     split,
        "task":      "classification",
        "n_samples": int(len(y_true)),
        "n_classes": n_classes,
        "accuracy":  round(float(accuracy_score(y_true, y_pred)), 4),
        "precision": round(float(precision_score(y_true, y_pred, average=avg, zero_division=0)), 4),
        "recall":    round(float(recall_score(y_true, y_pred, average=avg, zero_division=0)), 4),
        "f1_macro":  round(float(f1_score(y_true, y_pred, average="macro", zero_division=0)), 4),
        "f1_weighted": round(float(f1_score(y_true, y_pred, average="weighted", zero_division=0)), 4),
        "kappa":     round(float(cohen_kappa_score(y_true, y_pred)), 4),
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
    }

    # ROC-AUC
    if y_proba is not None:
        try:
            if n_classes == 2:
                metrics["roc_auc"] = round(float(roc_auc_score(y_true, y_proba[:, 1])), 4)
                metrics["pr_auc"]  = round(float(average_precision_score(y_true, y_proba[:, 1])), 4)
            else:
                metrics["roc_auc"] = round(float(
                    roc_auc_score(y_true, y_proba, multi_class="ovr", average="macro")
                ), 4)
        except Exception as exc:
            logger.debug("ROC-AUC skipped: %s", exc)

    # Per-class report
    names = class_names or [str(c) for c in sorted(np.unique(y_true))]
    try:
        report = classification_report(y_true, y_pred, target_names=names,
                                       output_dict=True, zero_division=0)
        metrics["per_class"] = {
            k: {mk: round(mv, 4) for mk, mv in v.items()}
            for k, v in report.items()
            if isinstance(v, dict)
        }
    except Exception:
        pass

    return metrics


def _regression_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    split: str,
) -> dict:
    from sklearn.metrics import (
        mean_absolute_error, mean_squared_error, r2_score,
        mean_absolute_percentage_error,
    )

    y_true = np.array(y_true, dtype=float)
    y_pred = np.array(y_pred, dtype=float)
    mse = float(mean_squared_error(y_true, y_pred))

    metrics: dict[str, Any] = {
        "split":     split,
        "task":      "regression",
        "n_samples": int(len(y_true)),
        "mae":       round(float(mean_absolute_error(y_true, y_pred)), 4),
        "mse":       round(mse, 4),
        "rmse":      round(float(np.sqrt(mse)), 4),
        "r2":        round(float(r2_score(y_true, y_pred)), 4),
    }
    try:
        metrics["mape"] = round(float(mean_absolute_percentage_error(y_true, y_pred)) * 100, 2)
    except Exception:
        pass

    return metrics


# ---------------------------------------------------------------------------
# Cross-validation helper
# ---------------------------------------------------------------------------

def cross_validate_model(
    model,
    X: np.ndarray,
    y: np.ndarray,
    task: str = "classification",
    cv: int = 5,
    seed: int = 42,
) -> dict:
    """Run K-Fold cross-validation; returns mean ± std metrics."""
    from sklearn.model_selection import StratifiedKFold, KFold, cross_validate
    from sklearn.metrics import make_scorer, accuracy_score, f1_score, r2_score, mean_absolute_error

    if task == "classification":
        kfold = StratifiedKFold(n_splits=cv, shuffle=True, random_state=seed)
        scoring = {
            "accuracy": make_scorer(accuracy_score),
            "f1_macro": make_scorer(f1_score, average="macro", zero_division=0),
        }
    else:
        kfold = KFold(n_splits=cv, shuffle=True, random_state=seed)
        scoring = {
            "r2":  make_scorer(r2_score),
            "mae": make_scorer(mean_absolute_error),
        }

    cv_results = cross_validate(
        model, X, y, cv=kfold, scoring=scoring, n_jobs=-1,
        return_train_score=True,
    )

    summary: dict[str, Any] = {"cv_folds": cv, "task": task}
    for key, vals in cv_results.items():
        if key.startswith("test_") or key.startswith("train_"):
            metric = key
            summary[f"{metric}_mean"] = round(float(np.mean(vals)), 4)
            summary[f"{metric}_std"]  = round(float(np.std(vals)),  4)

    return summary


# ---------------------------------------------------------------------------
# Comparison helper
# ---------------------------------------------------------------------------

def compare_models(results: list[dict]) -> dict:
    """
    Compare multiple training results.

    Parameters
    ----------
    results: list of dicts from TrainingEngine.train_tabular()

    Returns
    -------
    dict with sorted comparison table and best-model recommendation
    """
    rows = []
    for r in results:
        val = r.get("val_metrics", {})
        train = r.get("train_metrics", {})

        task = r.get("task", "classification")
        if task == "classification":
            val_score   = val.get("f1_macro", val.get("accuracy", 0))
            train_score = train.get("f1_macro", train.get("accuracy", 0))
            metric_name = "f1_macro"
        else:
            val_score   = val.get("r2", 0)
            train_score = train.get("r2", 0)
            metric_name = "r2"

        overfit_gap = round(train_score - val_score, 4)
        rows.append({
            "run_name":        r.get("run_name", "?"),
            "algorithm":       r.get("algorithm", "?"),
            "task":            task,
            f"val_{metric_name}":   round(val_score, 4),
            f"train_{metric_name}": round(train_score, 4),
            "overfit_gap":     overfit_gap,
            "overfit_flag":    overfit_gap > 0.15,
            "training_time_s": r.get("training_time_s", 0),
            "val_accuracy":    val.get("accuracy", None),
        })

    rows_sorted = sorted(rows, key=lambda x: x.get(f"val_{metric_name}", 0), reverse=True)

    best = rows_sorted[0] if rows_sorted else {}
    recommendation = (
        f"Best model: {best.get('algorithm','?')} "
        f"(val {metric_name}={best.get(f'val_{metric_name}','?')}). "
        f"Overfit gap={best.get('overfit_gap','?')} "
        f"({'⚠️ overfitting' if best.get('overfit_flag') else '✅ OK'})."
    )

    return {
        "comparison_table": rows_sorted,
        "best_model":       best,
        "metric_used":      metric_name,
        "recommendation":   recommendation,
        "n_models":         len(rows),
    }
