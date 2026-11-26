"""
backend/services/training_service.py
E-WASTE AI — Training Service (DB Integration)
===============================================
Integrates the ML Training Engine with the SQLAlchemy ORM layer.
Persists TrainingRun and ModelEvaluation records to the database.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


class TrainingService:
    """
    Database integration layer for ML training runs and evaluations.

    Usage::

        service = TrainingService(db_session)
        run_id = service.create_run(dataset_id=1, config={"algorithm": "rf"})
        service.update_status(run_id, "running")
        service.save_metrics(run_id, train_m, val_m, test_m)
        runs = service.list_runs()
    """

    def __init__(self, db_session=None):
        """
        db_session: SQLAlchemy Session or None.
        When None, the service operates in memory-only mode (useful for testing
        and environments without a database).
        """
        self.db = db_session
        self._memory_runs: dict[int, dict] = {}
        self._memory_evals: dict[int, dict] = {}
        self._next_run_id = 1
        self._next_eval_id = 1

    # ------------------------------------------------------------------ #
    # TRAINING RUN LIFECYCLE                                               #
    # ------------------------------------------------------------------ #

    def create_run(
        self,
        config: dict,
        dataset_id: int | None = None,
        run_name: str | None = None,
    ) -> int:
        """
        Create a new TrainingRun record and return its ID.

        config keys used (all optional):
            algorithm, task, architecture, random_seed, num_classes,
            class_names (list), hyperparameters (dict), model_path
        """
        if run_name is None:
            run_name = config.get("run_name") or (
                f"{config.get('algorithm', 'model')}_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
            )

        if self.db is not None:
            try:
                from backend.models.ml_model import TrainingRun
                run = TrainingRun(
                    dataset_id=dataset_id,
                    run_name=run_name,
                    model_type=config.get("task", "classification"),
                    architecture=config.get("algorithm", config.get("architecture", "unknown")),
                    hyperparameters=json.dumps(config.get("hyperparameters", {})),
                    random_seed=config.get("random_seed", config.get("seed", 42)),
                    num_classes=config.get("num_classes"),
                    class_names=json.dumps(config.get("class_names", [])),
                    training_history=json.dumps({}),
                    status="pending",
                )
                self.db.add(run)
                self.db.commit()
                self.db.refresh(run)
                logger.info("TrainingRun created: id=%s run_name=%s", run.id, run_name)
                return int(run.id)
            except Exception as exc:
                logger.warning("DB create_run failed (%s) — using memory mode.", exc)
                self.db = None  # fall through to memory

        # Memory mode
        run_id = self._next_run_id
        self._next_run_id += 1
        self._memory_runs[run_id] = {
            "id": run_id,
            "dataset_id": dataset_id,
            "run_name": run_name,
            "algorithm": config.get("algorithm", "unknown"),
            "task": config.get("task", "classification"),
            "hyperparameters": config.get("hyperparameters", {}),
            "seed": config.get("seed", 42),
            "status": "pending",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "model_path": None,
        }
        return run_id

    def update_status(self, run_id: int, status: str, model_path: str | None = None) -> None:
        """Update the status (pending/running/completed/failed) of a training run."""
        if self.db is not None:
            try:
                from backend.models.ml_model import TrainingRun
                run = self.db.query(TrainingRun).filter(TrainingRun.id == run_id).first()
                if run:
                    run.status = status
                    if model_path:
                        run.model_path = model_path
                    self.db.commit()
                    return
            except Exception as exc:
                logger.warning("DB update_status failed (%s).", exc)

        # Memory mode
        if run_id in self._memory_runs:
            self._memory_runs[run_id]["status"] = status
            if model_path:
                self._memory_runs[run_id]["model_path"] = model_path

    def save_metrics(
        self,
        run_id: int,
        train_metrics: dict,
        val_metrics: dict | None = None,
        test_metrics: dict | None = None,
    ) -> None:
        """Save train/val/test evaluation metrics for a training run."""
        if self.db is not None:
            try:
                from backend.models.ml_model import ModelEvaluation
                for split, m in [
                    ("train", train_metrics),
                    ("val", val_metrics or {}),
                    ("test", test_metrics or {}),
                ]:
                    if not m:
                        continue
                    eval_obj = ModelEvaluation(
                        training_run_id=run_id,
                        split=split,
                        accuracy=m.get("accuracy"),
                        precision=m.get("precision"),
                        recall=m.get("recall"),
                        f1_score=m.get("f1_macro"),
                        roc_auc=m.get("roc_auc"),
                        confusion_matrix=json.dumps(m.get("confusion_matrix", [])),
                        mae=m.get("mae"),
                        mse=m.get("mse"),
                        rmse=m.get("rmse"),
                        r2_score=m.get("r2"),
                        additional_metrics=json.dumps(m),
                    )
                    self.db.add(eval_obj)
                self.db.commit()
                return
            except Exception as exc:
                logger.warning("DB save_metrics failed (%s).", exc)

        # Memory mode
        if run_id not in self._memory_evals:
            self._memory_evals[run_id] = {}
        self._memory_evals[run_id]["train"] = train_metrics
        if val_metrics:
            self._memory_evals[run_id]["val"] = val_metrics
        if test_metrics:
            self._memory_evals[run_id]["test"] = test_metrics

    def save_history(self, run_id: int, history: dict) -> None:
        """Save training history (e.g., per-epoch losses) for a run."""
        if self.db is not None:
            try:
                from backend.models.ml_model import TrainingRun
                run = self.db.query(TrainingRun).filter(TrainingRun.id == run_id).first()
                if run:
                    run.training_history = json.dumps(history, default=str)
                    self.db.commit()
                    return
            except Exception as exc:
                logger.warning("DB save_history failed (%s).", exc)

        if run_id in self._memory_runs:
            self._memory_runs[run_id]["training_history"] = history

    # ------------------------------------------------------------------ #
    # QUERIES                                                              #
    # ------------------------------------------------------------------ #

    def get_run(self, run_id: int) -> dict | None:
        """Return a dict representation of the training run, or None."""
        if self.db is not None:
            try:
                from backend.models.ml_model import TrainingRun
                run = self.db.query(TrainingRun).filter(TrainingRun.id == run_id).first()
                if run:
                    return self._run_to_dict(run)
            except Exception as exc:
                logger.warning("DB get_run failed (%s).", exc)

        return self._memory_runs.get(run_id)

    def list_runs(
        self,
        dataset_id: int | None = None,
        status: str | None = None,
        limit: int = 100,
    ) -> list[dict]:
        """Return all training runs, optionally filtered."""
        if self.db is not None:
            try:
                from backend.models.ml_model import TrainingRun
                q = self.db.query(TrainingRun)
                if dataset_id is not None:
                    q = q.filter(TrainingRun.dataset_id == dataset_id)
                if status is not None:
                    q = q.filter(TrainingRun.status == status)
                runs = q.order_by(TrainingRun.id.desc()).limit(limit).all()
                return [self._run_to_dict(r) for r in runs]
            except Exception as exc:
                logger.warning("DB list_runs failed (%s).", exc)

        # Memory mode
        runs = list(self._memory_runs.values())
        if dataset_id is not None:
            runs = [r for r in runs if r.get("dataset_id") == dataset_id]
        if status is not None:
            runs = [r for r in runs if r.get("status") == status]
        return runs[-limit:]

    def get_metrics(self, run_id: int) -> dict:
        """Return all stored metrics for a run, keyed by split."""
        if self.db is not None:
            try:
                from backend.models.ml_model import ModelEvaluation
                evals = (
                    self.db.query(ModelEvaluation)
                    .filter(ModelEvaluation.training_run_id == run_id)
                    .all()
                )
                result = {}
                for e in evals:
                    result[e.split] = {
                        "accuracy": e.accuracy,
                        "precision": e.precision,
                        "recall": e.recall,
                        "f1_macro": e.f1_score,
                        "roc_auc": e.roc_auc,
                        "mae": e.mae,
                        "mse": e.mse,
                        "rmse": e.rmse,
                        "r2": e.r2_score,
                    }
                return result
            except Exception as exc:
                logger.warning("DB get_metrics failed (%s).", exc)

        return self._memory_evals.get(run_id, {})

    # ------------------------------------------------------------------ #
    # HELPERS                                                              #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _run_to_dict(run) -> dict:
        return {
            "id": run.id,
            "dataset_id": getattr(run, "dataset_id", None),
            "run_name": run.run_name,
            "algorithm": run.architecture,
            "task": run.model_type,
            "status": run.status,
            "model_path": run.model_path,
            "seed": run.random_seed,
            "num_classes": run.num_classes,
            "created_at": str(getattr(run, "created_at", "")),
        }
