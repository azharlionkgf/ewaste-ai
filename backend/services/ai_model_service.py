"""
E-Waste AI — AI Model Integration Engine (Phase 4 Task 3)
==========================================================
Loads, validates, and runs actual trained models from Phase 3.
Never returns hardcoded or fabricated predictions.
If a model is unavailable, clearly reports it.
"""

from __future__ import annotations

import hashlib
import logging
import pickle
from pathlib import Path
from typing import Any, Optional

import numpy as np

from backend.config import MODEL_REGISTRY_DIR, SAVED_MODELS_DIR

logger = logging.getLogger(__name__)


class ModelNotAvailableError(Exception):
    """Raised when a suitable model is not found in the registry."""


class ModelInferenceError(Exception):
    """Raised when model inference fails."""


class AIModelEngine:
    """
    Central engine for loading and running actual trained models.

    Design principles:
    - Only returns predictions from actual trained models.
    - If no suitable model exists, raises ModelNotAvailableError.
    - All predictions are tagged with model_id, version, and prediction_type.
    - Keeps a cache of loaded models for performance.
    """

    def __init__(self):
        self._model_cache: dict[str, Any] = {}
        self._registry_data: dict = {}
        self._load_registry()

    # ── Registry ───────────────────────────────────────────────────────

    def _load_registry(self):
        """Load model registry metadata from disk."""
        registry_file = MODEL_REGISTRY_DIR / "registry.json"
        if not registry_file.exists():
            logger.info("No model registry found at %s — no models available yet.", registry_file)
            self._registry_data = {}
            return
        try:
            import json
            with open(registry_file, "r") as f:
                self._registry_data = json.load(f)
            logger.info("Loaded model registry with %d entries.", len(self._registry_data))
        except Exception as exc:
            logger.error("Failed to load model registry: %s", exc)
            self._registry_data = {}

    def reload_registry(self):
        self._model_cache.clear()
        self._load_registry()

    def list_available_models(self) -> list[dict]:
        """Return list of registered models with their status."""
        result = []
        for model_id, meta in self._registry_data.items():
            result.append({
                "model_id": model_id,
                "name": meta.get("name", model_id),
                "algorithm": meta.get("algorithm"),
                "task_type": meta.get("task_type"),
                "version": meta.get("version"),
                "status": meta.get("status"),
                "metrics": meta.get("metrics", {}),
            })
        return result

    def get_active_model_for_task(self, task_type: str) -> Optional[dict]:
        """Find the active model for a given task type."""
        for model_id, meta in self._registry_data.items():
            if meta.get("status") == "active" and meta.get("task_type") == task_type:
                return {"model_id": model_id, **meta}
        # Fallback: any trained model for this task
        for model_id, meta in self._registry_data.items():
            if meta.get("status") == "trained" and meta.get("task_type") == task_type:
                return {"model_id": model_id, **meta}
        return None

    # ── Model Loading ──────────────────────────────────────────────────

    def _load_model(self, model_id: str) -> Any:
        """Load model from disk into cache."""
        if model_id in self._model_cache:
            return self._model_cache[model_id]

        meta = self._registry_data.get(model_id)
        if not meta:
            raise ModelNotAvailableError(f"Model '{model_id}' not found in registry.")

        file_path = meta.get("file_path")
        if not file_path:
            raise ModelNotAvailableError(f"Model '{model_id}' has no file_path in registry.")

        path = Path(file_path)
        if not path.exists():
            # Try relative to saved models dir
            path = SAVED_MODELS_DIR / path.name
        if not path.exists():
            raise ModelNotAvailableError(
                f"Model file not found: {file_path}. "
                "Train a model first using the AI Training Laboratory."
            )

        try:
            with open(path, "rb") as f:
                model = pickle.load(f)
            self._model_cache[model_id] = model
            logger.info("Loaded model '%s' from %s", model_id, path)
            return model
        except Exception as exc:
            raise ModelInferenceError(f"Failed to load model '{model_id}': {exc}") from exc

    # ── Prediction ─────────────────────────────────────────────────────

    def predict_tabular(
        self,
        input_features: dict,
        task_type: str,
        model_id: Optional[str] = None,
    ) -> dict:
        """
        Run tabular prediction using an actual trained model.

        Returns:
            dict with keys: prediction, confidence, model_id, model_name,
                            model_version, prediction_type, task_type
        """
        # Find model
        if model_id:
            meta = self._registry_data.get(model_id)
            if not meta:
                raise ModelNotAvailableError(f"Model '{model_id}' not found in registry.")
        else:
            meta_with_id = self.get_active_model_for_task(task_type)
            if not meta_with_id:
                raise ModelNotAvailableError(
                    f"No trained model available for task_type='{task_type}'. "
                    "Please train a model first in the AI Training Laboratory."
                )
            model_id = meta_with_id.pop("model_id")
            meta = meta_with_id

        model = self._load_model(model_id)

        # Build feature array
        feature_cols = meta.get("feature_columns", list(input_features.keys()))
        try:
            X = np.array([[input_features.get(col, 0.0) for col in feature_cols]])
        except Exception as exc:
            raise ModelInferenceError(f"Feature preparation failed: {exc}") from exc

        # Predict
        try:
            prediction = model.predict(X)
            pred_value = prediction[0] if hasattr(prediction, "__len__") else prediction

            # Confidence (probability) for classifiers
            confidence = None
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(X)[0]
                confidence = float(np.max(proba))

            return {
                "prediction": _serialize(pred_value),
                "confidence": confidence,
                "model_id": model_id,
                "model_name": meta.get("name", model_id),
                "model_version": meta.get("version"),
                "algorithm": meta.get("algorithm"),
                "task_type": task_type,
                "prediction_type": "actual_model",
                "feature_columns": feature_cols,
            }
        except Exception as exc:
            raise ModelInferenceError(f"Inference failed for model '{model_id}': {exc}") from exc

    def predict_batch(
        self,
        records: list[dict],
        task_type: str,
        model_id: Optional[str] = None,
    ) -> list[dict]:
        """Run predictions on a batch of records."""
        results = []
        for record in records:
            try:
                result = self.predict_tabular(record, task_type, model_id)
                results.append({"input": record, "result": result, "error": None})
            except (ModelNotAvailableError, ModelInferenceError) as exc:
                results.append({"input": record, "result": None, "error": str(exc)})
        return results

    def check_availability(self) -> dict:
        """Check which task types have trained models available."""
        availability = {}
        task_types = [
            "ewaste_classification",
            "device_identification",
            "component_classification",
            "material_classification",
            "recovery_quantity",
            "economic_value",
            "recycling_outcome",
        ]
        for task_type in task_types:
            model = self.get_active_model_for_task(task_type)
            availability[task_type] = {
                "available": model is not None,
                "model_name": model.get("name") if model else None,
                "version": model.get("version") if model else None,
            }
        return availability


def _serialize(value) -> Any:
    """Convert numpy types to Python native types."""
    if hasattr(value, "item"):
        return value.item()
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    return value


# ── Singleton ──────────────────────────────────────────────────────────
_engine_instance: Optional[AIModelEngine] = None


def get_ai_engine() -> AIModelEngine:
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = AIModelEngine()
    return _engine_instance
