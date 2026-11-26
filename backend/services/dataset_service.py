"""
Dataset Service — Phase 2: Dataset Intelligence Engine
Database service layer for dataset operations.
Aligns with actual ORM models in backend/models/dataset.py.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models.dataset import Dataset, DatasetVersion, CleaningRun, PreprocessingConfig

logger = logging.getLogger(__name__)


class DatasetService:
    """
    Service layer for all dataset-related database operations.

    Usage::

        svc = DatasetService()
        dataset_id = svc.register_dataset("my_csv", "/path/to/file.csv", "csv")
    """

    def __init__(self, db: Session | None = None):
        self._external_db = db

    # ------------------------------------------------------------------ #
    # Dataset registration                                                 #
    # ------------------------------------------------------------------ #

    def register_dataset(
        self,
        name: str,
        file_path: str,
        file_type: str,
        description: str = "",
        source: str = "upload",
        metadata: dict | None = None,
    ) -> int:
        """Register a dataset. Returns the dataset id."""
        with self._session() as db:
            existing = db.query(Dataset).filter(Dataset.name == name).first()
            if existing:
                logger.info("Dataset '%s' already registered (id=%d)", name, existing.id)
                return existing.id

            ds = Dataset(
                name=name,
                file_path=str(file_path),
                file_type=file_type.lower(),
                description=description,
                source=source,
                status="uploaded",
                tags=json.dumps(metadata or {}),
            )
            db.add(ds)
            db.commit()
            db.refresh(ds)
            logger.info("Dataset '%s' registered with id=%d", name, ds.id)
            return ds.id

    # ------------------------------------------------------------------ #
    # Cleaning runs                                                        #
    # ------------------------------------------------------------------ #

    def save_cleaning_run(self, dataset_id: int, report_dict: dict) -> int:
        """Persist cleaning run results. Returns CleaningRun id."""
        with self._session() as db:
            run = CleaningRun(
                dataset_id=dataset_id,
                rows_before=report_dict.get("rows_before", 0),
                rows_after=report_dict.get("rows_after", 0),
                duplicates_found=report_dict.get("duplicates_removed", 0),
                duplicates_removed=report_dict.get("duplicates_removed", 0),
                outliers_flagged=report_dict.get("outliers_flagged", 0),
                cleaning_config=json.dumps(report_dict.get("config_used", {})),
                cleaning_report=json.dumps(report_dict.get("operations_log", [])),
                status="completed",
            )
            db.add(run)
            ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
            if ds:
                ds.status = "cleaned"
            db.commit()
            db.refresh(run)
            logger.info("Cleaning run saved (id=%d) for dataset_id=%d", run.id, dataset_id)
            return run.id

    # ------------------------------------------------------------------ #
    # Preprocessing config                                                 #
    # ------------------------------------------------------------------ #

    def save_preprocessing_config(self, dataset_id: int, config_dict: dict) -> int:
        """Persist a preprocessing configuration. Returns PreprocessingConfig id."""
        with self._session() as db:
            pc = PreprocessingConfig(
                dataset_id=dataset_id,
                config_name=config_dict.get("config_name", "auto"),
                scaler_type=config_dict.get("scaler", "standard"),
                encoder_type=config_dict.get("encoder", "onehot"),
                target_column=config_dict.get("target_col", ""),
                feature_columns=json.dumps(config_dict.get("feature_cols", [])),
                train_ratio=config_dict.get("train_ratio", 0.70),
                val_ratio=config_dict.get("val_ratio", 0.15),
                test_ratio=config_dict.get("test_ratio", 0.15),
            )
            db.add(pc)
            ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
            if ds:
                ds.status = "preprocessed"
            db.commit()
            db.refresh(pc)
            logger.info("Preprocessing config saved (id=%d) for dataset_id=%d", pc.id, dataset_id)
            return pc.id

    # ------------------------------------------------------------------ #
    # Queries                                                              #
    # ------------------------------------------------------------------ #

    def get_dataset_history(self, dataset_id: int) -> dict:
        """Return full history for a dataset."""
        with self._session() as db:
            ds = db.query(Dataset).filter(Dataset.id == dataset_id).first()
            if not ds:
                return {"error": f"Dataset id={dataset_id} not found"}

            cleaning_runs = (
                db.query(CleaningRun)
                .filter(CleaningRun.dataset_id == dataset_id)
                .order_by(CleaningRun.created_at)
                .all()
            )
            prep_configs = (
                db.query(PreprocessingConfig)
                .filter(PreprocessingConfig.dataset_id == dataset_id)
                .order_by(PreprocessingConfig.created_at)
                .all()
            )

            return {
                "dataset": {
                    "id": ds.id,
                    "name": ds.name,
                    "file_path": ds.file_path,
                    "file_type": ds.file_type,
                    "description": ds.description,
                    "source": ds.source,
                    "status": ds.status,
                    "created_at": str(ds.created_at),
                },
                "cleaning_runs": [
                    {
                        "id": r.id,
                        "rows_before": r.rows_before,
                        "rows_after": r.rows_after,
                        "duplicates_removed": r.duplicates_removed,
                        "outliers_flagged": r.outliers_flagged,
                        "status": r.status,
                        "created_at": str(r.created_at),
                    }
                    for r in cleaning_runs
                ],
                "preprocessing_configs": [
                    {
                        "id": p.id,
                        "scaler_type": p.scaler_type,
                        "encoder_type": p.encoder_type,
                        "target_column": p.target_column,
                        "created_at": str(p.created_at),
                    }
                    for p in prep_configs
                ],
            }

    def list_all_datasets(self) -> list[dict]:
        """Return all registered datasets."""
        with self._session() as db:
            datasets = db.query(Dataset).order_by(Dataset.created_at.desc()).all()
            return [
                {
                    "id": ds.id,
                    "name": ds.name,
                    "file_type": ds.file_type,
                    "status": ds.status,
                    "description": ds.description,
                    "created_at": str(ds.created_at),
                }
                for ds in datasets
            ]

    # ------------------------------------------------------------------ #
    # Session helper                                                       #
    # ------------------------------------------------------------------ #

    class _SessionCtx:
        def __init__(self, db: Session, owned: bool):
            self.db = db
            self.owned = owned

        def __enter__(self) -> Session:
            return self.db

        def __exit__(self, *_):
            if self.owned:
                self.db.close()

    def _session(self) -> "_SessionCtx":
        if self._external_db is not None:
            return self._SessionCtx(self._external_db, owned=False)
        return self._SessionCtx(SessionLocal(), owned=True)
