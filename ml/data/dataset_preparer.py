"""
Dataset Preparer — Phase 2: Dataset Intelligence Engine
Handles final train/val/test splitting with provenance tracking.
"""

from __future__ import annotations

import json
import logging
import shutil
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)

SPLITS_BASE_DIR = Path("data/splits")


@dataclass
class PreparedDataset:
    """Result of a dataset preparation run."""
    dataset_name: str
    dataset_type: str                    # "tabular" | "image"
    split_paths: dict[str, str]          # {"train": "...", "val": "...", "test": "..."}
    config: dict = field(default_factory=dict)
    stats: dict = field(default_factory=dict)
    provenance: dict = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> dict:
        return asdict(self)


class DatasetPreparer:
    """
    Prepares tabular and image datasets for model training.

    Usage::

        preparer = DatasetPreparer()
        result = preparer.prepare_tabular(df, "label", config={"train_ratio": 0.7})
    """

    # ------------------------------------------------------------------ #
    # Tabular                                                              #
    # ------------------------------------------------------------------ #

    def prepare_tabular(
        self,
        df: pd.DataFrame,
        target_col: str,
        feature_cols: list[str] | None = None,
        config: dict | None = None,
        dataset_name: str = "dataset",
    ) -> PreparedDataset:
        """
        Validate, split, and save a tabular dataset.

        Parameters
        ----------
        df: Input DataFrame (original — not modified).
        target_col: Target / label column.
        feature_cols: Feature columns.  None → all except target.
        config: Optional config overrides (train_ratio, val_ratio, test_ratio,
                random_seed, stratify).
        dataset_name: Used for output directory name.

        Returns
        -------
        PreparedDataset with paths to saved splits.
        """
        cfg = {
            "train_ratio": 0.70,
            "val_ratio": 0.15,
            "test_ratio": 0.15,
            "random_seed": 42,
            "stratify": True,
        }
        if config:
            cfg.update(config)

        # --- validate --------------------------------------------------
        if target_col not in df.columns:
            raise ValueError(f"target_col '{target_col}' not found in DataFrame")

        if feature_cols is None:
            feature_cols = [c for c in df.columns if c != target_col]

        if target_col in feature_cols:
            raise ValueError("target_col must not be in feature_cols (data leakage)")

        ratios = cfg["train_ratio"] + cfg["val_ratio"] + cfg["test_ratio"]
        if abs(ratios - 1.0) > 1e-6:
            raise ValueError(f"Ratios must sum to 1.0, got {ratios:.4f}")

        # --- work on a clean copy --------------------------------------
        keep_cols = feature_cols + [target_col]
        df_clean = df[keep_cols].dropna(subset=[target_col]).reset_index(drop=True)

        y = df_clean[target_col]

        stratify_arr = y if cfg["stratify"] and y.nunique() > 1 else None
        try:
            df_train_val, df_test = train_test_split(
                df_clean,
                test_size=cfg["test_ratio"],
                random_state=cfg["random_seed"],
                stratify=stratify_arr,
            )
            val_relative = cfg["val_ratio"] / (cfg["train_ratio"] + cfg["val_ratio"])
            stratify_tv = df_train_val[target_col] if cfg["stratify"] and df_train_val[target_col].nunique() > 1 else None
            df_train, df_val = train_test_split(
                df_train_val,
                test_size=val_relative,
                random_state=cfg["random_seed"],
                stratify=stratify_tv,
            )
        except ValueError as exc:
            logger.warning("Stratified split failed (%s); using random split", exc)
            df_train_val, df_test = train_test_split(
                df_clean, test_size=cfg["test_ratio"], random_state=cfg["random_seed"]
            )
            val_relative = cfg["val_ratio"] / (cfg["train_ratio"] + cfg["val_ratio"])
            df_train, df_val = train_test_split(
                df_train_val, test_size=val_relative, random_state=cfg["random_seed"]
            )

        # --- save -------------------------------------------------------
        out_dir = SPLITS_BASE_DIR / dataset_name
        out_dir.mkdir(parents=True, exist_ok=True)

        paths = {
            "train": str(out_dir / "train.csv"),
            "val":   str(out_dir / "val.csv"),
            "test":  str(out_dir / "test.csv"),
        }
        df_train.to_csv(paths["train"], index=False)
        df_val.to_csv(paths["val"],   index=False)
        df_test.to_csv(paths["test"], index=False)

        # --- stats ------------------------------------------------------
        stats = {
            "total_samples": len(df_clean),
            "train_samples": len(df_train),
            "val_samples":   len(df_val),
            "test_samples":  len(df_test),
            "features": feature_cols,
            "target": target_col,
            "n_classes": int(y.nunique()),
            "class_distribution": y.value_counts().to_dict(),
        }

        # --- provenance -------------------------------------------------
        provenance = {
            "dataset_name": dataset_name,
            "source_rows": len(df),
            "source_cols": len(df.columns),
            "preparation_config": cfg,
            "feature_cols": feature_cols,
            "target_col": target_col,
            "split_stats": stats,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        with open(out_dir / "provenance.json", "w") as fh:
            json.dump(provenance, fh, indent=2, default=str)

        logger.info("Prepared %s: %d train / %d val / %d test", dataset_name,
                    len(df_train), len(df_val), len(df_test))

        return PreparedDataset(
            dataset_name=dataset_name,
            dataset_type="tabular",
            split_paths=paths,
            config=cfg,
            stats=stats,
            provenance=provenance,
        )

    # ------------------------------------------------------------------ #
    # Image                                                                #
    # ------------------------------------------------------------------ #

    def prepare_images(
        self,
        root_dir: str | Path,
        output_dir: str | Path,
        config: dict | None = None,
        dataset_name: str = "image_dataset",
    ) -> PreparedDataset:
        """
        Split an image dataset (class-per-folder) into train / val / test.

        Copies images into ``output_dir/{train,val,test}/{class_name}/``.
        Also saves CSV manifests listing each image path + label.
        """
        cfg = {
            "train_ratio": 0.70,
            "val_ratio": 0.15,
            "test_ratio": 0.15,
            "random_seed": 42,
        }
        if config:
            cfg.update(config)

        root = Path(root_dir)
        out = Path(output_dir)
        rng = np.random.default_rng(cfg["random_seed"])

        SUPPORTED = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}

        split_names = ["train", "val", "test"]
        for s in split_names:
            (out / s).mkdir(parents=True, exist_ok=True)

        manifests: dict[str, list[dict]] = {s: [] for s in split_names}
        stats: dict[str, Any] = {"classes": {}, "total": 0}

        for class_dir in sorted(root.iterdir()):
            if not class_dir.is_dir():
                continue
            class_name = class_dir.name
            images = [
                f for f in class_dir.rglob("*")
                if f.is_file() and f.suffix.lower() in SUPPORTED
            ]
            if not images:
                continue

            indices = rng.permutation(len(images))
            n_train = int(len(images) * cfg["train_ratio"])
            n_val   = int(len(images) * cfg["val_ratio"])

            split_indices = {
                "train": indices[:n_train],
                "val":   indices[n_train: n_train + n_val],
                "test":  indices[n_train + n_val:],
            }
            stats["classes"][class_name] = {s: int(len(split_indices[s])) for s in split_names}
            stats["total"] += len(images)

            for split, idx in split_indices.items():
                dst_class = out / split / class_name
                dst_class.mkdir(parents=True, exist_ok=True)
                for i in idx:
                    src = images[i]
                    dst = dst_class / src.name
                    shutil.copy2(src, dst)
                    manifests[split].append({
                        "filepath": str(dst),
                        "label": class_name,
                        "original": str(src),
                    })

        # Save manifests
        out_splits = SPLITS_BASE_DIR / dataset_name
        out_splits.mkdir(parents=True, exist_ok=True)
        paths: dict[str, str] = {}
        for split, rows in manifests.items():
            csv_path = str(out_splits / f"{split}.csv")
            pd.DataFrame(rows).to_csv(csv_path, index=False)
            paths[split] = csv_path

        provenance = {
            "dataset_name": dataset_name,
            "root_dir": str(root),
            "output_dir": str(out),
            "config": cfg,
            "stats": stats,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        with open(out_splits / "provenance.json", "w") as fh:
            json.dump(provenance, fh, indent=2, default=str)

        logger.info("Image dataset prepared: %s", dataset_name)
        return PreparedDataset(
            dataset_name=dataset_name,
            dataset_type="image",
            split_paths=paths,
            config=cfg,
            stats=stats,
            provenance=provenance,
        )
