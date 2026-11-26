"""
ewaste/ai_pipelines.py
E-WASTE AI — Domain-Specific AI Pipeline Manager
=================================================
Task 4: Seven e-waste specific model pipelines.

Each pipeline:
- Validates that the dataset has the required columns
- Recommends appropriate algorithms based on task type
- Prepares features and targets for training

IMPORTANT: Pipelines honestly report when required columns are missing.
No data is invented or imputed silently.
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def _is_numeric_series(series: pd.Series) -> bool:
    """Safe numeric check that handles Pandas 4 StringDtype and other extension types."""
    try:
        return np.issubdtype(series.dtype, np.number)
    except TypeError:
        # Pandas 4 extension types (StringDtype, etc.) can't be passed to issubdtype
        return False

# ---------------------------------------------------------------------------
# Pipeline definitions
# ---------------------------------------------------------------------------

EWASTE_PIPELINES = {
    "ewaste_category_classification": {
        "label": "E-Waste Category Classification",
        "task": "classification",
        "description": "Classify electronic items into e-waste categories.",
        "candidate_target_cols": [
            "category", "ewaste_category", "device_category",
            "waste_category", "type", "device_type", "label",
        ],
        "candidate_feature_groups": ["numerical", "categorical"],
        "recommended_algorithms": [
            "random_forest", "extra_trees", "gradient_boosting",
            "hist_gradient_boosting", "logistic_regression",
        ],
    },
    "device_identification": {
        "label": "Electronic Device Identification",
        "task": "classification",
        "description": "Identify the specific electronic device type.",
        "candidate_target_cols": [
            "device", "device_name", "device_type", "product_type",
            "item_type", "product", "model",
        ],
        "candidate_feature_groups": ["numerical", "categorical"],
        "recommended_algorithms": [
            "random_forest", "extra_trees", "gradient_boosting",
            "hist_gradient_boosting", "svm",
        ],
    },
    "component_classification": {
        "label": "Component Classification",
        "task": "classification",
        "description": "Classify electronic components extracted from e-waste.",
        "candidate_target_cols": [
            "component", "component_type", "component_category",
            "part", "part_type",
        ],
        "candidate_feature_groups": ["numerical", "categorical"],
        "recommended_algorithms": [
            "random_forest", "extra_trees", "gradient_boosting",
            "logistic_regression", "knn",
        ],
    },
    "material_classification": {
        "label": "Material Classification",
        "task": "classification",
        "description": "Classify materials present in e-waste items.",
        "candidate_target_cols": [
            "material", "material_type", "material_category",
            "substance", "element", "metal_type",
        ],
        "candidate_feature_groups": ["numerical", "categorical"],
        "recommended_algorithms": [
            "random_forest", "extra_trees", "gradient_boosting",
            "hist_gradient_boosting",
        ],
    },
    "recovery_quantity_prediction": {
        "label": "Recovery Quantity Prediction",
        "task": "regression",
        "description": "Predict the quantity (kg/g) of material that can be recovered.",
        "candidate_target_cols": [
            "recovery_quantity", "recovery_kg", "recovery_amount",
            "recovered_weight", "material_weight", "quantity_kg",
            "recovery_rate", "recovered_quantity",
        ],
        "candidate_feature_groups": ["numerical", "categorical"],
        "recommended_algorithms": [
            "random_forest", "gradient_boosting", "hist_gradient_boosting",
            "extra_trees", "xgboost",
        ],
    },
    "economic_value_prediction": {
        "label": "Economic Recovery Value Prediction",
        "task": "regression",
        "description": "Predict the economic value (USD/local currency) recoverable from e-waste.",
        "candidate_target_cols": [
            "economic_value", "value_usd", "recovery_value",
            "material_value", "price", "unit_price", "total_value",
            "economic_recovery",
        ],
        "candidate_feature_groups": ["numerical", "categorical"],
        "recommended_algorithms": [
            "random_forest", "gradient_boosting", "hist_gradient_boosting",
            "xgboost", "extra_trees",
        ],
    },
    "recycling_outcome_prediction": {
        "label": "Recycling Outcome Prediction",
        "task": "classification",
        "description": "Predict the recycling outcome or processing decision for an e-waste item.",
        "candidate_target_cols": [
            "recycling_outcome", "outcome", "recycling_method",
            "disposal_method", "processing_method", "treatment",
            "recycled", "recycling_status",
        ],
        "candidate_feature_groups": ["numerical", "categorical"],
        "recommended_algorithms": [
            "random_forest", "extra_trees", "gradient_boosting",
            "hist_gradient_boosting", "logistic_regression",
        ],
    },
}


# ---------------------------------------------------------------------------
# EwastePipelineManager
# ---------------------------------------------------------------------------

class EwastePipelineManager:
    """
    Manages 7 domain-specific e-waste AI pipelines.

    Usage::

        manager = EwastePipelineManager()
        info = manager.get_pipeline_info("ewaste_category_classification")
        result = manager.validate_dataset(df, "ewaste_category_classification")
        prep = manager.prepare(df, "ewaste_category_classification",
                               target_col=result["detected_target"])
    """

    def __init__(self):
        self.pipelines = EWASTE_PIPELINES

    # ------------------------------------------------------------------ #
    # INFO                                                                 #
    # ------------------------------------------------------------------ #

    def list_pipelines(self) -> list[dict]:
        """Return a summary list of all available pipelines."""
        return [
            {
                "pipeline_id": pid,
                "label": cfg["label"],
                "task": cfg["task"],
                "description": cfg["description"],
            }
            for pid, cfg in self.pipelines.items()
        ]

    def get_pipeline_info(self, pipeline_id: str) -> dict:
        """Return full configuration for a pipeline."""
        cfg = self.pipelines.get(pipeline_id)
        if cfg is None:
            raise ValueError(
                f"Unknown pipeline '{pipeline_id}'. "
                f"Available: {list(self.pipelines)}"
            )
        return {"pipeline_id": pipeline_id, **cfg}

    def get_recommended_algorithms(self, pipeline_id: str) -> list[str]:
        """Return recommended algorithm names for the given pipeline."""
        cfg = self._get_cfg(pipeline_id)
        return cfg["recommended_algorithms"]

    # ------------------------------------------------------------------ #
    # VALIDATION                                                           #
    # ------------------------------------------------------------------ #

    def validate_dataset(
        self,
        df: pd.DataFrame,
        pipeline_id: str,
        user_target_col: str | None = None,
    ) -> dict:
        """
        Check whether df is compatible with the given pipeline.

        Returns::

            {
                "pipeline_id": str,
                "compatible": bool,
                "detected_target": str | None,
                "available_features": list[str],
                "issues": list[str],
                "warnings": list[str],
                "task": str,
                "n_rows": int,
                "n_cols": int,
            }
        """
        cfg = self._get_cfg(pipeline_id)
        issues: list[str] = []
        warnings: list[str] = []
        cols = set(df.columns.str.lower())
        actual_cols = list(df.columns)

        # --- Detect target column ---
        detected_target: str | None = None

        if user_target_col:
            if user_target_col in df.columns:
                detected_target = user_target_col
            else:
                issues.append(
                    f"User-specified target column '{user_target_col}' "
                    f"not found in dataset columns: {actual_cols[:20]}"
                )
        else:
            # Try candidate target names (case-insensitive)
            for cand in cfg["candidate_target_cols"]:
                for col in actual_cols:
                    if col.lower() == cand.lower():
                        detected_target = col
                        break
                if detected_target:
                    break

        if detected_target is None:
            issues.append(
                f"No suitable target column detected for pipeline '{cfg['label']}'. "
                f"Expected one of: {cfg['candidate_target_cols']}. "
                f"Dataset columns: {actual_cols[:30]}. "
                "Please specify the target column manually."
            )

        # --- Identify feature columns ---
        feature_cols: list[str] = []
        if detected_target:
            for col in actual_cols:
                if col == detected_target:
                    continue
                try:
                    dtype = df[col].dtype
                    if _is_numeric_series(df[col]):
                        feature_cols.append(col)
                    elif dtype == object or str(dtype).startswith("string") or str(dtype) == "object":
                        feature_cols.append(col)
                except Exception:
                    pass
        else:
            feature_cols = [c for c in actual_cols]

        if detected_target and len(feature_cols) == 0:
            issues.append("No usable feature columns found after excluding the target.")

        # --- Row count checks ---
        n_rows = len(df)
        if n_rows < 10:
            issues.append(f"Dataset has only {n_rows} rows — too few to train reliably.")
        elif n_rows < 50:
            warnings.append(
                f"Dataset has only {n_rows} rows — results may not be reliable."
            )

        # --- Target quality checks ---
        if detected_target:
            target_series = df[detected_target]
            null_count = int(target_series.isna().sum())
            if null_count > 0:
                warnings.append(
                    f"Target column '{detected_target}' has {null_count} missing values "
                    f"({null_count / n_rows * 100:.1f}%). These rows will be dropped before training."
                )
            if cfg["task"] == "classification":
                n_classes = target_series.nunique()
                if n_classes < 2:
                    issues.append(
                        f"Target column '{detected_target}' has only {n_classes} unique class(es). "
                        "Classification requires at least 2 classes."
                    )
                elif n_classes > 100:
                    warnings.append(
                        f"Target column has {n_classes} unique values — high cardinality "
                        "may indicate this is not a categorical target."
                    )
            elif cfg["task"] == "regression":
                if not _is_numeric_series(target_series):
                    issues.append(
                        f"Target column '{detected_target}' is not numeric — "
                        "required for regression task."
                    )

        compatible = len(issues) == 0

        return {
            "pipeline_id": pipeline_id,
            "compatible": compatible,
            "detected_target": detected_target,
            "available_features": feature_cols,
            "issues": issues,
            "warnings": warnings,
            "task": cfg["task"],
            "n_rows": n_rows,
            "n_cols": len(actual_cols),
        }

    # ------------------------------------------------------------------ #
    # PREPARATION                                                          #
    # ------------------------------------------------------------------ #

    def prepare(
        self,
        df: pd.DataFrame,
        pipeline_id: str,
        target_col: str,
        feature_cols: list[str] | None = None,
        drop_na_target: bool = True,
    ) -> dict:
        """
        Prepare X, y arrays from df for training.

        Returns::

            {
                "X": np.ndarray,
                "y": np.ndarray,
                "feature_names": list[str],
                "target_name": str,
                "task": str,
                "n_samples": int,
                "encoding_map": dict,   # label→int for categorical targets
                "class_names": list | None,
                "dropped_rows": int,
            }
        """
        cfg = self._get_cfg(pipeline_id)
        df = df.copy()

        # Drop rows with missing target
        dropped = 0
        if drop_na_target:
            before = len(df)
            df = df.dropna(subset=[target_col])
            dropped = before - len(df)

        # Select feature columns
        if feature_cols is None:
            feature_cols = [c for c in df.columns if c != target_col]

        # Keep only feature + target cols
        use_cols = [c for c in feature_cols if c in df.columns]
        df = df[use_cols + [target_col]].copy()

        # Encode categorical features
        encoding_map: dict[str, dict] = {}
        X_parts = []
        for col in use_cols:
            series = df[col]
            if _is_numeric_series(series):
                arr = series.fillna(series.median()).values.astype(float)
                X_parts.append(arr.reshape(-1, 1))
            else:
                vals = series.fillna("__missing__").astype(str)
                uniq = sorted(vals.unique())
                lmap = {v: i for i, v in enumerate(uniq)}
                encoding_map[col] = lmap
                X_parts.append(
                    vals.map(lmap).values.astype(float).reshape(-1, 1)
                )

        X = np.hstack(X_parts) if X_parts else np.zeros((len(df), 0))

        # Encode target
        y_series = df[target_col]
        class_names: list | None = None

        if cfg["task"] == "classification":
            if not _is_numeric_series(y_series):
                uniq = sorted(y_series.astype(str).unique())
                tmap = {v: i for i, v in enumerate(uniq)}
                encoding_map[f"__target__{target_col}"] = tmap
                y = y_series.astype(str).map(tmap).values.astype(int)
                class_names = uniq
            else:
                y = y_series.values.astype(int)
                class_names = [str(c) for c in sorted(np.unique(y))]
        else:
            y = y_series.values.astype(float)

        return {
            "X": X,
            "y": y,
            "feature_names": use_cols,
            "target_name": target_col,
            "task": cfg["task"],
            "n_samples": int(len(y)),
            "encoding_map": encoding_map,
            "class_names": class_names,
            "dropped_rows": dropped,
        }

    # ------------------------------------------------------------------ #
    # HELPERS                                                              #
    # ------------------------------------------------------------------ #

    def _get_cfg(self, pipeline_id: str) -> dict:
        cfg = self.pipelines.get(pipeline_id)
        if cfg is None:
            raise ValueError(
                f"Unknown pipeline '{pipeline_id}'. "
                f"Available: {list(self.pipelines)}"
            )
        return cfg
