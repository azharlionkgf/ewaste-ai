"""
E-Waste AI — Comprehensive Industrial ERP Database Test Suite
=============================================================
Tests:
1. All 136 requested ERP tables across Modules 1–15 + safe zero-data-loss migration
2. Dual SQLite/PostgreSQL database configuration validation
3. Foreign keys, constraints & Company -> Branch -> Dept -> Employee hierarchy
4. End-to-end batch traceability (Supplier -> PO -> Batch -> Sort -> Process -> Recovery)
5. Transactional warehouse stock consistency & branch transfers (blocking negative stock)
6. Double-entry financial ledger balancing (debit == credit) & non-audited flag
7. FastAPI RBAC, financial restriction, admin restriction & cross-company isolation
8. All 15 company ERP database reports (real records only)
9. Database backup & restoration integrity in a safe temp directory
10. Frontend Company ERP & Admin navigation & rendering availability
"""

from __future__ import annotations

import os
import sys
import tempfile
from datetime import date, datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def _isolated_erp_db():
    from backend.database import Base
    import backend.models  # noqa: registers all Core + ERP tables

    eng = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=eng)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=eng)
    return eng, Session()


class TestERPSchemaAndMigrations:
    """Verify all 15 ERP modules, constraints, and zero-data-loss migration."""

    REQUIRED_ERP_TABLES = [
        # M1
        "companies", "company_branches", "departments", "business_units",
        "company_addresses", "company_contacts", "company_documents",
        "company_licenses", "company_settings", "financial_years",
        # M2
        "employees", "employee_departments", "employee_designations", "employee_roles",
        "employee_attendance", "employee_shifts", "employee_training_records",
        "employee_permissions", "employee_activity_logs",
        # M3
        "suppliers", "supplier_contacts", "supplier_documents", "supplier_material_categories",
        "procurement_orders", "procurement_order_items", "supplier_invoices",
        "supplier_payments", "purchase_returns",
        # M4
        "customers", "customer_contacts", "customer_documents", "sales_orders",
        "sales_order_items", "sales_invoices", "sales_payments", "sales_returns", "quotations",
        # M5
        "incoming_materials", "incoming_batches", "batch_items", "weighbridge_records",
        "material_receiving_records", "incoming_inspections", "batch_documents", "batch_status_history",
        # M6
        "sorting_operations", "dismantling_operations", "processing_jobs", "processing_job_items",
        "workstations", "machines", "machine_usage_logs", "machine_maintenance",
        "operator_assignments", "processing_waste_records", "quality_inspections",
        # M7
        "device_categories", "device_models", "components", "component_categories",
        "material_types", "component_material_mapping", "material_composition_sources",
        "hazardous_material_types", "hazardous_material_records",
        # M8
        "recovery_jobs", "recovery_job_inputs", "recovery_job_outputs", "recovered_materials",
        "material_quality_records", "material_loss_records", "recovery_measurements", "recovery_method_records",
        # M9
        "warehouses", "warehouse_locations", "inventory_items", "inventory_stock",
        "inventory_transactions", "stock_movements", "stock_adjustments", "stock_reservations",
        "material_transfers", "stock_audit_records",
        # M10
        "chart_of_accounts", "accounting_vouchers", "journal_entries", "journal_entry_lines",
        "expense_categories", "expenses", "income_records", "purchase_payments",
        "sales_receipts", "tax_records", "bank_transactions", "cash_transactions", "financial_periods",
        # M11
        "transporters", "vehicles", "drivers", "transport_orders",
        "transport_trip_records", "transportation_expenses", "delivery_records", "vehicle_maintenance",
        # M12
        "production_lines", "machine_categories", "machine_capacity", "machine_operating_logs",
        "machine_downtime", "maintenance_schedules", "maintenance_records", "energy_consumption_records",
        # M13
        "hazardous_waste_movements", "environmental_measurements", "waste_disposal_records",
        "authorized_recycler_records", "compliance_documents", "compliance_observations",
        "environmental_audit_records", "environmental_reports",
        # M14
        "ai_models", "ai_model_versions", "ai_predictions", "ai_prediction_feedback",
        "recovery_recommendations", "anomaly_records", "forecasting_results", "automation_jobs",
        # M15
        "document_registry", "generated_reports", "report_templates", "audit_logs",
        "activity_logs", "notification_records", "approval_workflows", "approval_history",
    ]

    def test_all_136_erp_tables_present(self):
        eng, db = _isolated_erp_db()
        try:
            tables = set(inspect(eng).get_table_names())
            missing = [t for t in self.REQUIRED_ERP_TABLES if t not in tables]
            assert missing == [], f"Missing ERP tables: {missing}"
            assert len(self.REQUIRED_ERP_TABLES) == 136
        finally:
            db.close()
            eng.dispose()

    def test_safe_migration_preserves_existing_records(self, tmp_path):
        import sqlite3
        from backend.database import build_engine
        from backend.migrations.runner import apply_migrations, get_migration_status

        db_file = tmp_path / "legacy_preserve.db"
        # Simulate pre-ERP legacy SQLite database with existing rows
        with sqlite3.connect(str(db_file)) as conn:
            conn.execute(
                "CREATE TABLE users (id TEXT PRIMARY KEY, username TEXT UNIQUE, email TEXT UNIQUE, hashed_password TEXT, full_name TEXT, role TEXT, is_active INTEGER, created_at TEXT, last_login TEXT)"
            )
            conn.execute(
                "CREATE TABLE waste_batches (id TEXT PRIMARY KEY, batch_number TEXT UNIQUE, source TEXT, total_weight_kg REAL)"
            )
            conn.execute(
                "INSERT INTO users VALUES ('u1', 'legacy_user', 'legacy@test.io', 'hash', 'Legacy', 'operator', 1, '2026-11-20', NULL)"
            )
            conn.execute("INSERT INTO waste_batches VALUES ('wb1', 'LEGACY-001', 'City', 45.0)")
            conn.commit()

        eng = build_engine(f"sqlite:///{db_file}")
        try:
            res = apply_migrations(target_engine=eng, pre_backup=False)
            assert res["total_tables"] >= 150
            assert "0003_industrial_erp_15_modules" in res["executed_revisions"]
            status_info = get_migration_status(target_engine=eng)
            assert status_info["is_up_to_date"] is True

            # Verify zero data loss
            with sqlite3.connect(str(db_file)) as conn:
                u_cnt = conn.execute("SELECT COUNT(*) FROM users WHERE username='legacy_user'").fetchone()[0]
                wb_cnt = conn.execute("SELECT COUNT(*) FROM waste_batches WHERE batch_number='LEGACY-001'").fetchone()[0]
                assert u_cnt == 1
                assert wb_cnt == 1
        finally:
            eng.dispose()

    def test_postgresql_dialect_config_without_sqlite_args(self):
        from backend.database import is_sqlite_url
        assert is_sqlite_url("sqlite:///./database/ewaste_ai.db") is True
        assert is_sqlite_url("postgresql://user:pass@localhost:5432/ewaste_erp") is False


class TestERPWorkflowsTraceabilityAndConsistency:
    """Test real recycling workflows, FK integrity, inventory transactions & finance balancing."""

    def setup_method(self):
        self.eng, self.db = _isolated_erp_db()

    def teardown_method(self):
        self.db.close()
        self.eng.dispose()

    def _seed_org_hierarchy(self):
        from backend.services.erp_core_service import CompanyService, EmployeeService

        c_svc = CompanyService()
        e_svc = EmployeeService()
        comp = c_svc.create_company(self.db, {"company_code": "GCY-01", "legal_name": "GreenCycle Industrial Pvt Ltd"})
        b1 = c_svc.create_branch(self.db, {"company_id": comp.id, "branch_code": "BR-NORTH", "branch_name": "North Plant"})
        b2 = c_svc.create_branch(self.db, {"company_id": comp.id, "branch_code": "BR-SOUTH", "branch_name": "South Hub"})
        dept = c_svc.create_department(self.db, {"company_id": comp.id, "branch_id": b1.id, "dept_code": "OPS", "dept_name": "Operations"})
        emp = e_svc.create_employee(
            self.db,
            {
                "company_id": comp.id, "branch_id": b1.id, "department_id": dept.id,
                "employee_code": "EMP-101", "full_name": "Ravi Operator", "joining_date": date(2025, 1, 15),
            },
        )
        return comp, b1, b2, dept, emp

    def test_full_batch_to_recovery_to_stock_and_sales_traceability(self):
        from backend.models.erp_batches_ops import SortingOperation
        from backend.models.erp_recovery_inv import ERPInventoryItem, MaterialLossRecord, MaterialType, Warehouse
        from backend.services.erp_core_service import ProcurementService, SalesService
        from backend.services.erp_operations_service import (
            IncomingBatchService,
            ProcessingAndRecoveryService,
            WarehouseInventoryService,
        )
        from backend.services.erp_reports_service import ERPReportsService

        comp, b1, _b2, _dept, emp = self._seed_org_hierarchy()
        proc_svc = ProcurementService()
        sales_svc = SalesService()
        batch_svc = IncomingBatchService()
        ops_svc = ProcessingAndRecoveryService()
        wh_svc = WarehouseInventoryService()

        sup = proc_svc.create_supplier(self.db, {"company_id": comp.id, "branch_id": b1.id, "supplier_code": "SUP-1", "name": "Metro Corp"})
        po = proc_svc.create_procurement_order(
            self.db,
            {"company_id": comp.id, "branch_id": b1.id, "supplier_id": sup.id, "po_number": "PO-1001", "order_date": date(2026, 11, 20), "ewaste_category": "it_equipment", "transportation_cost": 50.0},
            items=[{"ewaste_category": "it_equipment", "quantity": 20, "weight_kg": 100.0, "unit_price": 12.0}],
        )
        assert po.total_weight_kg == 100.0
        assert po.purchase_price_total == 240.0

        wh = Warehouse(company_id=comp.id, branch_id=b1.id, warehouse_code="WH-N1", warehouse_name="North Store")
        mat = MaterialType(company_id=comp.id, material_code="CU", material_name="Copper", material_group="copper")
        self.db.add_all([wh, mat])
        self.db.commit()

        # Tare > gross must fail
        with pytest.raises(ValueError, match="Tare weight"):
            batch_svc.register_incoming_batch(self.db, {
                "company_id": comp.id, "branch_id": b1.id, "batch_number": "BAD-01",
                "receiving_date": date(2026, 11, 20), "ewaste_category": "it_equipment",
                "gross_weight_kg": 10.0, "tare_weight_kg": 12.0,
            })

        batch = batch_svc.register_incoming_batch(self.db, {
            "company_id": comp.id, "branch_id": b1.id, "warehouse_id": wh.id,
            "supplier_id": sup.id, "procurement_order_id": po.id, "responsible_employee_id": emp.id,
            "batch_number": "INB-2026-01", "receiving_date": date(2026, 11, 20),
            "ewaste_category": "it_equipment", "gross_weight_kg": 110.0, "tare_weight_kg": 10.0, "purchase_value": 240.0,
        })
        assert batch.net_weight_kg == 100.0
        assert len(batch.status_history) == 1

        batch_svc.transition_batch_status(self.db, batch.id, "processing", employee_id=emp.id, reason="Sorting completed")
        self.db.add(SortingOperation(
            company_id=comp.id, branch_id=b1.id, incoming_batch_id=batch.id,
            operator_employee_id=emp.id, start_time=datetime.utcnow(),
            input_weight_kg=100.0, output_weight_kg=95.0, rejected_quantity_kg=5.0,
        ))
        self.db.commit()

        job = ops_svc.record_processing_job(self.db, {
            "company_id": comp.id, "branch_id": b1.id, "incoming_batch_id": batch.id,
            "operator_employee_id": emp.id, "job_number": "PJ-01", "process_type": "shredding",
            "start_time": datetime.utcnow(), "input_weight_kg": 95.0, "output_weight_kg": 90.0, "rejected_quantity_kg": 5.0,
        })
        rec = ops_svc.record_recovery_job_and_output(
            self.db,
            {"company_id": comp.id, "branch_id": b1.id, "incoming_batch_id": batch.id, "processing_job_id": job.id, "responsible_employee_id": emp.id, "job_number": "RJ-01", "recovery_date": date(2026, 11, 21)},
            material_type_id=mat.id, measured_weight_kg=18.5, predicted_weight_kg=19.2, estimated_weight_kg=17.5,
        )
        assert rec.measured_weight_kg == 18.5
        assert rec.predicted_weight_kg == 19.2
        assert rec.estimated_weight_kg == 17.5

        inv_item = ERPInventoryItem(company_id=comp.id, branch_id=b1.id, material_type_id=mat.id, sku_code="SKU-CU", item_name="Recovered Copper")
        self.db.add(inv_item)
        self.db.commit()

        stock = wh_svc.apply_stock_transaction(
            self.db, comp.id, b1.id, wh.id, inv_item.id, "RECEIVE", 18.5,
            incoming_batch_id=batch.id, employee_id=emp.id,
        )
        assert stock.closing_stock_kg == 18.5

        # Negative stock issue rejected atomically
        with pytest.raises(ValueError, match="Insufficient stock"):
            wh_svc.apply_stock_transaction(self.db, comp.id, b1.id, wh.id, inv_item.id, "SALE", 25.0, incoming_batch_id=batch.id)
        self.db.refresh(stock)
        assert stock.closing_stock_kg == 18.5

        cust = sales_svc.create_customer(self.db, {"company_id": comp.id, "branch_id": b1.id, "customer_code": "CUST-1", "name": "Aurubis Refiner"})
        so = sales_svc.create_sales_order(
            self.db,
            {"company_id": comp.id, "branch_id": b1.id, "customer_id": cust.id, "so_number": "SO-1001", "order_date": date(2026, 11, 22)},
            items=[{"recovered_material_name": "Copper", "inventory_item_id": inv_item.id, "quantity_kg": 10.0, "unit_price": 9.5, "tax_rate_pct": 10.0}],
        )
        assert so.total_amount == 104.5
        stock_after_sale = wh_svc.apply_stock_transaction(
            self.db, comp.id, b1.id, wh.id, inv_item.id, "SALE", 10.0,
            incoming_batch_id=batch.id, reference_type="sales_order", reference_id=so.id,
        )
        assert stock_after_sale.closing_stock_kg == 8.5

        # Verify all 15 DB reports execute cleanly
        rep_svc = ERPReportsService()
        for idx in range(1, 16):
            res = rep_svc.generate_by_number(self.db, idx, comp.id)
            assert "report" in res
        assert rep_svc.material_recovery_report(self.db, comp.id)["total_measured_kg"] == 18.5
        assert rep_svc.warehouse_stock_report(self.db, comp.id)["total_closing_kg"] == 8.5
        pl = rep_svc.profit_and_loss_summary(self.db, comp.id)
        assert pl["is_audited_statement"] is False

    def test_interbranch_stock_transfer_and_double_entry_finance_guard(self):
        from backend.models.erp_finance_env_ai_audit import ChartOfAccount
        from backend.models.erp_recovery_inv import ERPInventoryItem, Warehouse
        from backend.services.erp_operations_service import FinanceLedgerService, WarehouseInventoryService

        comp, b1, b2, _dept, emp = self._seed_org_hierarchy()
        w1 = Warehouse(company_id=comp.id, branch_id=b1.id, warehouse_code="WH-A", warehouse_name="Plant A Store")
        w2 = Warehouse(company_id=comp.id, branch_id=b2.id, warehouse_code="WH-B", warehouse_name="Hub B Store")
        item = ERPInventoryItem(company_id=comp.id, branch_id=b1.id, sku_code="SKU-AL", item_name="Aluminium Ingot")
        self.db.add_all([w1, w2, item])
        self.db.commit()

        wh_svc = WarehouseInventoryService()
        wh_svc.apply_stock_transaction(self.db, comp.id, b1.id, w1.id, item.id, "OPENING", 50.0, employee_id=emp.id)
        tr = wh_svc.transfer_between_branches(self.db, comp.id, b1.id, b2.id, w1.id, w2.id, item.id, 20.0, "TRF-001", employee_id=emp.id)
        assert tr.quantity_kg == 20.0

        from backend.models.erp_recovery_inv import InventoryStock
        s1 = self.db.query(InventoryStock).filter_by(warehouse_id=w1.id, inventory_item_id=item.id).first()
        s2 = self.db.query(InventoryStock).filter_by(warehouse_id=w2.id, inventory_item_id=item.id).first()
        assert s1.closing_stock_kg == 30.0
        assert s2.closing_stock_kg == 20.0

        # Double-entry finance validation
        cash_acc = ChartOfAccount(company_id=comp.id, account_code="1001", account_name="Cash at Bank", account_type="asset")
        rev_acc = ChartOfAccount(company_id=comp.id, account_code="4001", account_name="Scrap Sales Revenue", account_type="revenue")
        self.db.add_all([cash_acc, rev_acc])
        self.db.commit()

        fin = FinanceLedgerService()
        with pytest.raises(ValueError, match="Unbalanced journal entry"):
            fin.create_journal_entry(
                self.db, comp.id, b1.id, "JE-BAD", date(2026, 11, 22), "Bad Entry",
                [{"account_id": cash_acc.id, "debit_amount": 100.0}, {"account_id": rev_acc.id, "credit_amount": 90.0}],
            )
        je = fin.create_journal_entry(
            self.db, comp.id, b1.id, "JE-001", date(2026, 11, 22), "Material Sale",
            [{"account_id": cash_acc.id, "debit_amount": 104.5}, {"account_id": rev_acc.id, "credit_amount": 104.5}],
        )
        assert je.is_balanced is True
        assert je.is_audited_statement is False


class TestERPSecurityIsolationAndBackupRestore:
    """Verify RBAC permissions, cross-company isolation, API endpoints, and SQLite backup/restore."""

    def setup_method(self):
        from backend.database import get_db
        from backend.main import app

        self.eng, self.db = _isolated_erp_db()
        self._app = app
        self._get_db = get_db

        def _override():
            yield self.db

        app.dependency_overrides[get_db] = _override
        self.client = TestClient(app)

    def teardown_method(self):
        self._app.dependency_overrides.pop(self._get_db, None)
        self.db.close()
        self.eng.dispose()

    def _register_and_login(self, username: str, role: str) -> tuple[str, str]:
        from backend.models.all_models import User
        from backend.services.auth_service import hash_password

        u = User(username=username, email=f"{username}@erp.test", hashed_password=hash_password("StrongPass123!"), role=role, is_active=True)
        self.db.add(u)
        self.db.commit()
        self.db.refresh(u)
        r = self.client.post("/api/v1/auth/login", json={"username": username, "password": "StrongPass123!"})
        assert r.status_code == 200
        return u.id, r.json()["access_token"]

    def test_rbac_financial_admin_and_cross_company_isolation(self):
        from backend.models.erp_org_staff import Company, CompanyBranch, Employee

        # Unauthenticated rejected
        assert self.client.get("/api/v1/erp/companies").status_code == 401
        assert self.client.get("/api/v1/erp/admin/overview").status_code == 401

        _admin_id, admin_tok = self._register_and_login("erp_super_admin", "admin")
        op_id, op_tok = self._register_and_login("erp_branch_op", "operator")

        # Admin creates Company A & Company B
        r_a = self.client.post("/api/v1/erp/companies", json={"company_code": "COMP-A", "legal_name": "Alpha Recycle Ltd"}, headers={"Authorization": f"Bearer {admin_tok}"})
        r_b = self.client.post("/api/v1/erp/companies", json={"company_code": "COMP-B", "legal_name": "Beta Metals Ltd"}, headers={"Authorization": f"Bearer {admin_tok}"})
        assert r_a.status_code == 201 and r_b.status_code == 201
        comp_a_id = r_a.json()["id"]
        comp_b_id = r_b.json()["id"]

        b_a = self.client.post("/api/v1/erp/branches", json={"company_id": comp_a_id, "branch_code": "A-BR1", "branch_name": "Alpha HQ"}, headers={"Authorization": f"Bearer {admin_tok}"}).json()

        # Bind operator user to Company A employee record
        emp_a = Employee(company_id=comp_a_id, branch_id=b_a["id"], user_id=op_id, employee_code="EMP-A1", full_name="Alpha Op", joining_date=date(2026, 1, 1))
        self.db.add(emp_a)
        self.db.commit()

        # Operator CAN access Company A batches & branches
        assert self.client.get(f"/api/v1/erp/companies/{comp_a_id}/branches", headers={"Authorization": f"Bearer {op_tok}"}).status_code == 200
        # Operator CANNOT access Company B data (cross-company blocked 403)
        assert self.client.get(f"/api/v1/erp/companies/{comp_b_id}/branches", headers={"Authorization": f"Bearer {op_tok}"}).status_code == 403
        assert self.client.get(f"/api/v1/erp/companies/{comp_b_id}/incoming-batches", headers={"Authorization": f"Bearer {op_tok}"}).status_code == 403
        # Operator CANNOT access restricted finance or admin endpoints (403)
        assert self.client.post("/api/v1/erp/finance/accounts", json={"company_id": comp_a_id, "account_code": "101", "account_name": "Cash", "account_type": "asset"}, headers={"Authorization": f"Bearer {op_tok}"}).status_code == 403
        assert self.client.get(f"/api/v1/erp/reports/9?company_id={comp_a_id}", headers={"Authorization": f"Bearer {op_tok}"}).status_code == 403
        assert self.client.get("/api/v1/erp/admin/overview", headers={"Authorization": f"Bearer {op_tok}"}).status_code == 403

        # Admin accesses restricted financial report & overview
        assert self.client.get(f"/api/v1/erp/reports/9?company_id={comp_a_id}", headers={"Authorization": f"Bearer {admin_tok}"}).status_code == 200
        assert self.client.get("/api/v1/erp/admin/overview", headers={"Authorization": f"Bearer {admin_tok}"}).status_code == 200

    def test_backup_and_restore_roundtrip(self, tmp_path):
        import sqlite3
        from backend.database import backup_database, build_engine, restore_sqlite_backup
        from backend.migrations.runner import apply_migrations
        from backend.models.erp_org_staff import Company

        src_db = tmp_path / "live_erp.db"
        restore_db = tmp_path / "restored_erp.db"
        eng = build_engine(f"sqlite:///{src_db}")
        try:
            apply_migrations(target_engine=eng, pre_backup=False)
            Session = sessionmaker(bind=eng)
            s = Session()
            s.add(Company(company_code="BK-CO", legal_name="Backup Verification Corp"))
            s.commit()
            s.close()

            b_info = backup_database(backup_dir=tmp_path / "backups", target_engine=eng)
            assert b_info["tables_backed_up"] >= 150
            assert Path(b_info["snapshot_path"]).exists()

            # Write SQLite hot backup directly and simulate corruption/loss followed by restore
            snap_sqlite = tmp_path / "hot_backup.db"
            with sqlite3.connect(str(src_db)) as c1, sqlite3.connect(str(snap_sqlite)) as c2:
                c1.backup(c2)

            res = restore_sqlite_backup(snap_sqlite, restore_db)
            assert res["verified"] is True
            with sqlite3.connect(str(restore_db)) as verify:
                row = verify.execute("SELECT legal_name FROM companies WHERE company_code='BK-CO'").fetchone()
                assert row and row[0] == "Backup Verification Corp"
        finally:
            eng.dispose()

    def test_frontend_erp_admin_importable(self):
        from frontend.pages.erp_admin import render_erp_admin
        assert callable(render_erp_admin)
