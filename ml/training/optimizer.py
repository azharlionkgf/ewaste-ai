"""
Model Optimizer — Phase 3: AI/ML Training Laboratory
======================================================
Hyperparameter tuning, cross-validation, class-imbalance handling.
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)


class ModelOptimizer:
    """
    Hyperparameter search and cross-validation wrapper.

    Usage::

        optimizer = ModelOptimizer()
        best_model, best_params = optimizer.tune(
            algorithm="random_forest", X_train, y_train,
            task="classification", method="random"
        )
    """

    # Reasonable CPU-safe search spaces
    SEARCH_SPACES = {
        "random_forest": {
            "n_estimators":     [50, 100, 200],
            "max_depth":        [None, 5, 10, 20],
            "min_samples_split":[2, 5, 10],
            "class_weight":     ["balanced", None],
        },
        "extra_trees": {
            "n_estimators":     [50, 100, 200],
            "max_depth":        [None, 5, 10],
            "class_weight":     ["balanced", None],
        },
        "logistic_regression": {
            "C":        [0.01, 0.1, 1.0, 10.0],
            "max_iter": [500, 1000],
        },
        "svm": {
            "C":      [0.1, 1.0, 10.0],
            "kernel": ["rbf", "linear"],
        },
        "gradient_boosting": {
            "n_estimators":  [50, 100],
            "learning_rate": [0.05, 0.1, 0.2],
            "max_depth":     [3, 5],
        },
        "hist_gradient_boosting": {
            "max_iter":      [50, 100],
            "learning_rate": [0.05, 0.1],
        },
        "xgboost": {
            "n_estimators":  [50, 100],
            "learning_rate": [0.05, 0.1],
            "max_depth":     [4, 6],
        },
        "knn": {
            "n_neighbors": [3, 5, 7, 11],
            "weights":     ["uniform", "distance"],
        },
        "decision_tree": {
            "max_depth":        [None, 5, 10, 20],
            "min_samples_split":[2, 5, 10],
        },
    }

    def tune(
        self,
        algorithm: str,
        X_train: np.ndarray,
        y_train: np.ndarray,
        task: str = "classification",
        method: str = "random",          # "random" | "grid"
        n_iter: int = 20,
        cv: int = 3,
        seed: int = 42,
    ) -> tuple[Any, dict]:
        """
        Tune hyperparameters for the given algorithm.

        Returns (best_fitted_model, best_params_dict).
        """
        from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

        space = self.SEARCH_SPACES.get(algorithm, {})
        if not space:
            logger.warning("No search space defined for '%s'; using defaults", algorithm)
            from ml.models.tabular.sklearn_models import build_tabular_classifier, build_tabular_regressor
            if task == "classification":
                model = build_tabular_classifier(algorithm, {}, seed)
            else:
                model = build_tabular_regressor(algorithm, {}, seed)
            model.fit(X_train, y_train)
            return model, {}

        scoring = "f1_macro" if task == "classification" else "r2"

        from ml.models.tabular.sklearn_models import build_tabular_classifier, build_tabular_regressor
        if task == "classification":
            base_model = build_tabular_classifier(algorithm, {}, seed)
        else:
            base_model = build_tabular_regressor(algorithm, {}, seed)

        if method == "grid":
            search = GridSearchCV(
                base_model, space, scoring=scoring, cv=cv, n_jobs=-1, refit=True,
            )
        else:
            search = RandomizedSearchCV(
                base_model, space, n_iter=min(n_iter, _param_count(space)),
                scoring=scoring, cv=cv, n_jobs=-1, random_state=seed, refit=True,
            )

        logger.info("Tuning %s via %s (cv=%d, n_iter=%d)...", algorithm, method, cv, n_iter)
        search.fit(X_train, y_train)
        logger.info("Best params: %s  score=%.4f", search.best_params_, search.best_score_)

        return search.best_estimator_, search.best_params_

    @staticmethod
    def handle_class_imbalance(
        X: np.ndarray,
        y: np.ndarray,
        strategy: str = "auto",
        seed: int = 42,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Handle class imbalance.

        strategy: "none" | "smote" | "oversample" | "auto"
        Returns (X_resampled, y_resampled).
        """
        from collections import Counter
        counts = Counter(y)
        max_count = max(counts.values())
        min_count = min(counts.values())
        ratio = max_count / max(min_count, 1)

        if strategy == "none" or ratio < 2.0:
            return X, y

        if strategy in ("smote", "auto"):
            try:
                from imblearn.over_sampling import SMOTE
                sm = SMOTE(random_state=seed)
                X_res, y_res = sm.fit_resample(X, y)
                logger.info("SMOTE applied: %d → %d samples", len(y), len(y_res))
                return X_res, y_res
            except ImportError:
                logger.info("imbalanced-learn not installed; using class_weight='balanced'")
                return X, y

        if strategy == "oversample":
            try:
                from imblearn.over_sampling import RandomOverSampler
                ros = RandomOverSampler(random_state=seed)
                X_res, y_res = ros.fit_resample(X, y)
                return X_res, y_res
            except ImportError:
                # Fallback: manual numpy random oversampling
                rng = np.random.RandomState(seed)
                parts_X = [X]
                parts_y = [y]
                for cls, cnt in counts.items():
                    if cnt < max_count:
                        idx = np.where(y == cls)[0]
                        n_extra = max_count - cnt
                        extra_idx = rng.choice(idx, size=n_extra, replace=True)
                        parts_X.append(X[extra_idx])
                        parts_y.append(y[extra_idx])
                X_res = np.vstack(parts_X)
                y_res = np.concatenate(parts_y)
                logger.info("Manual oversample: %d → %d samples", len(y), len(y_res))
                return X_res, y_res

        return X, y


def _param_count(space: dict) -> int:
    """Total combinations in a search space."""
    total = 1
    for v in space.values():
        total *= len(v)
    return total
