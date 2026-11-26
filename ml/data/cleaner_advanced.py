"""
Advanced Data Cleaner — Phase 2: Dataset Intelligence Engine
Extends Phase 1 DataCleaner with full audit trail, never modifies original data.
"""

from __future__ import annotations

import re
import logging
from datetime import datetime, timezone
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

from ml.data.loaders.cleaner import DataCleaner

logger = logging.getLogger(__name__)


class AdvancedDataCleaner:
    """
    Cleans tabular DataFrames while preserving the original.

    Usage::

        cleaner = AdvancedDataCleaner()
        cleaned_df, report = cleaner.clean(raw_df, config)

    The returned ``cleaned_df`` is always a *copy* — ``raw_df`` is never touched.
    """

    # ------------------------------------------------------------------ #
    # Public interface                                                     #
    # ------------------------------------------------------------------ #

    def clean(
        self,
        df: pd.DataFrame,
        config: dict | None = None,
    ) -> tuple[pd.DataFrame, dict]:
        """
        Run the full cleaning pipeline.

        Parameters
        ----------
        df:
            Raw DataFrame (never modified in place).
        config:
            Optional cleaning configuration dictionary.  Supported keys:

            * ``fill_strategy``  – ``"median"`` | ``"mean"`` | ``"mode"`` |
              ``"constant"`` | ``"drop_row"``  (default ``"median"``)
            * ``fill_constant``  – value used when ``fill_strategy=="constant"``
            * ``drop_empty_cols`` – bool (default ``True``)
            * ``remove_duplicates`` – bool (default ``True``)
            * ``normalize_text`` – bool (default ``True``)
            * ``fix_types`` – bool (default ``True``)
            * ``flag_outliers`` – bool (default ``True``)
            * ``outlier_method`` – ``"iqr"`` | ``"zscore"`` (default ``"iqr"``)
            * ``outlier_threshold`` – IQR multiplier / Z-score threshold
              (default ``1.5`` / ``3.0``)

        Returns
        -------
        (cleaned_df, report)
        """
        cfg = self._default_config()
        if config:
            cfg.update(config)

        cleaned = df.copy()
        ops: list[dict] = []

        rows_before = len(cleaned)
        cols_before = list(cleaned.columns)

        # --- pipeline steps ------------------------------------------------
        if cfg["drop_empty_cols"]:
            cleaned, op = self._drop_empty_columns(cleaned)
            ops.append(op)

        if cfg["remove_duplicates"]:
            cleaned, op = self._remove_duplicates(cleaned)
            ops.append(op)

        if cfg["fix_types"]:
            cleaned, op = self._fix_data_types(cleaned)
            ops.append(op)

        if cfg["normalize_text"]:
            cleaned, op = self._normalize_text(cleaned)
            ops.append(op)

        cleaned, op = self._handle_missing_values(cleaned, cfg)
        ops.append(op)

        if cfg["flag_outliers"]:
            cleaned, op = self._flag_outliers(cleaned, cfg)
            ops.append(op)

        cleaned, op = self._detect_inconsistent_categories(cleaned)
        ops.append(op)

        # --- build report --------------------------------------------------
        rows_after = len(cleaned)
        cols_after = list(cleaned.columns)
        dropped_cols = [c for c in cols_before if c not in cols_after]

        # Aggregate counts from individual op reports
        missing_filled = sum(
            o.get("missing_filled", 0) for o in ops if isinstance(o, dict)
        )
        duplicates_removed = sum(
            o.get("duplicates_removed", 0) for o in ops if isinstance(o, dict)
        )
        outliers_flagged = sum(
            o.get("outliers_flagged", 0) for o in ops if isinstance(o, dict)
        )
        type_fixes = sum(
            o.get("type_fixes", 0) for o in ops if isinstance(o, dict)
        )
        text_normalizations = sum(
            o.get("text_normalizations", 0) for o in ops if isinstance(o, dict)
        )

        report = {
            "rows_before": rows_before,
            "rows_after": rows_after,
            "rows_removed": rows_before - rows_after,
            "cols_before": len(cols_before),
            "cols_after": len(cols_after),
            "columns_dropped": dropped_cols,
            "missing_filled": missing_filled,
            "duplicates_removed": duplicates_removed,
            "outliers_flagged": outliers_flagged,
            "type_fixes": type_fixes,
            "text_normalizations": text_normalizations,
            "config_used": cfg,
            "operations_log": ops,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        logger.info(
            "Cleaning complete: %d→%d rows, %d→%d cols",
            rows_before,
            rows_after,
            len(cols_before),
            len(cols_after),
        )
        return cleaned, report

    # ------------------------------------------------------------------ #
    # Private helpers                                                      #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _default_config() -> dict:
        return {
            "fill_strategy": "median",
            "fill_constant": 0,
            "drop_empty_cols": True,
            "remove_duplicates": True,
            "normalize_text": True,
            "fix_types": True,
            "flag_outliers": True,
            "outlier_method": "iqr",
            "outlier_threshold": 1.5,
        }

    # ---- empty columns -----------------------------------------------

    @staticmethod
    def _drop_empty_columns(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
        empty = [c for c in df.columns if df[c].isna().all()]
        if empty:
            df = df.drop(columns=empty)
        return df, {
            "operation": "drop_empty_columns",
            "columns_dropped": empty,
            "detail": f"Dropped {len(empty)} fully-empty columns",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # ---- duplicates --------------------------------------------------

    @staticmethod
    def _remove_duplicates(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
        before = len(df)
        df = df.drop_duplicates()
        removed = before - len(df)
        return df, {
            "operation": "remove_duplicates",
            "duplicates_removed": removed,
            "detail": f"Removed {removed} duplicate rows",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # ---- type correction ---------------------------------------------

    @staticmethod
    def _fix_data_types(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
        fixes = 0
        for col in df.select_dtypes(include="object").columns:
            converted = pd.to_numeric(df[col], errors="coerce")
            # Only convert if more than 80 % of values parse as numeric
            valid_ratio = converted.notna().sum() / max(len(df), 1)
            if valid_ratio >= 0.80 and df[col].notna().sum() > 0:
                df[col] = converted
                fixes += 1
        return df, {
            "operation": "fix_data_types",
            "type_fixes": fixes,
            "detail": f"Converted {fixes} string columns to numeric",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # ---- text normalisation ------------------------------------------

    @staticmethod
    def _normalize_text(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
        normalizations = 0
        # In Pandas 4, string columns may have StringDtype instead of object
        str_cols = df.select_dtypes(include=["object", "string"]).columns
        for col in str_cols:
            original = df[col].copy()
            df[col] = df[col].apply(
                lambda v: str(v).strip().lower() if pd.notna(v) else v
            )
            changed = (df[col].astype(str) != original.astype(str)).sum()
            normalizations += int(changed)
        return df, {
            "operation": "normalize_text",
            "text_normalizations": normalizations,
            "detail": f"Normalised {normalizations} text values (strip + lowercase)",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # ---- missing values ----------------------------------------------

    @staticmethod
    def _handle_missing_values(
        df: pd.DataFrame, cfg: dict
    ) -> tuple[pd.DataFrame, dict]:
        strategy = cfg.get("fill_strategy", "median")
        filled = 0
        missing_before = df.isna().sum().sum()

        if strategy == "drop_row":
            before = len(df)
            df = df.dropna()
            filled = before - len(df)
        else:
            for col in df.columns:
                col_missing = df[col].isna().sum()
                if col_missing == 0:
                    continue
                if df[col].dtype in [np.float64, np.float32, np.int64, np.int32]:
                    if strategy == "mean":
                        df[col] = df[col].fillna(df[col].mean())
                    elif strategy == "median":
                        df[col] = df[col].fillna(df[col].median())
                    elif strategy == "mode":
                        mode_val = df[col].mode()
                        if not mode_val.empty:
                            df[col] = df[col].fillna(mode_val.iloc[0])
                    elif strategy == "constant":
                        df[col] = df[col].fillna(cfg.get("fill_constant", 0))
                else:
                    mode_val = df[col].mode()
                    if not mode_val.empty:
                        df[col] = df[col].fillna(mode_val.iloc[0])
                    else:
                        df[col] = df[col].fillna("unknown")
                filled += col_missing

        missing_after = df.isna().sum().sum()
        return df, {
            "operation": "handle_missing_values",
            "missing_filled": int(missing_before - missing_after),
            "strategy": strategy,
            "detail": f"Filled {missing_before - missing_after} missing values using {strategy}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # ---- outlier detection -------------------------------------------

    @staticmethod
    def _flag_outliers(
        df: pd.DataFrame, cfg: dict
    ) -> tuple[pd.DataFrame, dict]:
        method = cfg.get("outlier_method", "iqr")
        threshold = cfg.get("outlier_threshold", 1.5)
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        outlier_counts: dict[str, int] = {}
        total_flagged = 0

        for col in numeric_cols:
            series = df[col].dropna()
            if len(series) < 4:
                continue
            if method == "iqr":
                q1, q3 = series.quantile(0.25), series.quantile(0.75)
                iqr = q3 - q1
                lower, upper = q1 - threshold * iqr, q3 + threshold * iqr
                mask = (df[col] < lower) | (df[col] > upper)
            else:  # zscore
                z = np.abs(stats.zscore(series, nan_policy="omit"))
                # Align back to full df index
                mask = pd.Series(False, index=df.index)
                mask.loc[series.index] = z > threshold

            count = int(mask.sum())
            if count:
                flag_col = f"_outlier_{col}"
                df[flag_col] = False
                df.loc[mask, flag_col] = True
                outlier_counts[col] = count
                total_flagged += count

        return df, {
            "operation": "flag_outliers",
            "outliers_flagged": total_flagged,
            "method": method,
            "threshold": threshold,
            "per_column": outlier_counts,
            "detail": f"Flagged {total_flagged} outliers across {len(outlier_counts)} columns",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # ---- inconsistent categories ------------------------------------

    @staticmethod
    def _detect_inconsistent_categories(
        df: pd.DataFrame,
    ) -> tuple[pd.DataFrame, dict]:
        low_cardinality = []
        inconsistencies: dict[str, list] = {}

        for col in df.select_dtypes(include="object").columns:
            unique_vals = df[col].dropna().unique()
            if len(unique_vals) <= 50:
                low_cardinality.append(col)
                # Detect values that differ only in case/spacing
                canonical: dict[str, list] = {}
                for v in unique_vals:
                    key = str(v).strip().lower()
                    canonical.setdefault(key, []).append(str(v))
                conflicts = {k: v for k, v in canonical.items() if len(v) > 1}
                if conflicts:
                    inconsistencies[col] = list(conflicts.values())

        return df, {
            "operation": "detect_inconsistent_categories",
            "outliers_flagged": 0,
            "inconsistent_columns": list(inconsistencies.keys()),
            "inconsistencies": inconsistencies,
            "detail": f"Found inconsistent categories in {len(inconsistencies)} columns",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
