# Database Integrity Report — Phase 7
## E-Waste AI Platform
**Date:** 2026-11-28 | **Test Suite:** `tests/test_phase7_db.py` | **Engine:** SQLite (SQLAlchemy 2.0)

---

## 1. Schema Verification

After unifying legacy Phase 2 auxiliary tables (`dataset_versions`, `cleaning_runs`, `preprocessing_configs`) with `backend/models/all_models.py`, `backend.models` registers **20 ORM tables** cleanly under a single `Base.metadata` registry:

1. **Core Phase 4 Canonical Tables (17):**
   `users`, `audit_logs`, `datasets`, `ml_models`, `model_evaluations`, `waste_batches`, `devices`, `components`, `materials`, `inventory`, `recovery_records`, `processing_operations`, `operational_costs`, `ai_predictions`, `environmental_reports`, `generated_reports`, `research_experiments`
2. **Phase 2 Auxiliary Dataset Tracking Tables (3):**
   `dataset_versions`, `cleaning_runs`, `preprocessing_configs`

### Schema Mapping Corrections Verified
- `InventoryItem.__tablename__ == 'inventory'` (not `inventory_items`).
- `WasteBatch`: uses `batch_number` (unique non-null indexed string).
- `RecoveryRecord`: uses `recovered_quantity_g` (grams), `value_source`, `recorded_at`.
- `Device`: uses `manufacturer`, `weight_kg`, `condition`.
- `ResearchExperiment`: uses `experiment_name` (not `name`).
- `MLModel` / `TrainedModel` and `InventoryItem` / `Inventory` aliases preserved cleanly in `all_models.py`.

---

## 2. Critical Integration Fix: Duplicate `Dataset` Registry Conflict

- **Issue discovered:** `backend/models/dataset.py` previously defined its own `class Dataset(Base)` on the same `Base` registry as `backend/models/all_models.py`. Even with `extend_existing=True` on `__table_args__`, importing both modules in the same Python process caused SQLAlchemy mapper configuration to fail with:
  `Multiple classes found for path "Dataset" in the registry of this declarative base.`
- **Resolution:**
  - Updated `backend/models/dataset.py` to re-export `from backend.models.all_models import Dataset` instead of declaring a second `Dataset` class.
  - Aligned `DatasetVersion.dataset_id`, `CleaningRun.dataset_id`, and `PreprocessingConfig.dataset_id` foreign keys to `Column(String, ForeignKey("datasets.id"))` matching `all_models.Dataset.id`.
  - Updated `backend/services/dataset_service.py` to target canonical `Dataset` columns (`dataset_type`, `is_cleaned`, `is_preprocessed`) while preserving dict output compatibility (`file_type`, `status`).
  - Updated `backend/models/__init__.py` to export `CleaningRun`, `DatasetVersion`, `PreprocessingConfig`.
- **Verification:** Local stale `database/ewaste_ai.db` was rebuilt via `init_db()`; `test_init_db_idempotent` confirms repeated `init_db()` calls succeed cleanly.

---

## 3. CRUD, Constraints, Foreign Keys & Rollback Tests (`tests/test_phase7_db.py`)

| Test Group | Coverage | Outcome |
|------------|----------|---------|
| `TestDatabaseSchema` | All models importable, required tables created, column checks, idempotent `init_db()` | ✅ PASS |
| `TestWasteBatchCRUD` | Create, Read, Update (`status`, `total_weight_kg`), Delete on `WasteBatch` | ✅ PASS |
| `TestRecoveryDataSeparation` | `value_source` separates `'estimate'` and `'measured'` values for same batch/material independently | ✅ PASS |
| `TestForeignKeyRelationships` | `Device.batch_id` & `RecoveryRecord.batch_id` FKs, multi-device per batch query count | ✅ PASS |
| `TestResearchExperimentCRUD` | `ResearchExperiment` create & read with `experiment_name` | ✅ PASS |
| `TestConstraintsAndRollback` | Duplicate `batch_number` raises `IntegrityError`; `db.rollback()` reverts uncommitted row while preserving prior commits | ✅ PASS |

---

## 4. Separation of Value Provenance

Checked `RecoveryRecord` and `Material` schemas and verified behavior:
- `RecoveryRecord` records include explicit `value_source` (`estimate`, `measured`, `ai_predicted`), `price_source`, and `price_timestamp`.
- Estimated and measured records can coexist for the same batch and material without overwriting each other.

---

## 5. SQLite Configuration & Limitations

- `backend/database.py` enables `PRAGMA journal_mode=WAL` and `PRAGMA foreign_keys=ON` on SQLite connection open.
- **Backup & Restore:** Automated point-in-time backup/restore endpoints are not implemented in this version; SQLite persistence relies on local `database/ewaste_ai.db` file backup (and ephemeral filesystem initialization via `app.py:_bootstrap_db()` on Streamlit Community Cloud).
