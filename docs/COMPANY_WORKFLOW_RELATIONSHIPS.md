# E-WASTE AI — Company Workflow Relationships & Traceability

This document maps the implemented foreign-key chains linking organization, procurement, batches, operations, recovery, warehouse stock, sales, finance, environmental records, AI predictions, and audits across the 152 registered ORM tables (`439` FKs total).

---

## 1. End-to-End Entity Relationship Chains

### Organizational & RBAC Chain
`companies` → `company_branches` → `departments` → `employees`
- `employees` also connects to `employee_departments`, `employee_designations`, `employee_roles`, `employee_shifts`, optional `users.id`, and per-employee/role `employee_permissions`.
- Every branch-scoped business record carries `company_id` + `branch_id` so multi-company and cross-branch boundaries can be verified in queries and API dependencies.

### Inbound Procurement & Receiving Chain
`suppliers` → `procurement_orders` (`procurement_order_items`) → `incoming_batches`
- `incoming_batches` (`batch_number`, `barcode_qr_code`, `receiving_date`, `gross_weight_kg`, `tare_weight_kg`, `net_weight_kg`, `purchase_value`, `batch_status`) references:
  - `companies.id`, `company_branches.id`, `warehouses.id`
  - `suppliers.id`, `procurement_orders.id`, `employees.id` (`responsible_employee_id`)
  - Optional `waste_batches.id` (`legacy_batch_id`)
- Supported by `weighbridge_records`, `material_receiving_records`, `incoming_inspections`, `batch_items`, `batch_documents`, and `batch_status_history`.
- `IncomingBatchService.transition_batch_status()` appends immutable status transitions into `batch_status_history` and writes unified `audit_logs`.

### Shop-Floor Operations & Recovery Chain
`incoming_batches` → `sorting_operations` → `dismantling_operations` → `processing_jobs` → `recovery_jobs` → `recovered_materials`
- Operational jobs link to `machines.id`, `production_lines.id`, `employees.id` (`operator_employee_id`), `quality_inspections`, and `processing_waste_records`.
- `RecoveryJob` produces `RecoveryJobOutput`, `RecoveryMeasurement`, and `RecoveredMaterial` rows tagged to `material_types.id` while retaining strict separation between `measured_weight_kg`, `predicted_weight_kg`, and `estimated_weight_kg`.

### Warehouse, Stock Movement & Sales Chain
`recovered_materials` / `incoming_batches` → `warehouses` → `inventory_stock` (`inventory_transactions`, `stock_movements`, `material_transfers`) → `sales_orders` → `sales_invoices` → `sales_payments`
- `WarehouseInventoryService.apply_stock_transaction()` updates `opening_stock_kg`, `received_stock_kg`, `issued_stock_kg`, `sold_stock_kg`, and `closing_stock_kg` atomically alongside ledger rows in `inventory_transactions`.
- Inter-branch transfers via `transfer_between_branches()` pair `TRANSFER_OUT` and `TRANSFER_IN` in a single database transaction with `MaterialTransfer` + `StockMovement` records.

### Compliance, AI Verification & Audit Loop
- `ai_predictions` links via `incoming_batch_id` and `ai_model_version_id` to `incoming_batches` and `ai_model_versions`, with human verification stored in `ai_prediction_feedback` (`ComplianceAIService.verify_ai_prediction()`).
- `hazardous_material_records` → `hazardous_waste_movements` → `authorized_recycler_records` (+ optional `transport_orders.id`) tracks hazardous custody without auto-claiming statutory certification.
- Every service mutation records audit metadata via `record_erp_audit()` into both `audit_logs` and `employee_activity_logs`.
