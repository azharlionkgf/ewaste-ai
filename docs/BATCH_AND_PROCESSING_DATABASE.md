# E-WASTE AI — Incoming Batch, Processing, Logistics & Machine Database

Covers **Module 5 (Incoming E-Waste Registration)**, **Module 6 (Sorting, Dismantling & Processing)**, **Module 11 (Transport & Logistics)**, and **Module 12 (Machine & Production Management)** (`backend/models/erp_batches_ops.py`).

---

## 1. Incoming Batch Registration & Traceability (Module 5 — 8 Tables)

- `incoming_batches`: Core traceability record linking `company_id`, `branch_id`, `warehouse_id`, `supplier_id`, `procurement_order_id`, `responsible_employee_id`, and optional `legacy_batch_id`. Tracks `batch_number`, auto-generated or scanned `barcode_qr_code`, `receiving_date`, `ewaste_category`, `device_type`, `gross_weight_kg`, `tare_weight_kg`, `net_weight_kg`, `inspection_status`, `purchase_value`, and `batch_status`.
- **Integrity Guard (`IncomingBatchService.register_incoming_batch`):** Validates `tare_weight_kg <= gross_weight_kg` before computing `net_weight_kg = round(gross - tare, 4)` and automatically creates the initial row in `batch_status_history`.
- Supporting tables: `incoming_materials`, `batch_items`, `weighbridge_records`, `material_receiving_records`, `incoming_inspections`, `batch_documents`, `batch_status_history`.

---

## 2. Sorting, Dismantling & Processing Operations (Module 6 — 11 Tables)

Tracks operational timestamps, weights, rejects, operators, workstations, and quality checks **strictly as authorized operational logs (without providing hazardous dismantling instructions)**:

- `sorting_operations` & `dismantling_operations`: Operator-linked `input_weight_kg`, `output_weight_kg`, `rejected_quantity_kg`, `start_time`, `end_time`, and process outcome.
- `processing_jobs` & `processing_job_items`: Connects `incoming_batch_id`, `production_line_id`, `machine_id`, and `operator_employee_id` (`ProcessingAndRecoveryService.record_processing_job()`).
- Supporting tables: `workstations`, shared `machines`, `machine_usage_logs`, `machine_maintenance`, `operator_assignments`, `processing_waste_records`, `quality_inspections`.

---

## 3. Transport & Logistics (Module 11 — 8 Tables)

- `transporters`, `vehicles`, `drivers`, `transport_orders` (linking `incoming_batch_id`, `sales_order_id`, supplier pickup, inter-branch transfer, or customer delivery), `transport_trip_records`, `transportation_expenses`, `delivery_records`, and `vehicle_maintenance`.

---

## 4. Machine & Production Management (Module 12 — 8 Additional + Shared `machines`)

- `production_lines`, `machine_categories`, shared `machines` (`rated_capacity_kg_hr`, manufacturer, serial number, status), `machine_capacity`, `machine_operating_logs` (`operating_hours`, `output_kg`), `machine_downtime` (`downtime_hours`), `maintenance_schedules`, `maintenance_records`, and `energy_consumption_records`.
- Feeds **Report 10 (`machine_utilization_report`)**, computing utilization percentage as `operating_hours / (operating_hours + downtime_hours) * 100` directly from live operating & downtime logs.
