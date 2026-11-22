"""
Training callbacks for the E-WASTE AI project.
  - EarlyStopping  : halt training when a monitored metric stagnates.
  - ProgressCallback : emit structured progress dicts at the end of each epoch.
"""

import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict

import numpy as np

logger = logging.getLogger(__name__)


class EarlyStopping:
    """
    Monitor a scalar metric and signal when training should stop.

    Parameters
    ----------
    patience : int
        Number of epochs with no improvement before stopping.
    min_delta : float
        Minimum change to qualify as an improvement.
    mode : {'max', 'min'}
        'max' → higher is better (e.g. accuracy).
        'min' → lower is better (e.g. loss).
    """

    def __init__(self, patience: int = 5, min_delta: float = 0.001, mode: str = "max"):
        if mode not in ("max", "min"):
            raise ValueError(f"mode must be 'max' or 'min', got '{mode}'.")
        self.patience   = patience
        self.min_delta  = min_delta
        self.mode       = mode
        self._counter   = 0
        self._best: float = -np.inf if mode == "max" else np.inf
        self._stopped   = False

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def best_value(self) -> float:
        """The best observed metric value so far."""
        return self._best

    # ------------------------------------------------------------------
    # Core logic
    # ------------------------------------------------------------------

    def __call__(self, metric_value: float) -> bool:
        """
        Evaluate the latest metric value.

        Returns
        -------
        bool
            True  → training should stop now.
            False → continue training.
        """
        metric_value = float(metric_value)
        improved = (
            metric_value > self._best + self.min_delta
            if self.mode == "max"
            else metric_value < self._best - self.min_delta
        )

        if improved:
            self._best    = metric_value
            self._counter = 0
            logger.debug("EarlyStopping: improvement → best=%.6f", self._best)
        else:
            self._counter += 1
            logger.debug(
                "EarlyStopping: no improvement (%d / %d)", self._counter, self.patience
            )

        if self._counter >= self.patience:
            self._stopped = True
            logger.info(
                "EarlyStopping triggered after %d epochs without improvement "
                "(best=%.6f).",
                self.patience,
                self._best,
            )
            return True

        return False

    def reset(self) -> None:
        """Reset state so the callback can be reused for a new training run."""
        self._counter = 0
        self._best    = -np.inf if self.mode == "max" else np.inf
        self._stopped = False
        logger.debug("EarlyStopping reset.")


class ProgressCallback:
    """
    Emit structured progress information at the end of each epoch and at
    training completion.

    Parameters
    ----------
    total_epochs : int
        Total number of planned epochs (used to calculate progress %).
    model_name : str
        Human-readable model identifier included in every emitted dict.
    """

    def __init__(self, total_epochs: int, model_name: str):
        self.total_epochs = total_epochs
        self.model_name   = model_name
        self._start_time  = time.monotonic()

    # ------------------------------------------------------------------
    # Epoch-level hook
    # ------------------------------------------------------------------

    def on_epoch_end(self, epoch: int, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Called at the end of each training epoch.

        Parameters
        ----------
        epoch : int
            1-based epoch index.
        metrics : dict
            Arbitrary key/value pairs produced by the trainer
            (e.g. train_loss, val_acc, …).

        Returns
        -------
        dict
            Emit-ready dict suitable for logging, websockets, or stdout.
        """
        progress_pct = round(epoch / max(self.total_epochs, 1) * 100.0, 2)
        elapsed      = time.monotonic() - self._start_time

        payload = {
            "epoch":        epoch,
            "total_epochs": self.total_epochs,
            "progress_pct": progress_pct,
            "metrics":      {k: _safe_scalar(v) for k, v in metrics.items()},
            "model_name":   self.model_name,
            "elapsed_sec":  round(elapsed, 3),
            "timestamp":    datetime.now(tz=timezone.utc).isoformat(),
        }

        logger.info(
            "[%s] Epoch %d/%d (%.1f%%) — %s",
            self.model_name,
            epoch,
            self.total_epochs,
            progress_pct,
            ", ".join(f"{k}={v}" for k, v in payload["metrics"].items()),
        )

        return payload

    # ------------------------------------------------------------------
    # Completion hook
    # ------------------------------------------------------------------

    def on_training_complete(self, history: Dict[str, Any]) -> Dict[str, Any]:
        """
        Called once when training finishes (normally or via early stopping).

        Parameters
        ----------
        history : dict
            The full training history dict returned by the trainer.

        Returns
        -------
        dict
            Summary dict with timing and history snapshot.
        """
        total_elapsed = time.monotonic() - self._start_time
        payload = {
            "event":          "training_complete",
            "model_name":     self.model_name,
            "total_elapsed_sec": round(total_elapsed, 3),
            "timestamp":      datetime.now(tz=timezone.utc).isoformat(),
            "history_summary": {
                "epochs_run":        history.get("epochs_run"),
                "best_val_accuracy": history.get("best_val_accuracy"),
                "training_complete": history.get("training_complete", True),
            },
        }

        logger.info(
            "[%s] Training complete in %.1f s — best_val_acc=%.4f",
            self.model_name,
            total_elapsed,
            history.get("best_val_accuracy", float("nan")),
        )

        return payload


# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------

def _safe_scalar(value: Any) -> Any:
    """Convert numpy scalars / arrays to plain Python types for JSON safety."""
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    return value
