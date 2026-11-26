"""
Sklearn Models — Phase 3: AI/ML Training Laboratory
=====================================================
Builds all tabular classifiers and regressors.
Extends the Phase 1 stub in ml/models/tabular/classifier.py.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# CLASSIFIERS
# ---------------------------------------------------------------------------

def build_tabular_classifier(algorithm: str, cfg: dict, seed: int = 42):
    """Return a fitted-ready sklearn-compatible classifier."""
    algo = algorithm.lower()

    if algo == "logistic_regression":
        from sklearn.linear_model import LogisticRegression
        # multi_class removed in scikit-learn 1.5+
        return LogisticRegression(
            C=cfg.get("C", 1.0),
            max_iter=cfg.get("max_iter", 1000),
            random_state=seed,
            solver="lbfgs",
        )

    if algo == "decision_tree":
        from sklearn.tree import DecisionTreeClassifier
        return DecisionTreeClassifier(
            max_depth=cfg.get("max_depth", None),
            min_samples_split=cfg.get("min_samples_split", 2),
            random_state=seed,
        )

    if algo == "random_forest":
        from sklearn.ensemble import RandomForestClassifier
        return RandomForestClassifier(
            n_estimators=cfg.get("n_estimators", 100),
            max_depth=cfg.get("max_depth", None),
            min_samples_split=cfg.get("min_samples_split", 2),
            class_weight=cfg.get("class_weight", "balanced"),
            random_state=seed,
            n_jobs=-1,
        )

    if algo == "extra_trees":
        from sklearn.ensemble import ExtraTreesClassifier
        return ExtraTreesClassifier(
            n_estimators=cfg.get("n_estimators", 100),
            max_depth=cfg.get("max_depth", None),
            class_weight=cfg.get("class_weight", "balanced"),
            random_state=seed,
            n_jobs=-1,
        )

    if algo == "svm":
        from sklearn.svm import SVC
        return SVC(
            C=cfg.get("C", 1.0),
            kernel=cfg.get("kernel", "rbf"),
            probability=True,
            class_weight=cfg.get("class_weight", "balanced"),
            random_state=seed,
        )

    if algo == "knn":
        from sklearn.neighbors import KNeighborsClassifier
        return KNeighborsClassifier(
            n_neighbors=cfg.get("n_neighbors", 5),
            weights=cfg.get("weights", "uniform"),
            n_jobs=-1,
        )

    if algo == "gradient_boosting":
        from sklearn.ensemble import GradientBoostingClassifier
        return GradientBoostingClassifier(
            n_estimators=cfg.get("n_estimators", 100),
            learning_rate=cfg.get("learning_rate", 0.1),
            max_depth=cfg.get("max_depth", 3),
            random_state=seed,
        )

    if algo == "hist_gradient_boosting":
        from sklearn.ensemble import HistGradientBoostingClassifier
        return HistGradientBoostingClassifier(
            max_iter=cfg.get("max_iter", 100),
            learning_rate=cfg.get("learning_rate", 0.1),
            max_depth=cfg.get("max_depth", None),
            random_state=seed,
        )

    if algo == "xgboost":
        try:
            from xgboost import XGBClassifier
            return XGBClassifier(
                n_estimators=cfg.get("n_estimators", 100),
                learning_rate=cfg.get("learning_rate", 0.1),
                max_depth=cfg.get("max_depth", 6),
                use_label_encoder=False,
                eval_metric="mlogloss",
                random_state=seed,
                n_jobs=-1,
                verbosity=0,
            )
        except ImportError:
            logger.warning("XGBoost not installed, falling back to HistGradientBoosting")
            from sklearn.ensemble import HistGradientBoostingClassifier
            return HistGradientBoostingClassifier(random_state=seed)

    if algo == "catboost":
        try:
            from catboost import CatBoostClassifier
            return CatBoostClassifier(
                iterations=cfg.get("iterations", 100),
                learning_rate=cfg.get("learning_rate", 0.1),
                depth=cfg.get("depth", 6),
                random_seed=seed,
                verbose=0,
                auto_class_weights="Balanced",
            )
        except ImportError:
            logger.warning("CatBoost not installed, falling back to HistGradientBoosting")
            from sklearn.ensemble import HistGradientBoostingClassifier
            return HistGradientBoostingClassifier(random_state=seed)

    raise ValueError(
        f"Unknown classifier: '{algorithm}'. "
        f"Supported: logistic_regression, decision_tree, random_forest, extra_trees, "
        f"svm, knn, gradient_boosting, hist_gradient_boosting, xgboost, catboost"
    )


# ---------------------------------------------------------------------------
# REGRESSORS
# ---------------------------------------------------------------------------

def build_tabular_regressor(algorithm: str, cfg: dict, seed: int = 42):
    """Return a fitted-ready sklearn-compatible regressor."""
    algo = algorithm.lower()

    if algo == "linear_regression":
        from sklearn.linear_model import Ridge
        return Ridge(alpha=cfg.get("alpha", 1.0))

    if algo == "decision_tree":
        from sklearn.tree import DecisionTreeRegressor
        return DecisionTreeRegressor(
            max_depth=cfg.get("max_depth", None),
            random_state=seed,
        )

    if algo == "random_forest":
        from sklearn.ensemble import RandomForestRegressor
        return RandomForestRegressor(
            n_estimators=cfg.get("n_estimators", 100),
            max_depth=cfg.get("max_depth", None),
            random_state=seed,
            n_jobs=-1,
        )

    if algo == "extra_trees":
        from sklearn.ensemble import ExtraTreesRegressor
        return ExtraTreesRegressor(
            n_estimators=cfg.get("n_estimators", 100),
            random_state=seed,
            n_jobs=-1,
        )

    if algo == "gradient_boosting":
        from sklearn.ensemble import GradientBoostingRegressor
        return GradientBoostingRegressor(
            n_estimators=cfg.get("n_estimators", 100),
            learning_rate=cfg.get("learning_rate", 0.1),
            max_depth=cfg.get("max_depth", 3),
            random_state=seed,
        )

    if algo == "hist_gradient_boosting":
        from sklearn.ensemble import HistGradientBoostingRegressor
        return HistGradientBoostingRegressor(
            max_iter=cfg.get("max_iter", 100),
            learning_rate=cfg.get("learning_rate", 0.1),
            random_state=seed,
        )

    if algo == "xgboost":
        try:
            from xgboost import XGBRegressor
            return XGBRegressor(
                n_estimators=cfg.get("n_estimators", 100),
                learning_rate=cfg.get("learning_rate", 0.1),
                max_depth=cfg.get("max_depth", 6),
                random_state=seed,
                n_jobs=-1,
                verbosity=0,
            )
        except ImportError:
            from sklearn.ensemble import HistGradientBoostingRegressor
            return HistGradientBoostingRegressor(random_state=seed)

    if algo == "svr":
        from sklearn.svm import SVR
        return SVR(C=cfg.get("C", 1.0), kernel=cfg.get("kernel", "rbf"))

    raise ValueError(f"Unknown regressor: '{algorithm}'")


# ---------------------------------------------------------------------------
# Feature importance (where supported)
# ---------------------------------------------------------------------------

def get_feature_importance(model, feature_names: list[str]) -> list[dict] | None:
    """Return feature importance as list of dicts, or None if unsupported."""
    importance = None

    if hasattr(model, "feature_importances_"):
        importance = model.feature_importances_
    elif hasattr(model, "coef_"):
        coef = model.coef_
        if coef.ndim > 1:
            importance = abs(coef).mean(axis=0)
        else:
            importance = abs(coef)

    if importance is None:
        return None

    pairs = sorted(
        zip(feature_names, importance.tolist()),
        key=lambda x: x[1],
        reverse=True,
    )
    return [{"feature": f, "importance": round(v, 6)} for f, v in pairs]


# ---------------------------------------------------------------------------
# Algorithm metadata for UI
# ---------------------------------------------------------------------------

CLASSIFIER_REGISTRY = {
    "logistic_regression":    {"name": "Logistic Regression",     "library": "sklearn", "task": "classification"},
    "decision_tree":          {"name": "Decision Tree",           "library": "sklearn", "task": "both"},
    "random_forest":          {"name": "Random Forest",           "library": "sklearn", "task": "both"},
    "extra_trees":            {"name": "Extra Trees",             "library": "sklearn", "task": "both"},
    "svm":                    {"name": "Support Vector Machine",  "library": "sklearn", "task": "classification"},
    "knn":                    {"name": "K-Nearest Neighbors",     "library": "sklearn", "task": "classification"},
    "gradient_boosting":      {"name": "Gradient Boosting",       "library": "sklearn", "task": "both"},
    "hist_gradient_boosting": {"name": "HistGradientBoosting",    "library": "sklearn", "task": "both"},
    "xgboost":                {"name": "XGBoost",                 "library": "xgboost", "task": "both"},
    "catboost":               {"name": "CatBoost",                "library": "catboost","task": "both"},
}

REGRESSOR_REGISTRY = {
    "linear_regression":      {"name": "Ridge Regression",        "library": "sklearn", "task": "regression"},
    "decision_tree":          {"name": "Decision Tree Regressor", "library": "sklearn", "task": "regression"},
    "random_forest":          {"name": "Random Forest Regressor", "library": "sklearn", "task": "regression"},
    "extra_trees":            {"name": "Extra Trees Regressor",   "library": "sklearn", "task": "regression"},
    "gradient_boosting":      {"name": "Gradient Boosting Reg.",  "library": "sklearn", "task": "regression"},
    "hist_gradient_boosting": {"name": "HistGradBoost Regressor", "library": "sklearn", "task": "regression"},
    "xgboost":                {"name": "XGBoost Regressor",       "library": "xgboost", "task": "regression"},
    "svr":                    {"name": "SVR",                     "library": "sklearn", "task": "regression"},
}
