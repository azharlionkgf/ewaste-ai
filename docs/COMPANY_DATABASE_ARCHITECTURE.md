# E-WASTE AI — Company Industrial ERP Database Architecture

**Scope:** Modules 1–15 Production-Oriented Industrial E-Waste Recycling ERP Database  
**Total Registered Tables:** **152** (`136` ERP module tables + `15` Phase 1–6 Core/ML tables + `schema_migrations`)  
**Schema Footprint:** `2,298` columns | `439` foreign keys | `700` indexes  

---

## 1. Architectural Strategy & Existing System Reuse

Rather than creating a separate shadow database, the Industrial ERP schema expands E-Waste AI's existing central SQLAlchemy ORM (`backend/database.py`, `backend/models/`) and preserves all existing tables and rows:

- **Reused & Safely Extended (5 tables):**
  - `components` (Module 7 — extended with nullable `company_id`, `branch_id`, `component_category_id`, `device_model_id`, `is_deleted`, `updated_at`)
  - `environmental_reports` (Module 13 — extended with `company_id`, `branch_id`, `compliance_category`, `jurisdiction_ref`, `supporting_document_id`, `is_deleted`, `updated_at`)
  - `ai_predictions` (Module 14 — extended with `company_id`, `branch_id`, `incoming_batch_id`, `ai_model_version_id`, `review_status`, `human_verified`, `verified_by`, `verified_at`, `final_measured_outcome`)
  - `generated_reports` (Module 15 — extended with `company_id`, `branch_id`, `template_id`, `is_deleted`)
  - `audit_logs` (Module 15 — extended with `company_id`, `branch_id`, `employee_id`, `module`, `before_state`, `after_state`, `status`)
- **Coexistence Choices (Zero Breaking Changes):**
  - `inventory_items` (`ERPInventoryItem`) serves ERP Module 9 while preserving Phase 4–7 `inventory` (`InventoryItem`).
  - `ai_models` (`AIModelRegistry`) serves ERP Module 14 while preserving Phase 4–7 `ml_models` (`MLModel`).
  - `machines` is shared as a single canonical table across Module 6 (Sorting/Processing) and Module 12 (Machine & Production).
  - `incoming_batches` links optionally via `legacy_batch_id` to Phase 4 `waste_batches`.

---

## 2. Dual-Dialect Database Engine & Migration Architecture

### Engine (`backend/database.py`)
- Uses `is_sqlite_url()` and `build_engine()` to separate local SQLite execution (`check_same_thread=False`, `PRAGMA` hooks) from PostgreSQL (`DATABASE_URL` via `psycopg2 2.9.12` driver with connection pooling and `pool_pre_ping=True`, without SQLite-only `connect_args`).
- Hot backups & recovery via `backup_database()` (SQLite online `backup()` API + logical JSON snapshot under `database/backups/`, git-ignored) and `restore_sqlite_backup()`.

### Safe Migration Engine (`backend/migrations/runner.py` & `alembic/`)
- Idempotent SQLAlchemy migration runner tracked in `schema_migrations`:
  - `0001_phase4_6_baseline`: Registers Phase 1–6 baseline tables.
  - `0002_erp_non_breaking_extensions`: Safely executes `ALTER TABLE ... ADD COLUMN` across the 5 reused tables (`33` columns in `_EXTENDED_COLUMNS`) with dialect-aware `BOOLEAN`/`TIMESTAMP` vs `DATETIME` mapping and zero row deletion.
  - `0003_industrial_erp_15_modules`: Creates all remaining 15-module ERP tables (`checkfirst=True`).
  - `0004_erp_composite_indexes`: Adds `ix_audit_company_branch`, `ix_pred_company_batch`, and `ix_env_rep_company_branch`.
- Alembic templates exist in `alembic.ini`, `alembic/env.py`, `alembic/versions/0001_baseline.py`, and `alembic/versions/0002_industrial_erp.py` for PostgreSQL deployments where the `alembic` CLI package is installed. *(Local Python 3.13 test environment validates SQLite migrations live and PostgreSQL dialect config/URL detection; `alembic` CLI and a live PostgreSQL server instance were not executed locally.)*

---

## 3. Layered Software Architecture

| Layer | Files | Responsibility |
|-------|-------|----------------|
| Mixins & Core Models | `backend/models/erp_mixins.py`, `all_models.py`, `dataset.py`, `ml_model.py` | UUID PKs, soft-delete flags, `created_by`/`updated_by`, `company_id`/`branch_id` mixins |
| ERP ORM Modules | `erp_org_staff.py`, `erp_partners.py`, `erp_batches_ops.py`, `erp_recovery_inv.py`, `erp_finance_env_ai_audit.py` | 136 normalized tables across M1–M15 |
| Security & Audit | `backend/services/erp_security.py` | JWT decode, `EmployeeRole`/`EmployeePermission` resolution, company/branch isolation, unified `AuditLog` + `EmployeeActivityLog` writes |
| Domain Services | `erp_core_service.py`, `erp_operations_service.py`, `erp_reports_service.py`, `erp_admin_service.py` | Transactional workflows, negative-stock & unbalanced-journal guards, 15 DB reports, DB inspection/backup |
| REST API & Schemas | `backend/schemas/erp_schemas.py`, `backend/routers/erp_routers.py` | 30 `/api/v1/erp/*` endpoints with RBAC & Pydantic v2 validation |
| Frontend ERP UI | `frontend/pages/erp_admin.py` | 6-tab Company ERP & DB Administration workspace (`Company ERP & Admin`) |

### Honest Implementation Scope Disclosure
- All **136** requested ERP tables, foreign keys, indexes, and safe migrations are implemented and tested in ORM/DDL.
- REST endpoints (`30` routes under `/api/v1/erp`) cover core company/branch/staff, supplier/PO, customer/SO, incoming batch, processing, material recovery, warehouse stock/transfer, finance COA/journal entry, machines, compliance docs, AI feedback, all 15 DB reports, and admin overview/backup. Auxiliary sub-tables (`company_contacts`, `supplier_contacts`, `customer_documents`, `quotations`, `purchase_returns`, `sales_returns`, `employee_attendance`, `employee_training_records`, `bank_transactions`, `cash_transactions`, `tax_records`, `vehicle_maintenance`, `automation_jobs`, `forecasting_results`, `approval_workflows`) are present in ORM/services and await dedicated per-table REST endpoints if needed individually.
