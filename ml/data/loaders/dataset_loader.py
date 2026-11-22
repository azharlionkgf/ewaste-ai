"""
E-Waste AI — Dataset Loader
=============================
Handles loading of CSV, Excel, JSON, and image datasets.
Returns Pandas DataFrames for tabular data.
Returns image paths + labels for image data.

Used in Phase 2 (Cleaning) and Phase 4 (Training).
"""

import os
import json
import hashlib
import logging
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

# Supported file extensions
TABULAR_EXTENSIONS = {".csv", ".xlsx", ".xls", ".json"}
IMAGE_EXTENSIONS   = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff"}


def compute_sha256(file_path: str) -> str:
    """Compute SHA-256 checksum of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def load_tabular_dataset(
    file_path: str,
    sheet_name: Optional[str] = None,
    encoding: str = "utf-8",
) -> pd.DataFrame:
    """
    Load a tabular dataset from CSV, Excel, or JSON.

    Args:
        file_path:  Path to the file
        sheet_name: Excel sheet name (optional)
        encoding:   Text encoding for CSV

    Returns:
        pandas DataFrame
    """
    path = Path(file_path)
    ext  = path.suffix.lower()

    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {file_path}")

    logger.info(f"Loading {ext} dataset: {path.name}")

    if ext == ".csv":
        try:
            df = pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding="latin-1")

    elif ext in {".xlsx", ".xls"}:
        df = pd.read_excel(file_path, sheet_name=sheet_name or 0)

    elif ext == ".json":
        df = pd.read_json(file_path)

    else:
        raise ValueError(f"Unsupported tabular format: {ext}. Use CSV, Excel or JSON.")

    logger.info(f"Loaded dataset: {df.shape[0]} rows × {df.shape[1]} columns")
    return df


def inspect_tabular_dataset(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate a comprehensive inspection report for a tabular dataset.

    Returns:
        dict with shape, dtypes, missing values, duplicates, basic stats
    """
    total_cells = df.shape[0] * df.shape[1]

    null_counts = df.isnull().sum().to_dict()
    null_pct    = {k: round(v / df.shape[0] * 100, 2) for k, v in null_counts.items()}

    report = {
        "rows":              df.shape[0],
        "columns":           df.shape[1],
        "column_names":      list(df.columns),
        "dtypes":            {k: str(v) for k, v in df.dtypes.to_dict().items()},
        "total_missing":     int(df.isnull().sum().sum()),
        "missing_percent":   round(df.isnull().sum().sum() / total_cells * 100, 2),
        "null_per_column":   null_counts,
        "null_pct_per_col":  null_pct,
        "duplicate_rows":    int(df.duplicated().sum()),
        "numeric_columns":   list(df.select_dtypes(include=[np.number]).columns),
        "categorical_columns": list(df.select_dtypes(include=["object", "category"]).columns),
        "memory_usage_mb":   round(df.memory_usage(deep=True).sum() / 1e6, 3),
    }

    # Value counts for categorical columns (top 10 each)
    cat_distributions = {}
    for col in report["categorical_columns"][:10]:  # limit to 10 columns
        cat_distributions[col] = df[col].value_counts().head(20).to_dict()
    report["categorical_distributions"] = cat_distributions

    # Basic stats for numeric columns
    if report["numeric_columns"]:
        stats = df[report["numeric_columns"]].describe().to_dict()
        report["numeric_stats"] = {
            col: {k: round(v, 4) for k, v in vals.items()}
            for col, vals in stats.items()
        }

    return report


def load_image_dataset(
    folder_path: str,
    class_subdirs: bool = True,
) -> Tuple[List[str], List[str]]:
    """
    Load an image dataset from a folder.

    Args:
        folder_path:   Path to dataset root folder
        class_subdirs: If True, subdirectory names are class labels
                       If False, all images are unlabeled

    Returns:
        (image_paths, labels) — lists of equal length
        If class_subdirs=False, labels are all empty strings.
    """
    root = Path(folder_path)
    if not root.exists():
        raise FileNotFoundError(f"Image dataset folder not found: {folder_path}")

    image_paths: List[str] = []
    labels: List[str] = []

    if class_subdirs:
        for class_dir in sorted(root.iterdir()):
            if class_dir.is_dir():
                class_name = class_dir.name
                for img_file in sorted(class_dir.iterdir()):
                    if img_file.suffix.lower() in IMAGE_EXTENSIONS:
                        image_paths.append(str(img_file))
                        labels.append(class_name)
    else:
        for img_file in sorted(root.rglob("*")):
            if img_file.is_file() and img_file.suffix.lower() in IMAGE_EXTENSIONS:
                image_paths.append(str(img_file))
                labels.append("")

    logger.info(f"Found {len(image_paths)} images | Classes: {sorted(set(labels)) if labels[0] else 'unlabeled'}")
    return image_paths, labels


def inspect_image_dataset(image_paths: List[str], labels: List[str]) -> Dict[str, Any]:
    """Generate inspection report for an image dataset."""
    from collections import Counter

    class_dist = dict(Counter(labels))
    total = len(image_paths)

    return {
        "total_images":       total,
        "num_classes":        len(class_dist),
        "class_names":        sorted(class_dist.keys()),
        "class_distribution": class_dist,
        "class_balance":      {k: round(v/total*100, 2) for k, v in class_dist.items()},
        "is_balanced":        (max(class_dist.values()) / max(min(class_dist.values()), 1)) < 3,
    }


def get_dataset_metadata(file_path: str) -> Dict[str, Any]:
    """Get basic file metadata for a dataset."""
    path = Path(file_path)
    return {
        "filename":     path.name,
        "extension":    path.suffix.lower(),
        "file_size_mb": round(path.stat().st_size / 1e6, 3),
        "checksum":     compute_sha256(file_path),
    }
