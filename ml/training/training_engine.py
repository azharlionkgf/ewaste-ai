"""
Training Engine — Phase 3: AI/ML Training Laboratory
======================================================
Unified training engine for tabular ML and CNN image models.
CPU-first design; GPU used automatically when available.
"""

from __future__ import annotations

import json
import logging
import pickle
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)

MODELS_DIR = Path("models/saved")
HISTORY_DIR = Path("models/history")


class TrainingEngine:
    """
    Reusable training engine supporting tabular ML and CNN image models.

    Usage — Tabular::

        engine = TrainingEngine()
        result = engine.train_tabular(X_train, y_train, X_val, y_val,
                                       algorithm="random_forest", config={})

    Usage — Image::

        result = engine.train_image(train_loader, val_loader,
                                     architecture="mobilenetv3_small", config={})
    """

    def __init__(self, seed: int = 42):
        self.seed = seed
        self._set_global_seed(seed)
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        HISTORY_DIR.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ #
    # TABULAR TRAINING                                                     #
    # ------------------------------------------------------------------ #

    def train_tabular(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        algorithm: str = "random_forest",
        task: str = "classification",   # "classification" | "regression"
        config: dict | None = None,
        run_name: str | None = None,
    ) -> dict:
        """
        Train a tabular model and return a full result dict.

        Returns
        -------
        dict with keys: model, algorithm, task, train_metrics, val_metrics,
                        training_time_s, run_name, config, timestamp, model_path
        """
        cfg = config or {}
        run_name = run_name or f"{algorithm}_{int(time.time())}"
        t0 = time.time()

        model = self._build_tabular_model(algorithm, task, cfg)

        logger.info("Training %s (%s) run='%s'", algorithm, task, run_name)
        model.fit(X_train, y_train)

        training_time = round(time.time() - t0, 2)

        # Metrics
        train_metrics = self._eval_tabular(model, X_train, y_train, task, "train")
        val_metrics   = self._eval_tabular(model, X_val,   y_val,   task, "val")

        # Save
        model_path = self._save_model(model, run_name)

        result = {
            "run_name":        run_name,
            "algorithm":       algorithm,
            "task":            task,
            "config":          cfg,
            "seed":            self.seed,
            "train_metrics":   train_metrics,
            "val_metrics":     val_metrics,
            "training_time_s": training_time,
            "duration_sec":    training_time,   # alias for compatibility
            "model_path":      str(model_path),
            "timestamp":       datetime.now(timezone.utc).isoformat(),
            "model":           model,  # live object for downstream use
        }

        self._save_history(result, run_name)
        logger.info(
            "Training complete: val_%s=%.4f in %.1fs",
            "accuracy" if task == "classification" else "r2",
            val_metrics.get("accuracy", val_metrics.get("r2", 0)),
            training_time,
        )
        return result

    def evaluate_on_test(
        self,
        model: Any,
        X_test: np.ndarray,
        y_test: np.ndarray,
        task: str = "classification",
        class_names: list | None = None,
    ) -> dict:
        """Run final evaluation on held-out test set."""
        return self._eval_tabular(model, X_test, y_test, task, "test",
                                  class_names=class_names)

    # ------------------------------------------------------------------ #
    # IMAGE TRAINING                                                       #
    # ------------------------------------------------------------------ #

    def train_image(
        self,
        train_loader,
        val_loader,
        num_classes: int,
        architecture: str = "mobilenetv3_small",
        config: dict | None = None,
        run_name: str | None = None,
    ) -> dict:
        """
        Train a CNN image classifier with transfer learning.

        Returns full result dict including per-epoch history.
        """
        import torch
        import torch.nn as nn
        import torch.optim as optim

        cfg = {
            "epochs": 10,
            "lr": 1e-3,
            "weight_decay": 1e-4,
            "patience": 5,
            "unfreeze_after": 3,   # unfreeze backbone after N epochs
        }
        if config:
            cfg.update(config)

        run_name = run_name or f"{architecture}_{int(time.time())}"
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info("Image training: arch=%s device=%s run='%s'", architecture, device, run_name)

        from ml.models.cnn.classifier import build_cnn_classifier
        model = build_cnn_classifier(architecture, num_classes).to(device)

        # Freeze backbone initially
        for name, param in model.named_parameters():
            if "classifier" not in name and "fc" not in name:
                param.requires_grad = False

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(
            filter(lambda p: p.requires_grad, model.parameters()),
            lr=cfg["lr"],
            weight_decay=cfg["weight_decay"],
        )
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=2, factor=0.5)

        history = []
        best_val_acc = 0.0
        patience_counter = 0
        best_model_state = None
        t0 = time.time()

        for epoch in range(1, cfg["epochs"] + 1):
            # Unfreeze backbone after N epochs
            if epoch == cfg["unfreeze_after"] + 1:
                for param in model.parameters():
                    param.requires_grad = True
                optimizer = optim.Adam(model.parameters(), lr=cfg["lr"] / 10,
                                       weight_decay=cfg["weight_decay"])
                logger.info("Epoch %d: backbone unfrozen", epoch)

            train_loss, train_acc = self._image_epoch(model, train_loader, criterion,
                                                       optimizer, device, train=True)
            val_loss, val_acc     = self._image_epoch(model, val_loader, criterion,
                                                       None, device, train=False)
            scheduler.step(val_loss)

            epoch_data = {
                "epoch": epoch, "train_loss": round(train_loss, 4),
                "train_acc": round(train_acc, 4), "val_loss": round(val_loss, 4),
                "val_acc": round(val_acc, 4),
            }
            history.append(epoch_data)
            logger.info("Epoch %d/%d  train_acc=%.3f  val_acc=%.3f",
                        epoch, cfg["epochs"], train_acc, val_acc)

            if val_acc > best_val_acc:
                best_val_acc = val_acc
                best_model_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
                patience_counter = 0
            else:
                patience_counter += 1
                if patience_counter >= cfg["patience"]:
                    logger.info("Early stopping at epoch %d", epoch)
                    break

        # Restore best weights
        if best_model_state:
            model.load_state_dict(best_model_state)

        training_time = round(time.time() - t0, 2)
        model_path = self._save_torch_model(model, run_name)

        result = {
            "run_name":         run_name,
            "architecture":     architecture,
            "task":             "image_classification",
            "config":           cfg,
            "seed":             self.seed,
            "best_val_acc":     round(best_val_acc, 4),
            "epochs_completed": len(history),
            "history":          history,
            "training_time_s":  training_time,
            "model_path":       str(model_path),
            "timestamp":        datetime.now(timezone.utc).isoformat(),
            "model":            model,
            "device":           str(device),
        }
        self._save_history(result, run_name)
        return result

    # ------------------------------------------------------------------ #
    # Private helpers                                                      #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _set_global_seed(seed: int) -> None:
        import random
        random.seed(seed)
        np.random.seed(seed)
        try:
            import torch
            torch.manual_seed(seed)
        except ImportError:
            pass

    @staticmethod
    def _build_tabular_model(algorithm: str, task: str, cfg: dict):
        """Build a sklearn-compatible model."""
        seed = cfg.get("random_seed", 42)

        if task == "regression":
            from ml.models.tabular.sklearn_models import build_tabular_regressor
            return build_tabular_regressor(algorithm, cfg, seed)
        else:
            from ml.models.tabular.sklearn_models import build_tabular_classifier
            return build_tabular_classifier(algorithm, cfg, seed)

    @staticmethod
    def _eval_tabular(
        model, X: np.ndarray, y: np.ndarray, task: str, split: str,
        class_names: list | None = None,
    ) -> dict:
        from ml.evaluation.evaluator import evaluate_tabular
        return evaluate_tabular(model, X, y, task=task, split=split,
                                class_names=class_names)

    @staticmethod
    def _image_epoch(model, loader, criterion, optimizer, device, train: bool):
        import torch
        model.train(train)
        total_loss, correct, total = 0.0, 0, 0
        with torch.set_grad_enabled(train):
            for images, labels in loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                if train:
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()
                total_loss += loss.item() * len(labels)
                correct += (outputs.argmax(1) == labels).sum().item()
                total += len(labels)
        return total_loss / max(total, 1), correct / max(total, 1)

    @staticmethod
    def _save_model(model, run_name: str) -> Path:
        path = MODELS_DIR / f"{run_name}.pkl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(model, f)
        return path

    @staticmethod
    def _save_torch_model(model, run_name: str) -> Path:
        import torch
        path = MODELS_DIR / f"{run_name}.pt"
        path.parent.mkdir(parents=True, exist_ok=True)
        torch.save(model.state_dict(), path)
        return path

    @staticmethod
    def _save_history(result: dict, run_name: str) -> None:
        path = HISTORY_DIR / f"{run_name}_history.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        serializable = {k: v for k, v in result.items() if k != "model"}
        with open(path, "w") as f:
            json.dump(serializable, f, indent=2, default=str)

    @staticmethod
    def load_model(model_path: str):
        """Load a saved tabular model from disk."""
        path = Path(model_path)
        if path.suffix == ".pkl":
            with open(path, "rb") as f:
                return pickle.load(f)
        raise ValueError(f"Use load_torch_model() for .pt files")

    @staticmethod
    def load_torch_model(model_path: str, architecture: str, num_classes: int):
        """Load a saved CNN model from disk."""
        import torch
        from ml.models.cnn.classifier import build_cnn_classifier
        model = build_cnn_classifier(architecture, num_classes)
        model.load_state_dict(torch.load(model_path, map_location="cpu"))
        model.eval()
        return model
