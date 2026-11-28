# E-WASTE AI — Procurement, Supplier & Sales Database

Covers **Module 3 (Supplier & E-Waste Procurement)** and **Module 4 (Customer & Sales Management)**.

---

## 1. Supplier & Procurement Model (`backend/models/erp_partners.py`)

| Table | Purpose | Key Tracked Fields |
|-------|---------|-------------------|
| `suppliers` | Approved e-waste suppliers | `supplier_code`, `name`, `supplier_type`, `registration_number`, `tax_id`, `rating`, `is_active`, `company_id`, `branch_id` |
| `supplier_contacts` | Commercial & logistics contacts | Name, designation, email, phone, primary contact flag |
| `supplier_documents` | KYC, registration & vendor agreements | Document type, reference number, file URL/path, expiry |
| `supplier_material_categories` | E-waste streams supplied per vendor | Material category mapping, active flag |
| `procurement_orders` | Purchase orders per branch | `po_number`, `order_date`, `expected_delivery_date`, `ewaste_category`, `total_quantity`, `total_weight_kg`, `purchase_price_total`, `transportation_cost`, `currency`, `status`, `approved_by_employee_id` |
| `procurement_order_items` | Line-level PO quantities & pricing | `ewaste_category`, `quantity`, `weight_kg`, `unit_price`, line total |
| `supplier_invoices` | Vendor billing documents | Invoice number, billing dates, tax/total amount, `payment_status` |
| `supplier_payments` | Vendor disbursements | Payment reference, date, method, amount |
| `purchase_returns` | Rejected/returned incoming supplies | Return reason, weight/quantity, settlement status |

### Service Logic (`ProcurementService` in `backend/services/erp_core_service.py`)
- `create_procurement_order()` aggregates line item quantity (`total_quantity`), weight (`total_weight_kg`), and purchase totals (`purchase_price_total`), stores `transportation_cost` and `branch_id`, flushes item lines, and logs `CREATE` in `audit_logs`.
- `create_supplier()`, `list_suppliers()`, and `create_supplier_invoice_and_payment()` support supplier history and invoice payment reconciliation.

---

## 2. Customer & Sales Model (`backend/models/erp_partners.py`)

| Table | Purpose | Key Tracked Fields |
|-------|---------|-------------------|
| `customers` | Refineries & industrial off-takers | `customer_code`, `name`, `customer_type`, `registration_number`, `tax_id`, `is_active`, `company_id`, `branch_id` |
| `customer_contacts` | Commercial contacts | Contact details linked to `customers.id` |
| `customer_documents` | Customer agreements & compliance docs | Document reference & storage URI |
| `quotations` | Pre-order recovered material quotes | Quoted material weights, unit pricing, validity |
| `sales_orders` | Confirmed recovered material orders | `so_number`, `order_date`, `subtotal_amount`, `tax_amount`, `total_amount`, `currency`, `delivery_status`, `payment_status` |
| `sales_order_items` | Material line items | `recovered_material_name`, optional `inventory_item_id`, `quantity_kg`, `unit_price`, `tax_rate_pct`, `line_total` |
| `sales_invoices` | Customer billing invoices | Invoice number, issue/due date, totals, `payment_status` |
| `sales_payments` | Customer payment collections | Receipt/payment ref, date, amount, mode |
| `sales_returns` | Customer material returns | Return quantity, reason, credit note link |

### Service Logic (`SalesService`)
- `create_sales_order()` calculates `subtotal_amount`, `tax_amount`, and `total_amount` from order line items (`line_total = quantity_kg * unit_price * (1 + tax_rate_pct / 100)`) and logs an audit entry.
- Tested end-to-end in `tests/test_company_erp_database.py::test_full_batch_to_recovery_to_stock_and_sales_traceability`, verifying PO totals (`240.0` on `100.0 kg`) and SO totals with `10%` tax (`104.5`).
