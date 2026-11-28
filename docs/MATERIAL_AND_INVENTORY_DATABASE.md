# E-WASTE AI — Material, Recovery & Warehouse Inventory Database

Covers **Module 7 (Component & Material Management)**, **Module 8 (Material Recovery Management)**, and **Module 9 (Warehouse & Inventory Management)** (`backend/models/erp_recovery_inv.py`).

---

## 1. Strict Separation: Estimated Composition vs. Measured Recovery (M7 & M8)

- **Module 7 (9 tables including reused `components`):** `device_categories`, `device_models`, `component_categories`, `components`, `material_types` (supporting Copper, Aluminium, Iron & Steel, Plastics, Glass, Precious-metal categories, and hazardous streams), `material_composition_sources`, `component_material_mapping`, `hazardous_material_types`, `hazardous_material_records`.
  - `ComponentMaterialMapping` enforces a database check constraint (`CheckConstraint("NOT is_measured_recovery")`) compatible with both PostgreSQL and SQLite so literature/BOM composition estimates can never masquerade as measured physical recovery.
  - `ProcessingAndRecoveryService.map_component_material_estimate()` explicitly persists `verification_status`, `confidence_score`, `source_id`, and `is_measured_recovery=False`.
- **Module 8 (8 tables):** `recovery_jobs`, `recovery_job_inputs`, `recovery_job_outputs`, `recovered_materials`, `material_quality_records`, `material_loss_records`, `recovery_measurements`, `recovery_method_records`.
  - `recovered_materials` keeps **`measured_weight_kg`**, **`predicted_weight_kg`**, and **`estimated_weight_kg`** in distinct columns so physical scale measurements, AI forecasts, and engineering estimates remain auditable side-by-side (`record_recovery_job_and_output()`).

---

## 2. Multi-Warehouse & Transactional Stock Consistency (M9 — 10 Tables)

- Tables: `warehouses`, `warehouse_locations`, `inventory_items` (`ERPInventoryItem`, separate from legacy Phase 4 `inventory`), `inventory_stock`, `inventory_transactions`, `stock_movements`, `stock_adjustments`, `stock_reservations`, `material_transfers`, and `stock_audit_records`.
- **Opening-to-Closing Balance Tracking (`inventory_stock`):** Tracks `opening_stock_kg`, `received_stock_kg`, `issued_stock_kg`, `sold_stock_kg`, `closing_stock_kg`, and `reserved_stock_kg` per warehouse, item, and optional batch (`incoming_batch_id`).
- **Negative-Stock Prevention (`WarehouseInventoryService.apply_stock_transaction`):** Every transaction (`OPENING`, `RECEIVE`, `ISSUE`, `SALE`, `TRANSFER_IN`, `TRANSFER_OUT`, `ADJUST`) computes `new_closing`, raises `ValueError("Insufficient stock...")` and rolls back if `new_closing < 0`, appends an immutable `InventoryTransaction` balance-after entry, and logs `STOCK_<TYPE>` to `audit_logs`.
- **Atomic Inter-Branch Transfers (`transfer_between_branches`):** Combines source-warehouse `TRANSFER_OUT`, destination-warehouse `TRANSFER_IN`, `MaterialTransfer`, and `StockMovement` inside one atomic transaction with full rollback on error.
- **Minimum Stock Alerts:** **Report 5 (`warehouse_stock_report`)** compares `inventory_stock.closing_stock_kg` against `inventory_items.min_stock_kg` and flags `below_min_alert`.
