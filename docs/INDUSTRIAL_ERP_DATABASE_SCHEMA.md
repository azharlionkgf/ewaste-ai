# E-WASTE AI — Industrial ERP Database Schema Reference

**Database Engine:** SQLite (local development) / PostgreSQL (production via `DATABASE_URL`)  
**ORM Metadata:** `152` tables, `2,298` columns, `439` foreign keys, `700` indexes  
**Common Audit Mixin (`backend/models/erp_mixins.py`):** UUID `id`, `created_at`, `updated_at`, `created_by`, `updated_by`, `is_deleted`, `deleted_at`, plus `company_id` / `branch_id` multi-tenant keys on transactional & branch-owned tables.

---

## Module 1: Company Management (`erp_org_staff.py` — 10 Tables)
- `companies` (15 cols) — Legal entity root (`company_code`, `legal_name`, `trade_name`, `registration_number`, `tax_id`, `base_currency`, `is_active`)
- `company_branches` (13 cols) — Multi-branch / plant entities (`branch_code`, `branch_name`, `branch_type`, `is_head_office`)
- `departments` (13 cols) — Branch-linked organizational departments
- `business_units` (13 cols) — Business unit segmentation per company/branch
- `company_addresses` (17 cols), `company_contacts` (14 cols), `company_documents` (15 cols), `company_licenses` (17 cols), `company_settings` (12 cols), `financial_years` (13 cols)

## Module 2: Employee & Staff Management (`erp_org_staff.py` — 9 Tables)
- `employee_departments` (14 cols), `employee_designations` (11 cols), `employee_roles` (13 cols — `is_admin_role`, `is_financial_restricted`), `employee_shifts` (12 cols)
- `employees` (21 cols, 7 FKs) — Linked optionally to `users.id`, `company_id`, `branch_id`, `department_id`, `designation_id`, `role_id`, `shift_id`, `joining_date`, `authorized_operations`
- `employee_attendance` (15 cols), `employee_training_records` (16 cols), `employee_permissions` (14 cols), `employee_activity_logs` (16 cols)

## Module 3: Supplier & Procurement (`erp_partners.py` — 9 Tables)
- `suppliers` (16 cols), `supplier_contacts` (14 cols), `supplier_documents` (13 cols), `supplier_material_categories` (12 cols)
- `procurement_orders` (22 cols, 4 FKs), `procurement_order_items` (15 cols), `supplier_invoices` (19 cols), `supplier_payments` (16 cols), `purchase_returns` (17 cols)

## Module 4: Customer & Sales Management (`erp_partners.py` — 9 Tables)
- `customers` (15 cols), `customer_contacts` (14 cols), `customer_documents` (13 cols), `quotations` (16 cols)
- `sales_orders` (20 cols, 4 FKs), `sales_order_items` (16 cols), `sales_invoices` (19 cols), `sales_payments` (16 cols), `sales_returns` (17 cols)

## Module 5: Incoming E-Waste Registration (`erp_batches_ops.py` — 8 Tables)
- `incoming_materials` (14 cols), `incoming_batches` (26 cols, 7 FKs, 14 indexes — `batch_number`, `barcode_qr_code`, `gross_weight_kg`, `tare_weight_kg`, `net_weight_kg`, `inspection_status`, `purchase_value`, `batch_status`), `batch_items` (17 cols), `weighbridge_records` (17 cols), `material_receiving_records` (15 cols), `incoming_inspections` (17 cols), `batch_documents` (14 cols), `batch_status_history` (15 cols)

## Module 6: Sorting, Dismantling & Processing (`erp_batches_ops.py` — 10 New + Shared `machines`)
- `workstations` (14 cols), `machines` (19 cols, 5 FKs — shared with Module 12), `sorting_operations` (19 cols), `dismantling_operations` (20 cols), `processing_jobs` (21 cols, 6 FKs), `processing_job_items` (13 cols), `machine_usage_logs` (16 cols), `machine_maintenance` (15 cols), `operator_assignments` (15 cols), `processing_waste_records` (15 cols), `quality_inspections` (17 cols)

## Module 7: Component & Material Management (`erp_recovery_inv.py` + `all_models.py` — 9 Tables)
- `device_categories` (11 cols), `device_models` (12 cols), `component_categories` (11 cols), `components` (reused & extended — 18 cols), `material_types` (13 cols), `material_composition_sources` (13 cols), `component_material_mapping` (16 cols, 5 FKs, enforces `CheckConstraint("NOT is_measured_recovery")`), `hazardous_material_types` (14 cols), `hazardous_material_records` (15 cols)

## Module 8: Material Recovery Management (`erp_recovery_inv.py` — 8 Tables)
- `recovery_jobs` (15 cols), `recovery_job_inputs` (11 cols), `recovery_job_outputs` (14 cols), `recovered_materials` (19 cols, 6 FKs — separate `measured_weight_kg`, `predicted_weight_kg`, `estimated_weight_kg`), `material_quality_records` (16 cols), `material_loss_records` (14 cols), `recovery_measurements` (16 cols), `recovery_method_records` (13 cols)

## Module 9: Warehouse & Inventory Management (`erp_recovery_inv.py` — 10 Tables)
- `warehouses` (14 cols), `warehouse_locations` (13 cols), `inventory_items` (`ERPInventoryItem`, 15 cols), `inventory_stock` (19 cols, 6 FKs — `opening_stock_kg`, `received_stock_kg`, `issued_stock_kg`, `sold_stock_kg`, `closing_stock_kg`, `reserved_stock_kg`), `inventory_transactions` (19 cols, 6 FKs), `stock_movements` (16 cols), `stock_adjustments` (15 cols), `stock_reservations` (15 cols), `material_transfers` (18 cols, 7 FKs), `stock_audit_records` (17 cols)

## Module 10: Finance & Accounting (`erp_finance_env_ai_audit.py` — 13 Tables)
- `financial_periods` (13 cols), `chart_of_accounts` (13 cols), `accounting_vouchers` (17 cols), `journal_entries` (19 cols — `is_balanced`, `is_posted`, `is_audited_statement`), `journal_entry_lines` (13 cols), `expense_categories` (11 cols), `expenses` (19 cols), `income_records` (17 cols), `purchase_payments` (16 cols), `sales_receipts` (16 cols), `tax_records` (16 cols), `bank_transactions` (15 cols), `cash_transactions` (14 cols)

## Module 11: Transport & Logistics (`erp_batches_ops.py` — 8 Tables)
- `transporters` (13 cols), `vehicles` (15 cols), `drivers` (14 cols), `transport_orders` (20 cols, 7 FKs), `transport_trip_records` (16 cols), `transportation_expenses` (14 cols), `delivery_records` (16 cols), `vehicle_maintenance` (14 cols)

## Module 12: Machine & Production Management (`erp_batches_ops.py` — 8 Additional + Shared `machines`)
- `production_lines` (13 cols), `machine_categories` (11 cols), `machine_capacity` (13 cols), `machine_operating_logs` (15 cols), `machine_downtime` (15 cols), `maintenance_schedules` (14 cols), `maintenance_records` (16 cols), `energy_consumption_records` (15 cols)

## Module 13: Environmental & Compliance Records (`erp_finance_env_ai_audit.py` + `all_models.py` — 8 Tables)
- `authorized_recycler_records` (15 cols), `hazardous_waste_movements` (17 cols, 6 FKs), `environmental_measurements` (16 cols), `waste_disposal_records` (15 cols), `compliance_documents` (16 cols), `compliance_observations` (15 cols), `environmental_audit_records` (14 cols), `environmental_reports` (reused & extended — 22 cols)

## Module 14: AI & Automation (`erp_finance_env_ai_audit.py` + `all_models.py` — 8 Tables)
- `ai_models` (14 cols), `ai_model_versions` (13 cols), `ai_predictions` (reused & extended — 23 cols), `ai_prediction_feedback` (16 cols), `recovery_recommendations` (16 cols), `anomaly_records` (16 cols), `forecasting_results` (15 cols), `automation_jobs` (15 cols)

## Module 15: Reports, Documents & Audit (`erp_finance_env_ai_audit.py` + `all_models.py` — 8 Tables)
- `document_registry` (17 cols), `report_templates` (13 cols), `generated_reports` (reused & extended — 16 cols), `audit_logs` (reused & extended — 15 cols), `activity_logs` (16 cols), `notification_records` (15 cols), `approval_workflows` (14 cols), `approval_history` (16 cols)
