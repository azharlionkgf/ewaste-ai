"""
DataPreprocessor: tabular data preprocessing for the E-WASTE AI project.
Handles categorical encoding, numeric scaling, and stratified splits.
"""

import json
import logging
import pathlib

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

logger = logging.getLogger(__name__)


class DataPreprocessor:
    """
    Fits encoders / scalers on a DataFrame, produces stratified
    train / val / test splits, and can be persisted to disk.
    """

    # Default split ratios: 70 % train, 15 % val, 15 % test
    _DEFAULT_TRAIN = 0.70
    _DEFAULT_VAL   = 0.15
    _DEFAULT_TEST  = 0.15

    def __init__(self, config: dict = None):
        self.config: dict = config or {}
        self._scaler: StandardScaler = StandardScaler()
        self._label_encoders: dict[str, LabelEncoder] = {}
        self._target_encoder: LabelEncoder = LabelEncoder()
        self._numeric_cols: list[str] = []
        self._categorical_cols: list[str] = []
        self._feature_names: list[str] = []
        self._is_fitted: bool = False

        # Configurable ratios (may be overridden via config)
        self._train_ratio = self.config.get("train_ratio", self._DEFAULT_TRAIN)
        self._val_ratio   = self.config.get("val_ratio",   self._DEFAULT_VAL)
        self._test_ratio  = self.config.get("test_ratio",  self._DEFAULT_TEST)
        self._random_state = self.config.get("random_state", 42)

        logger.debug("DataPreprocessor initialised with config: %s", self.config)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def fit_transform(
        self,
        df: pd.DataFrame,
        target_col: str,
    ) -> tuple:
        """
        Fit encoders / scaler on *df* and return stratified splits.

        Returns
        -------
        (X_train, X_val, X_test, y_train, y_val, y_test, feature_names)
        """
        logger.info("fit_transform: target='%s', df shape=%s", target_col, df.shape)

        if target_col not in df.columns:
            raise ValueError(f"Target column '{target_col}' not found in DataFrame.")

        df = df.copy()

        # --- Split features / target -----------------------------------------
        y_raw = df[target_col].copy()
        X_df  = df.drop(columns=[target_col])

        # --- Identify column types -------------------------------------------
        self._categorical_cols = X_df.select_dtypes(
            include=["object", "category", "bool"]
        ).columns.tolist()
        self._numeric_cols = X_df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        logger.debug("Categorical cols: %s", self._categorical_cols)
        logger.debug("Numeric cols: %s", self._numeric_cols)

        # --- Encode categoricals ---------------------------------------------
        for col in self._categorical_cols:
            le = LabelEncoder()
            X_df[col] = le.fit_transform(X_df[col].astype(str))
            self._label_encoders[col] = le

        # --- Encode target ---------------------------------------------------
        y_encoded = self._target_encoder.fit_transform(y_raw.astype(str))

        # --- Scale numerics --------------------------------------------------
        feature_order = self._categorical_cols + self._numeric_cols
        X_ordered = X_df[feature_order].values.astype(np.float64)

        # Fit scaler only on numeric portion
        n_cat = len(self._categorical_cols)
        if self._numeric_cols:
            X_ordered[:, n_cat:] = self._scaler.fit_transform(
                X_ordered[:, n_cat:]
            )

        self._feature_names = feature_order
        self._is_fitted = True

        # --- Stratified splits -----------------------------------------------
        # First split: train  |  temp (val + test)
        val_test_ratio = self._val_ratio + self._test_ratio
        X_train, X_temp, y_train, y_temp = train_test_split(
            X_ordered, y_encoded,
            test_size=val_test_ratio,
            stratify=y_encoded,
            random_state=self._random_state,
        )

        # Second split: val  |  test  (from temp)
        relative_test = self._test_ratio / val_test_ratio
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp,
            test_size=relative_test,
            stratify=y_temp,
            random_state=self._random_state,
        )

        logger.info(
            "Splits — train: %d, val: %d, test: %d",
            len(X_train), len(X_val), len(X_test),
        )

        return X_train, X_val, X_test, y_train, y_val, y_test, self._feature_names

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        """
        Apply fitted encoders / scaler to a new DataFrame (no target column).
        """
        if not self._is_fitted:
            raise RuntimeError("DataPreprocessor has not been fitted yet.")

        df = df.copy()

        # Encode categoricals
        for col in self._categorical_cols:
            if col not in df.columns:
                raise ValueError(f"Expected column '{col}' not found.")
            le = self._label_encoders[col]
            df[col] = le.transform(df[col].astype(str))

        # Build ordered array
        feature_order = self._categorical_cols + self._numeric_cols
        X = df[feature_order].values.astype(np.float64)

        # Scale numerics
        n_cat = len(self._categorical_cols)
        if self._numeric_cols:
            X[:, n_cat:] = self._scaler.transform(X[:, n_cat:])

        return X

    def save(self, path: str) -> None:
        """
        Persist the preprocessor to *path*.
        Saves: a joblib bundle (.joblib) + a sidecar config JSON (.json).
        """
        save_path = pathlib.Path(path)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        # Joblib bundle for sklearn objects
        joblib_path = save_path.with_suffix(".joblib")
        bundle = {
            "scaler": self._scaler,
            "label_encoders": self._label_encoders,
            "target_encoder": self._target_encoder,
            "numeric_cols": self._numeric_cols,
            "categorical_cols": self._categorical_cols,
            "feature_names": self._feature_names,
            "is_fitted": self._is_fitted,
        }
        joblib.dump(bundle, joblib_path)

        # JSON sidecar
        json_path = save_path.with_suffix(".json")
        meta = {
            "config": self.config,
            "train_ratio": self._train_ratio,
            "val_ratio":   self._val_ratio,
            "test_ratio":  self._test_ratio,
            "random_state": self._random_state,
            "feature_names": self._feature_names,
            "numeric_cols": self._numeric_cols,
            "categorical_cols": self._categorical_cols,
            "target_classes": list(self._target_encoder.classes_) if self._is_fitted else [],
        }
        json_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

        logger.info("DataPreprocessor saved → %s", joblib_path)

    @classmethod
    def load(cls, path: str) -> "DataPreprocessor":
        """
        Load a previously saved DataPreprocessor from *path*.
        Accepts the base path (with or without extension).
        """
        base_path = pathlib.Path(path).with_suffix("")
        joblib_path = base_path.with_suffix(".joblib")
        json_path   = base_path.with_suffix(".json")

        if not joblib_path.exists():
            raise FileNotFoundError(f"Joblib bundle not found: {joblib_path}")

        bundle = joblib.load(joblib_path)
        meta   = json.loads(json_path.read_text(encoding="utf-8")) if json_path.exists() else {}

        instance = cls(config=meta.get("config", {}))
        instance._scaler           = bundle["scaler"]
        instance._label_encoders   = bundle["label_encoders"]
        instance._target_encoder   = bundle["target_encoder"]
        instance._numeric_cols     = bundle["numeric_cols"]
        instance._categorical_cols = bundle["categorical_cols"]
        instance._feature_names    = bundle["feature_names"]
        instance._is_fitted        = bundle["is_fitted"]

        logger.info("DataPreprocessor loaded ← %s", joblib_path)
        return instance
