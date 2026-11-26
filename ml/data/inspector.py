"""
ml/data/inspector.py
E-WASTE AI — Automated Dataset Inspection & Profiling Engine
Generates a full profile of any tabular or image dataset.
"""

import logging
import datetime
import json
import hashlib
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# E-waste specific column keywords for domain detection
EWASTE_KEYWORDS = {
    "device": ["device", "equipment", "product", "item", "category", "type"],
    "material": ["material", "metal", "plastic", "gold", "silver", "copper", "lithium", "cobalt"],
    "weight": ["weight", "mass", "kg", "gram", "quantity"],
    "condition": ["condition", "state", "quality", "grade", "status"],
    "hazmat": ["hazardous", "hazmat", "toxic", "lead", "mercury", "cadmium", "rohs"],
    "economic": ["value", "price", "cost", "revenue", "profit", "usd", "inr"],
    "environmental": ["co2", "carbon", "emission", "environmental", "footprint"],
}


class DatasetInspector:
    """
    Automated dataset profiling engine.
    Analyses tabular CSV/Excel/JSON datasets or image dataset directories.
    Returns a detailed report dict — never modifies the source data.
    """

    def __init__(self):
        self.report: dict = {}

    # ------------------------------------------------------------------
    # PUBLIC: Tabular inspection
    # ------------------------------------------------------------------
    def inspect_tabular(self, df: pd.DataFrame, dataset_name: str = "dataset") -> dict:
        """
        Full inspection of a tabular dataset.
        Returns a structured report dict.
        """
        logger.info(f"Inspecting tabular dataset '{dataset_name}': {df.shape}")
        report = {
            "dataset_name": dataset_name,
            "inspection_timestamp": datetime.datetime.utcnow().isoformat(),
            "dataset_type": "tabular",
        }

        report["shape"] = {"rows": df.shape[0], "columns": df.shape[1]}
        report["memory_mb"] = round(df.memory_usage(deep=True).sum() / 1_048_576, 3)

        report["columns"] = self._inspect_columns(df)
        report["missing"] = self._inspect_missing(df)
        report["duplicates"] = self._inspect_duplicates(df)
        report["dtypes_summary"] = self._dtype_summary(df)
        report["numeric_stats"] = self._numeric_stats(df)
        report["categorical_stats"] = self._categorical_stats(df)
        report["outliers"] = self._detect_outliers(df)
        report["class_distribution"] = self._class_distribution(df)
        report["domain_detection"] = self._detect_ewaste_domain(df)
        report["data_issues"] = self._find_data_issues(df)
        report["checksum"] = self._dataframe_checksum(df)

        self.report = report
        logger.info(f"Inspection complete: {report['shape']['rows']} rows, "
                    f"{len(report['missing']['columns_with_missing'])} columns with missing values")
        return report

    # ------------------------------------------------------------------
    # PUBLIC: Image dataset inspection
    # ------------------------------------------------------------------
    def inspect_images(self, root_dir: str) -> dict:
        """
        Inspect an image dataset directory organised as one subfolder per class.
        """
        root = Path(root_dir)
        if not root.exists():
            return {"error": f"Directory not found: {root_dir}"}

        logger.info(f"Inspecting image dataset: {root_dir}")
        VALID_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}

        class_counts = {}
        all_sizes = []
        corrupt = []
        duplicate_hashes: dict[str, list] = {}
        total = 0

        for class_dir in sorted(root.iterdir()):
            if not class_dir.is_dir():
                continue
            imgs = [f for f in class_dir.rglob("*") if f.suffix.lower() in VALID_EXT]
            class_counts[class_dir.name] = len(imgs)
            total += len(imgs)

            for img_path in imgs:
                try:
                    file_hash = _file_hash(img_path)
                    duplicate_hashes.setdefault(file_hash, []).append(str(img_path))
                    size_kb = img_path.stat().st_size / 1024
                    all_sizes.append(size_kb)
                    # Try to open with PIL for dimension info
                    try:
                        from PIL import Image as PILImage
                        with PILImage.open(img_path) as im:
                            _ = im.size
                    except Exception:
                        corrupt.append(str(img_path))
                except Exception as e:
                    corrupt.append(str(img_path))

        duplicates = {h: paths for h, paths in duplicate_hashes.items() if len(paths) > 1}
        counts = list(class_counts.values())
        imbalance_ratio = max(counts) / max(min(counts), 1) if counts else 1.0

        report = {
            "dataset_type": "image",
            "root_dir": str(root_dir),
            "num_classes": len(class_counts),
            "class_names": list(class_counts.keys()),
            "class_counts": class_counts,
            "total_images": total,
            "avg_per_class": round(total / max(len(class_counts), 1), 1),
            "min_per_class": min(counts) if counts else 0,
            "max_per_class": max(counts) if counts else 0,
            "imbalance_ratio": round(imbalance_ratio, 2),
            "is_imbalanced": imbalance_ratio > 3.0,
            "corrupt_images": corrupt,
            "corrupt_count": len(corrupt),
            "duplicate_groups": len(duplicates),
            "avg_file_size_kb": round(np.mean(all_sizes), 1) if all_sizes else 0,
            "formats": list({Path(p).suffix.lower() for paths in duplicate_hashes.values() for p in paths}),
            "inspection_timestamp": datetime.datetime.utcnow().isoformat(),
        }

        logger.info(f"Image inspection: {total} images, {len(class_counts)} classes, "
                    f"{len(corrupt)} corrupt, {len(duplicates)} duplicate groups")
        return report

    # ------------------------------------------------------------------
    # PRIVATE helpers
    # ------------------------------------------------------------------
    def _inspect_columns(self, df: pd.DataFrame) -> list:
        cols = []
        for col in df.columns:
            series = df[col]
            null_count = int(series.isnull().sum())
            info = {
                "name": col,
                "dtype": str(series.dtype),
                "inferred_type": _infer_col_type(series),
                "null_count": null_count,
                "null_pct": round(null_count / max(len(df), 1) * 100, 2),
                "unique_count": int(series.nunique()),
                "unique_pct": round(series.nunique() / max(len(df), 1) * 100, 2),
                "sample_values": [str(v) for v in series.dropna().head(3).tolist()],
            }
            cols.append(info)
        return cols

    def _inspect_missing(self, df: pd.DataFrame) -> dict:
        missing = df.isnull().sum()
        total_missing = int(missing.sum())
        cols_with_missing = [
            {"column": col, "count": int(cnt), "pct": round(cnt / len(df) * 100, 2)}
            for col, cnt in missing[missing > 0].items()
        ]
        return {
            "total_missing": total_missing,
            "total_missing_pct": round(total_missing / max(df.size, 1) * 100, 2),
            "columns_with_missing": cols_with_missing,
            "complete_columns": int((missing == 0).sum()),
        }

    def _inspect_duplicates(self, df: pd.DataFrame) -> dict:
        dup_rows = int(df.duplicated().sum())
        return {
            "duplicate_rows": dup_rows,
            "duplicate_pct": round(dup_rows / max(len(df), 1) * 100, 2),
            "is_problem": dup_rows > 0,
        }

    def _dtype_summary(self, df: pd.DataFrame) -> dict:
        return {str(k): int(v) for k, v in df.dtypes.astype(str).value_counts().items()}

    def _numeric_stats(self, df: pd.DataFrame) -> dict:
        num_cols = df.select_dtypes(include="number")
        if num_cols.empty:
            return {}
        desc = num_cols.describe().T
        result = {}
        for col in desc.index:
            result[col] = {k: round(float(v), 6) if pd.notna(v) else None
                           for k, v in desc.loc[col].items()}
        return result

    def _categorical_stats(self, df: pd.DataFrame) -> dict:
        cat_cols = df.select_dtypes(include=["object", "category"])
        result = {}
        for col in cat_cols.columns:
            vc = df[col].value_counts(dropna=False)
            result[col] = {
                "unique": int(df[col].nunique()),
                "top_values": {str(k): int(v) for k, v in vc.head(10).items()},
                "has_mixed_case": _has_mixed_case(df[col]),
                "has_leading_trailing_spaces": _has_whitespace_issues(df[col]),
            }
        return result

    def _detect_outliers(self, df: pd.DataFrame) -> dict:
        num_cols = df.select_dtypes(include="number")
        result = {}
        for col in num_cols.columns:
            series = df[col].dropna()
            if len(series) < 4:
                continue
            q1, q3 = series.quantile(0.25), series.quantile(0.75)
            iqr = q3 - q1
            lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            outlier_count = int(((series < lower) | (series > upper)).sum())
            if outlier_count > 0:
                result[col] = {
                    "outlier_count": outlier_count,
                    "outlier_pct": round(outlier_count / len(series) * 100, 2),
                    "lower_fence": round(float(lower), 4),
                    "upper_fence": round(float(upper), 4),
                    "method": "IQR (1.5×)",
                }
        return result

    def _class_distribution(self, df: pd.DataFrame) -> dict:
        """Detect probable target columns and their class distributions."""
        result = {}
        low_cardinality_cats = [
            col for col in df.select_dtypes(include=["object", "category"]).columns
            if 1 < df[col].nunique() <= 50
        ]
        for col in low_cardinality_cats[:5]:  # top 5 candidates
            vc = df[col].value_counts(dropna=False)
            counts = vc.values
            imbalance = float(max(counts) / max(min(counts), 1))
            result[col] = {
                "num_classes": int(df[col].nunique()),
                "distribution": {str(k): int(v) for k, v in vc.items()},
                "imbalance_ratio": round(imbalance, 2),
                "is_imbalanced": imbalance > 3.0,
            }
        return result

    def _detect_ewaste_domain(self, df: pd.DataFrame) -> dict:
        """Detect whether columns match e-waste domain semantics."""
        detected = {}
        col_names_lower = [c.lower() for c in df.columns]
        for domain, keywords in EWASTE_KEYWORDS.items():
            matched = [
                df.columns[i] for i, name in enumerate(col_names_lower)
                if any(kw in name for kw in keywords)
            ]
            if matched:
                detected[domain] = matched
        is_ewaste = len(detected) >= 2
        return {
            "is_ewaste_dataset": is_ewaste,
            "detected_domains": detected,
            "confidence": "high" if len(detected) >= 4 else "medium" if len(detected) >= 2 else "low",
        }

    def _find_data_issues(self, df: pd.DataFrame) -> list:
        issues = []
        # Completely empty columns
        empty_cols = [col for col in df.columns if df[col].isnull().all()]
        if empty_cols:
            issues.append({"type": "empty_columns", "columns": empty_cols,
                           "severity": "high", "action": "Drop or investigate"})
        # Near-zero variance
        num_cols = df.select_dtypes(include="number")
        for col in num_cols.columns:
            if df[col].nunique() <= 1:
                issues.append({"type": "zero_variance", "column": col,
                               "severity": "medium", "action": "Drop — no predictive value"})
        # Columns with >80% missing
        missing_pct = df.isnull().mean()
        for col, pct in missing_pct[missing_pct > 0.8].items():
            issues.append({"type": "high_missing", "column": col,
                           "pct": round(float(pct) * 100, 1),
                           "severity": "high", "action": "Consider dropping"})
        # Mixed types (object column with numeric-looking values)
        for col in df.select_dtypes(include="object").columns:
            try:
                converted = pd.to_numeric(df[col].dropna(), errors="coerce")
                valid_pct = converted.notna().mean()
                if 0.3 < valid_pct < 0.9:
                    issues.append({"type": "mixed_types", "column": col,
                                   "numeric_pct": round(float(valid_pct) * 100, 1),
                                   "severity": "medium", "action": "Investigate — mixed numeric/text"})
            except Exception:
                pass
        return issues

    def _dataframe_checksum(self, df: pd.DataFrame) -> str:
        try:
            return hashlib.md5(pd.util.hash_pandas_object(df, index=True).values).hexdigest()
        except Exception:
            return "unknown"

    def to_json(self) -> str:
        return json.dumps(self.report, indent=2, default=str)


# ------------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------------
def _infer_col_type(series: pd.Series) -> str:
    if pd.api.types.is_integer_dtype(series):
        return "integer"
    if pd.api.types.is_float_dtype(series):
        return "float"
    if pd.api.types.is_bool_dtype(series):
        return "boolean"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    if pd.api.types.is_categorical_dtype(series):
        return "categorical"
    # Try numeric coercion
    if series.dtype == object:
        converted = pd.to_numeric(series.dropna(), errors="coerce")
        if converted.notna().mean() > 0.9:
            return "numeric_string"
    return "text"


def _has_mixed_case(series: pd.Series) -> bool:
    sample = series.dropna().astype(str).head(100)
    lower = (sample == sample.str.lower()).mean()
    return not (lower > 0.95 or lower < 0.05)


def _has_whitespace_issues(series: pd.Series) -> bool:
    sample = series.dropna().astype(str).head(100)
    return (sample != sample.str.strip()).any()


def _file_hash(path: Path, chunk_size: int = 65536) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()
