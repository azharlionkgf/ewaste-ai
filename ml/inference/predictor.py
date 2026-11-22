"""
ModelPredictor: inference interface for CNN and tabular models.
Handles image and tabular predictions with top-k ranking and batch support.
"""

import json
import logging
import pathlib
from typing import Any, Dict, List, Optional

import joblib
import numpy as np
import torch
import torchvision.transforms as T
from PIL import Image

logger = logging.getLogger(__name__)

# Default image preprocessing for CNN inference
_DEFAULT_TRANSFORM = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406],
                std =[0.229, 0.224, 0.225]),
])


class ModelPredictor:
    """
    Unified inference interface for E-WASTE AI models.

    Parameters
    ----------
    model_path : str
        Path to the saved model file (.pt for CNN, .joblib for tabular).
    model_type : str
        ``'cnn'`` or ``'tabular'``.
    class_names : list[str], optional
        Human-readable class names; index i → class_names[i].
    device : str
        Torch device string.  Defaults to ``'cpu'``.
    """

    def __init__(
        self,
        model_path: str,
        model_type: str,
        class_names: Optional[List[str]] = None,
        device: str = "cpu",
    ):
        self.model_path  = pathlib.Path(model_path)
        self.model_type  = model_type.lower()
        self.class_names = class_names or []
        self.device      = torch.device(device)
        self.model       = None

        logger.debug(
            "ModelPredictor: type=%s path=%s device=%s",
            self.model_type, self.model_path, self.device,
        )

    # ------------------------------------------------------------------
    # Model loading
    # ------------------------------------------------------------------

    def load_model(self) -> None:
        """
        Load the model from self.model_path.
        CNN  → torch.load state_dict (requires ml.models.cnn.classifier).
        Tabular → joblib.load (scikit-learn pipeline / estimator).
        """
        try:
            if self.model_type == "cnn":
                self._load_cnn()
            elif self.model_type == "tabular":
                self._load_tabular()
            else:
                raise ValueError(f"Unknown model_type: '{self.model_type}'")
            logger.info("Model loaded from %s", self.model_path)
        except Exception as exc:
            logger.error("load_model failed: %s", exc)
            raise

    def _load_cnn(self) -> None:
        try:
            from ml.models.cnn.classifier import build_cnn_classifier
            num_classes = len(self.class_names) if self.class_names else 10
            self.model = build_cnn_classifier(num_classes=num_classes)
        except ImportError:
            # Minimal fallback so predictor is still usable in tests
            logger.warning("build_cnn_classifier not found; loading raw state_dict.")
            self.model = None

        state_dict = torch.load(
            self.model_path, map_location=self.device, weights_only=True
        )

        if self.model is None:
            # We can't reconstruct architecture — wrap state_dict for reference
            logger.error(
                "Cannot load CNN without build_cnn_classifier.  "
                "Predictions will fail."
            )
            return

        self.model.load_state_dict(state_dict)
        self.model.to(self.device)
        self.model.eval()

    def _load_tabular(self) -> None:
        self.model = joblib.load(self.model_path)
        logger.debug("Tabular model type: %s", type(self.model).__name__)

    # ------------------------------------------------------------------
    # Image prediction
    # ------------------------------------------------------------------

    def predict_image(
        self, image_path: str, top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Predict the class of a single image.

        Returns
        -------
        list[dict]
            Sorted by confidence (descending).  Each dict has:
            ``class_name``, ``class_index``, ``confidence``, ``rank``.
        """
        try:
            if self.model is None:
                raise RuntimeError("Model not loaded.  Call load_model() first.")

            tensor = self._preprocess_image(image_path)
            with torch.no_grad():
                logits = self.model(tensor)
                probs  = torch.softmax(logits, dim=1).squeeze(0).cpu().numpy()

            return self._top_k_results(probs, top_k)

        except Exception as exc:
            logger.error("predict_image failed for %s: %s", image_path, exc)
            return [{"error": str(exc), "image_path": str(image_path)}]

    def predict_batch_images(
        self, image_paths: List[str], top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Predict classes for a list of image paths.

        Returns
        -------
        list[dict]
            One entry per input path; each entry is the same structure as
            ``predict_image`` (a list of top-k dicts) nested under ``predictions``,
            plus ``image_path`` and ``status``.
        """
        results = []
        for path in image_paths:
            try:
                preds = self.predict_image(str(path), top_k=top_k)
                results.append({
                    "image_path":  str(path),
                    "status":      "ok",
                    "predictions": preds,
                })
            except Exception as exc:
                logger.error("predict_batch_images: %s — %s", path, exc)
                results.append({
                    "image_path": str(path),
                    "status":     "error",
                    "error":      str(exc),
                })
        return results

    # ------------------------------------------------------------------
    # Tabular prediction
    # ------------------------------------------------------------------

    def predict_tabular(
        self,
        feature_dict: Dict[str, Any],
        feature_names: List[str],
    ) -> Dict[str, Any]:
        """
        Predict class for a single tabular sample.

        Parameters
        ----------
        feature_dict : dict
            Feature name → value mapping.
        feature_names : list[str]
            Ordered list of feature names the model was trained on.

        Returns
        -------
        dict
            ``predicted_class``, ``predicted_index``, ``confidence``,
            ``all_probabilities``.
        """
        try:
            if self.model is None:
                raise RuntimeError("Model not loaded.  Call load_model() first.")

            # Build ordered feature vector
            X = np.array(
                [[feature_dict.get(f, 0.0) for f in feature_names]],
                dtype=np.float64,
            )

            proba  = self.model.predict_proba(X)[0]
            pred_idx = int(np.argmax(proba))
            confidence = float(proba[pred_idx])

            pred_class = (
                self.class_names[pred_idx]
                if self.class_names and pred_idx < len(self.class_names)
                else str(pred_idx)
            )

            all_probs = {
                (self.class_names[i] if self.class_names and i < len(self.class_names) else str(i)):
                round(float(p), 6)
                for i, p in enumerate(proba)
            }

            return {
                "predicted_class": pred_class,
                "predicted_index": pred_idx,
                "confidence":      round(confidence, 6),
                "all_probabilities": all_probs,
            }

        except Exception as exc:
            logger.error("predict_tabular failed: %s", exc)
            return {
                "error":           str(exc),
                "predicted_class": None,
                "predicted_index": None,
                "confidence":      0.0,
                "all_probabilities": {},
            }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _preprocess_image(self, image_path) -> torch.Tensor:
        """
        Load an image from *image_path* and return a (1, C, H, W) tensor.
        """
        path = pathlib.Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {path}")

        image = Image.open(path).convert("RGB")
        tensor = _DEFAULT_TRANSFORM(image)          # (C, H, W)
        return tensor.unsqueeze(0).to(self.device)  # (1, C, H, W)

    def _top_k_results(
        self, probs: np.ndarray, top_k: int
    ) -> List[Dict[str, Any]]:
        """Convert a probability array into a ranked top-k list."""
        k = min(top_k, len(probs))
        top_indices = np.argsort(probs)[::-1][:k]

        results = []
        for rank, idx in enumerate(top_indices, start=1):
            class_name = (
                self.class_names[idx]
                if self.class_names and idx < len(self.class_names)
                else str(idx)
            )
            results.append({
                "class_name":  class_name,
                "class_index": int(idx),
                "confidence":  round(float(probs[idx]), 6),
                "rank":        rank,
            })

        return results
