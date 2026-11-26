"""
Advanced Preprocessor — Phase 2: Dataset Intelligence Engine
Handles tabular preprocessing with full reproducibility tracking.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import (
    LabelEncoder,
    MinMaxScaler,
    OneHotEncoder,
    RobustScaler,
    StandardScaler,
)
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

logger = logging.getLogger(__name__)


class AdvancedPreprocessor:
    """
    Fits and applies preprocessing transforms for tabular e-waste data.

    Usage::

        prep = AdvancedPreprocessor()
        result = prep.fit_transform(df, target_col="label", feature_cols=["a","b"], config={})
        # result contains X_train, X_val, X_test, y_train, y_val, y_test, etc.
    """

    def fit_transform(
        self,
        df: pd.DataFrame,
        target_col: str,
        feature_cols: list[str] | None = None,
        config: dict | None = None,
    ) -> dict:
        """
        Full preprocessing pipeline.

        Parameters
        ----------
        df: Input DataFrame (original — not modified).
        target_col: Name of the target/label column.
        feature_cols: Columns to use as features.  If None, all columns except
                      target_col are used.
        config: Optional config dict.  Keys:
            * scaler: "standard" | "minmax" | "robust" | "none"
            * encoder: "onehot" | "label" | "none"
            * train_ratio: float (default 0.70)
            * val_ratio:   float (default 0.15)
            * test_ratio:  float (default 0.15)
            * random_seed: int   (default 42)
            * stratify:    bool  (default True)

        Returns
        -------
        dict with keys:
            X_train, X_val, X_test (np.ndarray)
            y_train, y_val, y_test (np.ndarray)
            feature_names (list[str])
            class_names   (list)
            preprocessor_config (dict)
            preprocessing_report (dict)
        """
        cfg = {
            "scaler": "standard",
            "encoder": "onehot",
            "train_ratio": 0.70,
            "val_ratio": 0.15,
            "test_ratio": 0.15,
            "random_seed": 42,
            "stratify": True,
        }
        if config:
            cfg.update(config)

        # ---- validation ------------------------------------------------
        if target_col not in df.columns:
            raise ValueError(f"target_col '{target_col}' not found in DataFrame")

        if feature_cols is None:
            feature_cols = [c for c in df.columns if c != target_col]

        # Leakage prevention
        if target_col in feature_cols:
            raise ValueError(
                f"target_col '{target_col}' must not appear in feature_cols"
            )

        ratios = cfg["train_ratio"] + cfg["val_ratio"] + cfg["test_ratio"]
        if abs(ratios - 1.0) > 1e-6:
            raise ValueError(f"train+val+test ratios must sum to 1.0, got {ratios:.4f}")

        # ---- prepare data ----------------------------------------------
        df_work = df[feature_cols + [target_col]].copy()
        df_work = df_work.dropna(subset=[target_col])

        X_df = df_work[feature_cols].copy()
        y_raw = df_work[target_col].copy()

        # Encode target
        le = LabelEncoder()
        y = le.fit_transform(y_raw.astype(str))
        class_names = list(le.classes_)

        # ---- identify column types ------------------------------------
        numeric_cols = X_df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = X_df.select_dtypes(include=["object", "category"]).columns.tolist()

        # ---- build sklearn pipeline -----------------------------------
        transformers = []

        if numeric_cols:
            scaler = self._build_scaler(cfg["scaler"])
            if scaler is not None:
                transformers.append(("num", scaler, numeric_cols))

        if categorical_cols:
            encoder = self._build_encoder(cfg["encoder"])
            if encoder is not None:
                transformers.append(("cat", encoder, categorical_cols))

        if transformers:
            preprocessor = ColumnTransformer(transformers, remainder="passthrough")
            X = preprocessor.fit_transform(X_df.fillna(0))
        else:
            X = X_df.fillna(0).values
            preprocessor = None

        # ---- train / val / test split ----------------------------------
        stratify_arr = y if cfg["stratify"] and len(np.unique(y)) > 1 else None
        try:
            X_train_val, X_test, y_train_val, y_test = train_test_split(
                X, y,
                test_size=cfg["test_ratio"],
                random_state=cfg["random_seed"],
                stratify=stratify_arr,
            )
            val_relative = cfg["val_ratio"] / (cfg["train_ratio"] + cfg["val_ratio"])
            stratify_tv = y_train_val if cfg["stratify"] and len(np.unique(y_train_val)) > 1 else None
            X_train, X_val, y_train, y_val = train_test_split(
                X_train_val, y_train_val,
                test_size=val_relative,
                random_state=cfg["random_seed"],
                stratify=stratify_tv,
            )
        except ValueError as exc:
            logger.warning("Stratified split failed (%s); falling back to random split", exc)
            X_train_val, X_test, y_train_val, y_test = train_test_split(
                X, y, test_size=cfg["test_ratio"], random_state=cfg["random_seed"]
            )
            val_relative = cfg["val_ratio"] / (cfg["train_ratio"] + cfg["val_ratio"])
            X_train, X_val, y_train, y_val = train_test_split(
                X_train_val, y_train_val, test_size=val_relative, random_state=cfg["random_seed"]
            )

        # ---- feature names --------------------------------------------
        try:
            if preprocessor is not None:
                feature_names = list(preprocessor.get_feature_names_out())
            else:
                feature_names = feature_cols
        except Exception:
            feature_names = feature_cols

        # ---- report ---------------------------------------------------
        preprocessing_report = {
            "total_samples": len(df_work),
            "features_used": feature_cols,
            "numeric_features": numeric_cols,
            "categorical_features": categorical_cols,
            "target_column": target_col,
            "class_names": class_names,
            "n_classes": len(class_names),
            "scaler": cfg["scaler"],
            "encoder": cfg["encoder"],
            "split": {
                "train": len(X_train),
                "val": len(X_val),
                "test": len(X_test),
            },
            "stratified": cfg["stratify"],
            "random_seed": cfg["random_seed"],
            "leakage_check": "PASSED — target not in features",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        return {
            "X_train": X_train,
            "X_val": X_val,
            "X_test": X_test,
            "y_train": y_train,
            "y_val": y_val,
            "y_test": y_test,
            "feature_names": feature_names,
            "class_names": class_names,
            "preprocessor_config": cfg,
            "preprocessing_report": preprocessing_report,
        }

    def save_config(self, preprocessing_report: dict, path: str | Path) -> None:
        """Save preprocessing config to JSON for reproducibility."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(preprocessing_report, f, indent=2, default=str)
        logger.info("Preprocessing config saved to %s", path)

    # ------------------------------------------------------------------ #
    # Helpers                                                              #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _build_scaler(name: str):
        mapping = {
            "standard": StandardScaler(),
            "minmax": MinMaxScaler(),
            "robust": RobustScaler(),
            "none": None,
        }
        return mapping.get(name, StandardScaler())

    @staticmethod
    def _build_encoder(name: str):
        if name == "onehot":
            return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        elif name == "label":
            # LabelEncoder doesn't work inside ColumnTransformer for multi-col;
            # use OrdinalEncoder as equivalent
            from sklearn.preprocessing import OrdinalEncoder
            return OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
        return None
