# E-WASTE AI — Company Database Security, RBAC & Backup Controls

Enforced across `backend/services/erp_security.py`, `backend/routers/erp_routers.py`, and `backend/database.py`.

---

## 1. Authentication & Role-Based Permission Model

Every `/api/v1/erp/*` route validates an HS256 JWT token via `get_erp_context()`, linking the authenticated `User` to any active `Employee` row, its `EmployeeRole`, and granular `EmployeePermission` grants/denials.

| Base Role | Default Permissions Summary | Financial Access | Admin Overview/Backup |
|-----------|-----------------------------|------------------|-----------------------|
| `admin` | Full M1–M15 permissions + `admin:access` | Authorized (`finance:read/write`) | Authorized |
| `finance_manager` | `company:read`, `procurement`, `sales`, `warehouse:read`, `finance:read/write`, `reports:read` | Authorized | Denied (`403`) |
| `manager` | Company, HR read, Ops, Procurement, Sales, Warehouse, Logistics, Machines, Compliance, AI, Reports | Restricted unless granted via role | Denied (`403`) |
| `operator` | Batch, processing, recovery, warehouse/machine/logistics/compliance/AI read/ops, operational reports | Denied (`403`) | Denied (`403`) |
| `researcher` | Company/batch/recovery/compliance read, `ai:read/write`, non-financial `reports:read` | Denied (`403`) | Denied (`403`) |

---

## 2. Multi-Company & Branch Isolation

- `enforce_company_branch_scope(ctx, target_company_id, target_branch_id)`:
  - Platform super-admins (`ctx.is_admin and ctx.company_id is None`) may administer across companies.
  - Company-bound users receive `HTTP 403 ("Cross-company data access is prohibited")` on any request targeting another `company_id`.
  - Employees with `branch_restricted=True` receive `HTTP 403 ("Cross-branch data access restricted for your role")` when targeting another `branch_id`.
- Verified in `tests/test_company_erp_database.py::test_rbac_financial_admin_and_cross_company_isolation`: unauthenticated calls return `401`, cross-company queries and restricted financial/admin endpoints return `403` for operators while succeeding (`200`) for authorized roles.

---

## 3. Unified Audit Trail & Safe Backups

- `record_erp_audit()` writes transactional records into both `audit_logs` (including `company_id`, `branch_id`, `employee_id`, `module`, `before_state`, `after_state`, `status`) and `employee_activity_logs` when `employee_id` and `company_id` are present.
- `backup_database()` (`POST /api/v1/erp/admin/backup` and `ERPAdminService.create_backup()`) writes timestamped snapshots to `database/backups/` (git-ignored) using SQLite's online `backup()` API or dialect-neutral logical JSON export.
- `restore_sqlite_backup()` verifies and restores SQLite snapshots cleanly.
