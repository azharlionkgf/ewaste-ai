"""
E-Waste AI — Traditional ML Models
=====================================
Unified wrapper for scikit-learn, XGBoost, and CatBoost classifiers.
All models follow the same .fit() / .predict() / .predict_proba() interface.

Training happens in Phase 4. This module defines wrappers only.
"""

import numpy as np
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)


SUPPORTED_ALGORITHMS = {
    "random_forest":       "sklearn.ensemble.RandomForestClassifier",
    "xgboost":             "xgboost.XGBClassifier",
    "catboost":            "catboost.CatBoostClassifier",
    "svm":                 "sklearn.svm.SVC",
    "logistic_regression": "sklearn.linear_model.LogisticRegression",
}


def build_tabular_classifier(
    algorithm: str,
    hyperparams: Optional[Dict[str, Any]] = None,
    num_classes: int = 2,
    random_seed: int = 42,
):
    """
    Build a traditional ML classifier with given hyperparameters.

    Args:
        algorithm:    One of SUPPORTED_ALGORITHMS keys
        hyperparams:  Dict of algorithm-specific hyperparameters
        num_classes:  Number of output classes
        random_seed:  Random state for reproducibility

    Returns:
        Fitted-ready sklearn-compatible estimator
    """
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(
            f"Unsupported algorithm: '{algorithm}'. "
            f"Choose from: {list(SUPPORTED_ALGORITHMS.keys())}"
        )

    hp = hyperparams or {}
    logger.info(f"Building {algorithm} | seed={random_seed} | classes={num_classes}")

    if algorithm == "random_forest":
        from sklearn.ensemble import RandomForestClassifier
        return RandomForestClassifier(
            n_estimators=hp.get("n_estimators", 100),
            max_depth=hp.get("max_depth", None),
            min_samples_split=hp.get("min_samples_split", 2),
            min_samples_leaf=hp.get("min_samples_leaf", 1),
            class_weight=hp.get("class_weight", "balanced"),
            n_jobs=-1,
            random_state=random_seed,
        )

    elif algorithm == "xgboost":
        from xgboost import XGBClassifier
        return XGBClassifier(
            n_estimators=hp.get("n_estimators", 100),
            max_depth=hp.get("max_depth", 6),
            learning_rate=hp.get("learning_rate", 0.1),
            subsample=hp.get("subsample", 0.8),
            colsample_bytree=hp.get("colsample_bytree", 0.8),
            use_label_encoder=False,
            eval_metric="mlogloss",
            tree_method="hist",
            device="cpu",
            random_state=random_seed,
        )

    elif algorithm == "catboost":
        from catboost import CatBoostClassifier
        return CatBoostClassifier(
            iterations=hp.get("n_estimators", 100),
            depth=hp.get("max_depth", 6),
            learning_rate=hp.get("learning_rate", 0.1),
            loss_function="MultiClass" if num_classes > 2 else "Logloss",
            eval_metric="Accuracy",
            verbose=False,
            random_seed=random_seed,
        )

    elif algorithm == "svm":
        from sklearn.svm import SVC
        return SVC(
            C=hp.get("C", 1.0),
            kernel=hp.get("kernel", "rbf"),
            probability=True,     # needed for predict_proba
            class_weight="balanced",
            random_state=random_seed,
        )

    elif algorithm == "logistic_regression":
        from sklearn.linear_model import LogisticRegression
        return LogisticRegression(
            C=hp.get("C", 1.0),
            max_iter=hp.get("max_iter", 1000),
            multi_class="auto",
            class_weight="balanced",
            solver="lbfgs",
            n_jobs=-1,
            random_state=random_seed,
        )


def save_tabular_model(model, path: str, metadata: Optional[Dict] = None) -> None:
    """Serialize a trained sklearn/XGBoost/CatBoost model to disk."""
    import joblib
    import json
    import os

    joblib.dump(model, path)
    if metadata:
        meta_path = path.replace(".joblib", "_metadata.json")
        with open(meta_path, "w") as f:
            json.dump(metadata, f, indent=2, default=str)
    logger.info(f"Model saved → {path}")


def load_tabular_model(path: str):
    """Load a serialized model from disk."""
    import joblib
    model = joblib.load(path)
    logger.info(f"Model loaded ← {path}")
    return model
