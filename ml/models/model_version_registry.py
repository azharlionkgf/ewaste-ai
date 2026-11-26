"""
Model Registry — Phase 3: AI/ML Training Laboratory
=====================================================
Persistent model registry with version management, metadata, and activation.
"""

from __future__ import annotations

import json
import logging
import pickle
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)

REGISTRY_DIR  = Path("models/registry")
REGISTRY_FILE = REGISTRY_DIR / "registry.json"


class ModelRegistry:
    """
    File-based model registry with versioning and DB integration.

    Usage::

        registry = ModelRegistry()
        entry_id = registry.register(run_name, model_path, metadata)
        registry.activate(entry_id)
        model = registry.load_model(entry_id)
    """

    def __init__(self, registry_dir: str | None = None):
        global REGISTRY_DIR, REGISTRY_FILE
        if registry_dir:
            REGISTRY_DIR = Path(registry_dir)
            REGISTRY_FILE = REGISTRY_DIR / "registry.json"
        REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
        self._data: dict[str, dict] = self._load_registry()

    # ------------------------------------------------------------------ #
    # Public API                                                           #
    # ------------------------------------------------------------------ #

    def register(
        self,
        run_name: str,
        model_path: str,
        metadata: dict | None = None,
    ) -> str:
        """Register a trained model. Returns its registry entry_id."""
        entry_id = f"{run_name}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
        meta = metadata or {}

        # Copy model to registry directory
        src = Path(model_path)
        dst = REGISTRY_DIR / src.name
        if src.exists() and src != dst:
            shutil.copy2(src, dst)

        entry = {
            "entry_id":          entry_id,
            "run_name":          run_name,
            "algorithm":         meta.get("algorithm", "unknown"),
            "model_type":        meta.get("model_type", "tabular"),
            "task":              meta.get("task", "classification"),
            "dataset_name":      meta.get("dataset_name", "unknown"),
            "dataset_version":   meta.get("dataset_version", "1.0"),
            "feature_columns":   meta.get("feature_columns", []),
            "target_column":     meta.get("target_column", ""),
            "class_names":       meta.get("class_names", []),
            "hyperparameters":   meta.get("config", {}),
            "train_metrics":     meta.get("train_metrics", {}),
            "val_metrics":       meta.get("val_metrics", {}),
            "test_metrics":      meta.get("test_metrics", {}),
            "training_time_s":   meta.get("training_time_s", 0),
            "model_path":        str(dst),
            "model_size_kb":     round(dst.stat().st_size / 1024, 1) if dst.exists() else 0,
            "random_seed":       meta.get("seed", 42),
            "status":            "registered",   # registered|active|archived
            "registered_at":     datetime.now(timezone.utc).isoformat(),
            "library_versions":  _get_library_versions(),
        }

        self._data[entry_id] = entry
        self._save_registry()
        logger.info("Model registered: entry_id=%s algorithm=%s", entry_id, entry["algorithm"])
        return entry_id

    def activate(self, entry_id: str) -> None:
        """Mark a model as active; deactivate all others with the same algorithm."""
        if entry_id not in self._data:
            raise KeyError(f"Entry '{entry_id}' not found in registry")
        algo = self._data[entry_id]["algorithm"]
        for eid, entry in self._data.items():
            if entry["algorithm"] == algo and entry["status"] == "active":
                self._data[eid]["status"] = "archived"
        self._data[entry_id]["status"] = "active"
        self._save_registry()
        logger.info("Model activated: %s", entry_id)

    def archive(self, entry_id: str) -> None:
        """Archive a model entry."""
        if entry_id in self._data:
            self._data[entry_id]["status"] = "archived"
            self._save_registry()

    def get(self, entry_id: str) -> dict:
        """Return a single registry entry."""
        if entry_id not in self._data:
            raise KeyError(f"Entry '{entry_id}' not found")
        return self._data[entry_id]

    def list_all(self, status_filter: str | None = None) -> list[dict]:
        """Return all registry entries, optionally filtered by status."""
        entries = list(self._data.values())
        if status_filter:
            entries = [e for e in entries if e.get("status") == status_filter]
        return sorted(entries, key=lambda x: x["registered_at"], reverse=True)

    def get_active(self, algorithm: str) -> dict | None:
        """Return the currently active model for a given algorithm."""
        for entry in self._data.values():
            if entry["algorithm"] == algorithm and entry["status"] == "active":
                return entry
        return None

    def compare_versions(self, entry_ids: list[str]) -> list[dict]:
        """Compare metrics for multiple registry entries."""
        rows = []
        for eid in entry_ids:
            if eid in self._data:
                e = self._data[eid]
                val = e.get("val_metrics", {})
                test = e.get("test_metrics", {})
                rows.append({
                    "entry_id":    eid,
                    "algorithm":   e["algorithm"],
                    "status":      e["status"],
                    "val_f1":      val.get("f1_macro", val.get("r2", "N/A")),
                    "test_f1":     test.get("f1_macro", test.get("r2", "N/A")),
                    "val_acc":     val.get("accuracy", "N/A"),
                    "test_acc":    test.get("accuracy", "N/A"),
                    "train_time":  e.get("training_time_s", 0),
                    "registered":  e["registered_at"][:10],
                })
        return rows

    def load_model(self, entry_id: str) -> Any:
        """Load and return the model object for an entry."""
        entry = self.get(entry_id)
        path = Path(entry["model_path"])
        if not path.exists():
            raise FileNotFoundError(f"Model file not found: {path}")
        if path.suffix == ".pkl":
            with open(path, "rb") as f:
                return pickle.load(f)
        raise ValueError(f"Use load_torch_model() for .pt files")

    def export_metadata(self, entry_id: str, output_path: str) -> str:
        """Export registry entry metadata to JSON."""
        entry = self.get(entry_id)
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(entry, f, indent=2, default=str)
        return str(path)

    def update_test_metrics(self, entry_id: str, test_metrics: dict) -> None:
        """Add final test-set metrics to a registered model."""
        if entry_id in self._data:
            self._data[entry_id]["test_metrics"] = test_metrics
            self._save_registry()

    def delete(self, entry_id: str, delete_file: bool = False) -> None:
        """Remove an entry from the registry."""
        if entry_id not in self._data:
            return
        if delete_file:
            path = Path(self._data[entry_id].get("model_path", ""))
            if path.exists():
                path.unlink()
        del self._data[entry_id]
        self._save_registry()
        logger.info("Registry entry deleted: %s", entry_id)

    # ------------------------------------------------------------------ #
    # Private                                                              #
    # ------------------------------------------------------------------ #

    def _load_registry(self) -> dict:
        if REGISTRY_FILE.exists():
            try:
                with open(REGISTRY_FILE) as f:
                    return json.load(f)
            except Exception as exc:
                logger.warning("Could not load registry file: %s", exc)
        return {}

    def _save_registry(self) -> None:
        with open(REGISTRY_FILE, "w") as f:
            json.dump(self._data, f, indent=2, default=str)


def _get_library_versions() -> dict:
    """Capture key library versions for reproducibility."""
    versions: dict[str, str] = {}
    for lib in ["sklearn", "xgboost", "catboost", "torch", "numpy", "pandas"]:
        try:
            import importlib
            m = importlib.import_module(lib if lib != "sklearn" else "sklearn")
            versions[lib] = getattr(m, "__version__", "unknown")
        except ImportError:
            pass
    return versions
