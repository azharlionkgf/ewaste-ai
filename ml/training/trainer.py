"""
ModelTrainer: unified training interface for CNN and tabular models.
Supports early stopping, history tracking, and model persistence.
"""

import json
import logging
import pathlib
import time
from typing import Any, Dict

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import accuracy_score, f1_score

logger = logging.getLogger(__name__)


class ModelTrainer:
    """
    Unified trainer for CNN and tabular classifiers in the E-WASTE AI project.

    Parameters
    ----------
    model_type : str
        One of ``'cnn'`` or ``'tabular'``.
    model_name : str
        Human-readable identifier (used in history and file names).
    num_classes : int
        Number of output classes.
    device : str
        Torch device string.  Defaults to ``'cpu'``.
    """

    def __init__(
        self,
        model_type: str,
        model_name: str,
        num_classes: int,
        device: str = "cpu",
    ):
        self.model_type  = model_type.lower()
        self.model_name  = model_name
        self.num_classes = num_classes
        self.device      = torch.device(device)
        self.model       = None
        self._history: Dict[str, Any] = {}

        logger.info(
            "ModelTrainer init: type=%s name=%s classes=%d device=%s",
            self.model_type, self.model_name, self.num_classes, self.device,
        )

    # ------------------------------------------------------------------
    # Internal model builder
    # ------------------------------------------------------------------

    def _build_model(self):
        """Instantiate the appropriate model and move it to self.device."""
        if self.model_type == "cnn":
            try:
                from ml.models.cnn.classifier import build_cnn_classifier
                self.model = build_cnn_classifier(num_classes=self.num_classes)
            except ImportError:
                logger.warning(
                    "ml.models.cnn.classifier not found; using placeholder CNN."
                )
                self.model = _PlaceholderCNN(self.num_classes)
        elif self.model_type == "tabular":
            try:
                from ml.models.tabular.classifier import build_tabular_classifier
                self.model = build_tabular_classifier(num_classes=self.num_classes)
            except ImportError:
                logger.warning(
                    "ml.models.tabular.classifier not found; using placeholder tabular model."
                )
                self.model = None   # scikit-learn models have no .to()
        else:
            raise ValueError(f"Unknown model_type: '{self.model_type}'")

        if self.model is not None and hasattr(self.model, "to"):
            self.model = self.model.to(self.device)

        logger.debug("Model built: %s", type(self.model).__name__)

    # ------------------------------------------------------------------
    # Tabular training
    # ------------------------------------------------------------------

    def train_tabular(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val:   np.ndarray,
        y_val:   np.ndarray,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Fit a scikit-learn–compatible tabular classifier.

        Returns
        -------
        dict
            History dict with final metrics and mandatory keys.
        """
        logger.info("train_tabular: %d train, %d val samples", len(X_train), len(X_val))
        t0 = time.time()

        self._build_model()

        if self.model is None:
            # Fallback: RandomForestClassifier
            from sklearn.ensemble import RandomForestClassifier
            self.model = RandomForestClassifier(
                n_estimators=kwargs.get("n_estimators", 100),
                random_state=kwargs.get("random_state", 42),
                n_jobs=-1,
            )

        self.model.fit(X_train, y_train)

        # --- Evaluate --------------------------------------------------------
        train_preds = self.model.predict(X_train)
        val_preds   = self.model.predict(X_val)

        train_acc = accuracy_score(y_train, train_preds)
        val_acc   = accuracy_score(y_val,   val_preds)
        val_f1    = f1_score(y_val, val_preds, average="weighted", zero_division=0)

        elapsed = time.time() - t0

        self._history = {
            "model_name":        self.model_name,
            "model_type":        self.model_type,
            "num_classes":       self.num_classes,
            "epochs_run":        1,          # tabular = single fit
            "best_val_accuracy": val_acc,
            "training_complete": True,
            "train_accuracy":    train_acc,
            "val_accuracy":      val_acc,
            "val_f1_weighted":   val_f1,
            "elapsed_sec":       round(elapsed, 3),
        }

        logger.info(
            "train_tabular done — train_acc=%.4f val_acc=%.4f val_f1=%.4f",
            train_acc, val_acc, val_f1,
        )

        return self._history

    # ------------------------------------------------------------------
    # CNN training
    # ------------------------------------------------------------------

    def train_cnn(
        self,
        train_loader,
        val_loader,
        epochs:  int   = 20,
        lr:      float = 0.001,
        patience: int  = 5,
    ) -> Dict[str, Any]:
        """
        Train a PyTorch CNN with cross-entropy loss and Adam optimiser.

        Returns
        -------
        dict
            History dict including per-epoch train_loss, val_loss,
            train_acc, val_acc lists and mandatory summary keys.
        """
        from ml.training.callbacks import EarlyStopping

        logger.info(
            "train_cnn: epochs=%d lr=%f patience=%d device=%s",
            epochs, lr, patience, self.device,
        )

        self._build_model()

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=lr)
        early_stop = EarlyStopping(patience=patience, min_delta=0.001, mode="max")

        train_losses, val_losses   = [], []
        train_accs,   val_accs     = [], []
        best_val_acc  = 0.0
        best_epoch    = 0
        t0            = time.time()

        for epoch in range(1, epochs + 1):
            # --- Training phase ------------------------------------------
            self.model.train()
            running_loss = 0.0
            correct      = 0
            total        = 0

            for batch_x, batch_y in train_loader:
                batch_x = batch_x.to(self.device)
                batch_y = batch_y.to(self.device)

                optimizer.zero_grad()
                outputs = self.model(batch_x)
                loss    = criterion(outputs, batch_y)
                loss.backward()
                optimizer.step()

                running_loss += loss.item() * batch_x.size(0)
                preds    = outputs.argmax(dim=1)
                correct += (preds == batch_y).sum().item()
                total   += batch_x.size(0)

            epoch_train_loss = running_loss / max(total, 1)
            epoch_train_acc  = correct      / max(total, 1)

            # --- Validation phase ----------------------------------------
            self.model.eval()
            val_loss = 0.0
            val_correct = 0
            val_total   = 0

            with torch.no_grad():
                for batch_x, batch_y in val_loader:
                    batch_x = batch_x.to(self.device)
                    batch_y = batch_y.to(self.device)

                    outputs  = self.model(batch_x)
                    loss     = criterion(outputs, batch_y)
                    val_loss += loss.item() * batch_x.size(0)
                    preds    = outputs.argmax(dim=1)
                    val_correct += (preds == batch_y).sum().item()
                    val_total   += batch_x.size(0)

            epoch_val_loss = val_loss    / max(val_total, 1)
            epoch_val_acc  = val_correct / max(val_total, 1)

            train_losses.append(round(epoch_train_loss, 6))
            val_losses.append(round(epoch_val_loss, 6))
            train_accs.append(round(epoch_train_acc, 6))
            val_accs.append(round(epoch_val_acc, 6))

            if epoch_val_acc > best_val_acc:
                best_val_acc = epoch_val_acc
                best_epoch   = epoch

            logger.info(
                "Epoch %d/%d — train_loss=%.4f train_acc=%.4f "
                "val_loss=%.4f val_acc=%.4f",
                epoch, epochs,
                epoch_train_loss, epoch_train_acc,
                epoch_val_loss,   epoch_val_acc,
            )

            if early_stop(epoch_val_acc):
                logger.info("Early stopping at epoch %d.", epoch)
                break

        elapsed = time.time() - t0

        self._history = {
            "model_name":        self.model_name,
            "model_type":        self.model_type,
            "num_classes":       self.num_classes,
            "epochs_run":        len(train_losses),
            "best_val_accuracy": best_val_acc,
            "best_epoch":        best_epoch,
            "training_complete": True,
            "train_loss":        train_losses,
            "val_loss":          val_losses,
            "train_acc":         train_accs,
            "val_acc":           val_accs,
            "elapsed_sec":       round(elapsed, 3),
        }

        logger.info(
            "train_cnn done — epochs_run=%d best_val_acc=%.4f",
            self._history["epochs_run"], best_val_acc,
        )

        return self._history

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save_model(self, save_dir: str) -> str:
        """
        Save the trained model to *save_dir*.

        * PyTorch models  → ``<model_name>.pt``  (state_dict)
        * scikit-learn    → ``<model_name>.joblib``
        A ``<model_name>_history.json`` sidecar is always written.

        Returns
        -------
        str
            Absolute path of the saved model file.
        """
        import joblib

        save_path = pathlib.Path(save_dir)
        save_path.mkdir(parents=True, exist_ok=True)

        if self.model is None:
            raise RuntimeError("No model to save.  Call train_* first.")

        # --- Save model ------------------------------------------------------
        if self.model_type == "cnn":
            model_file = save_path / f"{self.model_name}.pt"
            torch.save(self.model.state_dict(), model_file)
        else:
            model_file = save_path / f"{self.model_name}.joblib"
            joblib.dump(self.model, model_file)

        # --- Save history sidecar -------------------------------------------
        history_file = save_path / f"{self.model_name}_history.json"
        history_file.write_text(
            json.dumps(self._history, indent=2, default=str),
            encoding="utf-8",
        )

        logger.info("Model saved → %s", model_file)
        return str(model_file)


# ---------------------------------------------------------------------------
# Fallback placeholder (used when ml.models.* packages are absent)
# ---------------------------------------------------------------------------

class _PlaceholderCNN(nn.Module):
    """Minimal CNN placeholder so imports never fail during testing."""

    def __init__(self, num_classes: int):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(64, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.features(x))
