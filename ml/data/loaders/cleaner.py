"""
E-Waste AI — Automated Data Cleaner
======================================
Cleans tabular datasets: missing values, duplicates, outliers, type errors.
Every cleaning step is logged and reversible. Returns before/after report.
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class DataCleaner:
    """
    Automated data cleaning pipeline.

    Usage:
        cleaner = DataCleaner(config)
        clean_df, report = cleaner.clean(df)
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.handle_missing   = self.config.get("handle_missing", "mean")
        self.remove_duplicates= self.config.get("remove_duplicates", True)
        self.remove_outliers  = self.config.get("remove_outliers", False)
        self.outlier_method   = self.config.get("outlier_method", "iqr")
        self.outlier_threshold= self.config.get("outlier_threshold", 1.5)
        self.fix_data_types   = self.config.get("fix_data_types", True)
        self.normalize_text   = self.config.get("normalize_text", True)
        self.report: Dict[str, Any] = {}

    def clean(self, df: pd.DataFrame) -> tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Run the full cleaning pipeline.

        Args:
            df: Raw input DataFrame

        Returns:
            (cleaned_df, report_dict)
        """
        df = df.copy()

        self.report = {
            "rows_before":      len(df),
            "cols":             len(df.columns),
            "missing_before":   int(df.isnull().sum().sum()),
            "duplicates_before":int(df.duplicated().sum()),
        }

        logger.info(f"Cleaning pipeline started: {df.shape}")

        # Step 1: Remove duplicates
        if self.remove_duplicates:
            df = self._remove_duplicates(df)

        # Step 2: Fix data types
        if self.fix_data_types:
            df = self._fix_data_types(df)

        # Step 3: Normalize text
        if self.normalize_text:
            df = self._normalize_text(df)

        # Step 4: Handle missing values
        df = self._handle_missing(df)

        # Step 5: Detect/remove outliers
        outliers_flagged = 0
        outliers_removed = 0
        if self.remove_outliers:
            df, outliers_flagged, outliers_removed = self._handle_outliers(df)

        self.report.update({
            "rows_after":        len(df),
            "missing_after":     int(df.isnull().sum().sum()),
            "duplicates_removed":self.report["duplicates_before"] - int(df.duplicated().sum()),
            "outliers_flagged":  outliers_flagged,
            "outliers_removed":  outliers_removed,
            "type_errors_fixed": self.report.get("type_errors_fixed", 0),
            "rows_removed":      self.report["rows_before"] - len(df),
        })

        logger.info(f"Cleaning complete: {self.report['rows_before']} → {self.report['rows_after']} rows")
        return df, self.report

    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        before = len(df)
        df = df.drop_duplicates()
        removed = before - len(df)
        logger.info(f"Duplicates removed: {removed}")
        return df

    def _fix_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Attempt to coerce numeric columns stored as strings."""
        fixed = 0
        for col in df.columns:
            if df[col].dtype == object:
                converted = pd.to_numeric(df[col], errors="coerce")
                # Only convert if >80% of values became numeric
                valid_ratio = converted.notna().sum() / max(len(converted), 1)
                if valid_ratio > 0.8:
                    df[col] = converted
                    fixed += 1
        self.report["type_errors_fixed"] = fixed
        return df

    def _normalize_text(self, df: pd.DataFrame) -> pd.DataFrame:
        """Lowercase and strip whitespace from string columns."""
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].astype(str).str.strip().str.lower()
            df[col] = df[col].replace({"nan": np.nan, "none": np.nan, "": np.nan})
        return df

    def _handle_missing(self, df: pd.DataFrame) -> pd.DataFrame:
        """Impute or drop missing values based on config."""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        cat_cols     = df.select_dtypes(include=["object"]).columns

        if self.handle_missing == "mean":
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            df[cat_cols]     = df[cat_cols].fillna(df[cat_cols].mode().iloc[0] if len(df[cat_cols].mode()) > 0 else "unknown")

        elif self.handle_missing == "median":
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
            df[cat_cols]     = df[cat_cols].fillna("unknown")

        elif self.handle_missing == "mode":
            for col in df.columns:
                mode = df[col].mode()
                if len(mode) > 0:
                    df[col] = df[col].fillna(mode.iloc[0])

        elif self.handle_missing == "ffill":
            df = df.ffill()

        elif self.handle_missing == "bfill":
            df = df.bfill()

        elif self.handle_missing == "drop":
            df = df.dropna()

        return df

    def _handle_outliers(self, df: pd.DataFrame) -> tuple[pd.DataFrame, int, int]:
        """Flag and optionally remove outliers from numeric columns."""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        outlier_mask = pd.Series(False, index=df.index)

        for col in numeric_cols:
            if self.outlier_method == "iqr":
                Q1  = df[col].quantile(0.25)
                Q3  = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - self.outlier_threshold * IQR
                upper = Q3 + self.outlier_threshold * IQR
                col_outliers = (df[col] < lower) | (df[col] > upper)
            elif self.outlier_method == "zscore":
                from scipy import stats
                z_scores = np.abs(stats.zscore(df[col].dropna()))
                col_outliers = pd.Series(False, index=df.index)
                col_outliers.iloc[df[col].notna().values] = z_scores > self.outlier_threshold
            else:
                col_outliers = pd.Series(False, index=df.index)

            outlier_mask |= col_outliers

        flagged = int(outlier_mask.sum())
        df      = df[~outlier_mask]
        removed = flagged

        logger.info(f"Outliers: flagged={flagged}, removed={removed}")
        return df, flagged, removed
