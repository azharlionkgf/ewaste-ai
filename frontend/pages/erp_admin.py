"""
E-Waste AI — Company ERP & Database Administration Workspace
=============================================================
Connects Obsidian & Champagne Gold UI directly to the 15-module Industrial
ERP database, RBAC security, transactional warehouse/batch workflows,
all 15 database reports, safe migrations, and backup verification.
"""

from __future__ import annotations

import os
import sys
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from backend.database import SessionLocal
from backend.models.all_models import User
from backend.models.erp_batches_ops import IncomingBatch, Machine
from backend.models.erp_finance_env_ai_audit import ChartOfAccount, ComplianceDocument
from backend.models.erp_org_staff import Company, CompanyBranch, Department, Employee, EmployeeRole
from backend.models.erp_partners import Customer, ProcurementOrder, SalesOrder, Supplier
from backend.models.erp_recovery_inv import ERPInventoryItem, InventoryStock, MaterialType, Warehouse
from backend.services.auth_service import hash_password, verify_password
from backend.services.erp_admin_service import ERPAdminService
from backend.services.erp_core_service import (
    CompanyService,
    EmployeeService,
    LogisticsAndMachineService,
    ProcurementService,
    SalesService,
)
from backend.services.erp_operations_service import (
    IncomingBatchService,
    ProcessingAndRecoveryService,
    WarehouseInventoryService,
)
from backend.services.erp_reports_service import ERPReportsService
from backend.services.erp_security import build_security_context
from frontend.theme import (
    CHART_PALETTE,
    apply_theme,
    empty_state_card,
    hero_banner,
    kpi_card,
    plotly_dark_layout,
    section_header,
    status_badge,
)


def _render_auth_panel(db):
    """Authenticate operator/admin or initialize first administrator (no hardcoded credentials)."""
    admin_exists = db.query(User).filter(User.role == "admin").count() > 0

    if st.session_state.get("erp_user_id"):
        u = db.query(User).filter(User.id == st.session_state["erp_user_id"]).first()
        if u and u.is_active:
            ctx = build_security_context(db, u)
            c1, c2 = st.columns([4, 1])
            with c1:
                st.markdown(
                    f"Signed in as **{u.username}** "
                    + status_badge(u.role.upper(), "gold" if ctx.is_admin else "info")
                    + (f"  · Company Lock: `{ctx.company_id[:8]}...`" if ctx.company_id else "  · Scope: Global"),
                    unsafe_allow_html=True,
                )
            with c2:
                if st.button("Sign Out", type="secondary", key="erp_logout_btn", use_container_width=True):
                    st.session_state.pop("erp_user_id", None)
                    st.rerun()
            return ctx

    section_header(
        "ERP Access Control",
        "Sign in with an active user account to access Company ERP & Database Administration",
        "🔐",
    )
    if not admin_exists:
        st.info("No administrator account exists yet. Create the initial ERP administrator account below.")
        with st.form("erp_bootstrap_admin"):
            c1, c2 = st.columns(2)
            uname = c1.text_input("Admin Username", placeholder="e.g. erp_admin")
            email = c2.text_input("Admin Email", placeholder="admin@company.example")
            fname = c1.text_input("Full Name", value="Plant Administrator")
            pwd = c2.text_input("Password (min 8 chars)", type="password")
            if st.form_submit_button("Create Initial Admin & Sign In", type="primary"):
                if len(uname.strip()) < 3 or len(pwd) < 8 or "@" not in email:
                    st.error("Provide a valid username (3+ chars), email, and 8+ character password.")
                else:
                    u = User(
                        username=uname.strip(),
                        email=email.strip(),
                        hashed_password=hash_password(pwd),
                        full_name=fname.strip(),
                        role="admin",
                        is_active=True,
                    )
                    db.add(u)
                    db.commit()
                    db.refresh(u)
                    st.session_state["erp_user_id"] = u.id
                    st.success("Administrator account created and signed in.")
                    st.rerun()
    else:
        with st.form("erp_login_form"):
            c1, c2 = st.columns(2)
            uname = c1.text_input("Username")
            pwd = c2.text_input("Password", type="password")
            if st.form_submit_button("Sign In to Company ERP", type="primary"):
                u = db.query(User).filter(User.username == uname.strip()).first()
                if u and verify_password(pwd, u.hashed_password) and u.is_active:
                    st.session_state["erp_user_id"] = u.id
                    st.rerun()
                else:
                    st.error("Invalid username/password or inactive account.")
    return None


def render_erp_admin():
    apply_theme()
    hero_banner(
        eyebrow="PRODUCTION INDUSTRIAL ERP DATABASE · 15 MODULES",
        title="Company ERP & Database Administration",
        subtitle=(
            "Multi-company, multi-branch operations database: Company structure, Staff & RBAC, "
            "Procurement, Sales, Batches, Warehouse Stock, 15 DB Reports, Migrations & Backups."
        ),
        icon="🏛️",
        badges=[
            ("POSTGRESQL / SQLITE", "live"),
            ("RBAC & AUDIT", "gold"),
        ],
    )

    db = SessionLocal()
    try:
        ctx = _render_auth_panel(db)
        if ctx is None:
            return

        # Filter companies strictly by security context
        comp_svc = CompanyService()
        companies = comp_svc.list_companies(db, company_id=ctx.company_id)

        # Top telemetry strip
        admin_svc = ERPAdminService()
        overview = admin_svc.get_database_overview()
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            kpi_card("Registered Companies", str(len(companies)), "Active tenant scope", "gold")
        with k2:
            kpi_card("Schema Tables", str(overview["total_tables"]), f"Dialect: {overview['dialect']}", "live" if overview["migration_status"]["is_up_to_date"] else "warning")
        with k3:
            kpi_card("Incoming Batches", str(overview["tables"].get("incoming_batches", 0)), "Weighbridge tracked", "info")
        with k4:
            kpi_card("Stock Ledger Rows", str(overview["tables"].get("inventory_stock", 0)), "Transactional balance", "success")

        tabs = st.tabs([
            "🏢 Company & Branches",
            "👥 Staff & Partners",
            "📥 Batches & Warehouse",
            "⚙️ Machines & Compliance",
            "📊 15 DB Reports",
            "🗄️ DB Admin & Backups",
        ])

        # ── TAB 1: COMPANY & BRANCHES ────────────────────────────────
        with tabs[0]:
            section_header("Companies, Branches & Departments")
            if ctx.is_admin:
                with st.expander("➕ Register New Company", expanded=(len(companies) == 0)):
                    with st.form("erp_new_company"):
                        c1, c2 = st.columns(2)
                        c_code = c1.text_input("Company Code", placeholder="e.g. GREEN-REC-01")
                        l_name = c2.text_input("Legal Name", placeholder="GreenCycle Recycling Pvt Ltd")
                        reg_no = c1.text_input("Registration No.")
                        curr = c2.selectbox("Base Currency", ["USD", "EUR", "INR", "GBP"])
                        if st.form_submit_button("Create Company", type="primary"):
                            if not c_code.strip() or not l_name.strip():
                                st.error("Company Code and Legal Name are required.")
                            else:
                                try:
                                    comp_svc.create_company(db, {
                                        "company_code": c_code.strip(),
                                        "legal_name": l_name.strip(),
                                        "registration_number": reg_no.strip() or None,
                                        "base_currency": curr,
                                    }, actor_id=ctx.user_id)
                                    st.success("Company created.")
                                    st.rerun()
                                except Exception as exc:
                                    db.rollback()
                                    st.error(f"Create company failed: {exc}")

            if not companies:
                empty_state_card("🏢", "No Companies Found", "Create a company above to unlock branch, staff, supplier, warehouse, and batch workflows.")
            else:
                cmap = {f"{c.company_code} — {c.legal_name}": c for c in companies}
                sel_label = st.selectbox("Active Company Context", list(cmap.keys()), key="erp_sel_comp")
                sel_comp = cmap[sel_label]
                st.session_state["erp_active_company_id"] = sel_comp.id

                branches = comp_svc.list_branches(db, sel_comp.id)
                with st.expander("➕ Add Branch / Plant / Warehouse Office", expanded=(len(branches) == 0)):
                    with st.form("erp_new_branch"):
                        b1, b2, b3 = st.columns(3)
                        b_code = b1.text_input("Branch Code", placeholder="PLT-NORTH-01")
                        b_name = b2.text_input("Branch Name", placeholder="North Processing Plant")
                        b_type = b3.selectbox("Branch Type", ["hq", "recycling_plant", "collection_center", "warehouse"])
                        if st.form_submit_button("Create Branch", type="primary"):
                            try:
                                comp_svc.create_branch(db, {
                                    "company_id": sel_comp.id,
                                    "branch_code": b_code.strip(),
                                    "branch_name": b_name.strip(),
                                    "branch_type": b_type,
                                }, actor_id=ctx.user_id)
                                st.success("Branch added.")
                                st.rerun()
                            except Exception as exc:
                                db.rollback()
                                st.error(f"Branch creation failed: {exc}")

                if branches:
                    st.dataframe(
                        pd.DataFrame([{"Code": b.branch_code, "Name": b.branch_name, "Type": b.branch_type, "Active": b.is_active} for b in branches]),
                        use_container_width=True,
                    )

        active_company_id = st.session_state.get("erp_active_company_id") or (companies[0].id if companies else None)
        branches = comp_svc.list_branches(db, active_company_id) if active_company_id else []
        branch_map = {f"{b.branch_code} — {b.branch_name}": b.id for b in branches}

        # ── TAB 2: STAFF & PARTNERS ──────────────────────────────────
        with tabs[1]:
            if not active_company_id or not branches:
                empty_state_card("👥", "Company & Branch Required", "Create a company and at least one branch first.")
            else:
                emp_svc = EmployeeService()
                sup_svc = ProcurementService()
                sales_svc = SalesService()
                c_left, c_right = st.columns(2)
                with c_left:
                    section_header("Employees")
                    with st.expander("➕ Add Employee"):
                        with st.form("erp_add_emp"):
                            ecode = st.text_input("Employee Code", placeholder="EMP-001")
                            ename = st.text_input("Full Name")
                            ebranch = st.selectbox("Assigned Branch", list(branch_map.keys()))
                            jdate = st.date_input("Joining Date", value=date.today())
                            if st.form_submit_button("Register Employee", type="primary"):
                                try:
                                    emp_svc.create_employee(db, {
                                        "company_id": active_company_id,
                                        "branch_id": branch_map[ebranch],
                                        "employee_code": ecode.strip(),
                                        "full_name": ename.strip(),
                                        "joining_date": jdate,
                                    }, actor_id=ctx.user_id)
                                    st.success("Employee registered.")
                                    st.rerun()
                                except Exception as exc:
                                    db.rollback()
                                    st.error(str(exc))
                    emps = emp_svc.list_employees(db, active_company_id)
                    if emps:
                        st.dataframe(pd.DataFrame([{"Code": e.employee_code, "Name": e.full_name, "Joined": str(e.joining_date), "Active": e.is_active} for e in emps]), use_container_width=True)

                with c_right:
                    section_header("Suppliers & Customers")
                    with st.expander("➕ Add Supplier"):
                        with st.form("erp_add_sup"):
                            scode = st.text_input("Supplier Code", placeholder="SUP-001")
                            sname = st.text_input("Supplier Name")
                            stype = st.selectbox("Type", ["corporate", "municipality", "aggregator", "individual"])
                            if st.form_submit_button("Register Supplier", type="primary"):
                                try:
                                    sup_svc.create_supplier(db, {
                                        "company_id": active_company_id,
                                        "branch_id": next(iter(branch_map.values())),
                                        "supplier_code": scode.strip(),
                                        "name": sname.strip(),
                                        "supplier_type": stype,
                                    }, actor_id=ctx.user_id)
                                    st.success("Supplier added.")
                                    st.rerun()
                                except Exception as exc:
                                    db.rollback()
                                    st.error(str(exc))
                    sups = sup_svc.list_suppliers(db, active_company_id)
                    custs = sales_svc.list_customers(db, active_company_id)
                    st.caption(f"Registered Suppliers: {len(sups)} · Customers: {len(custs)}")
                    if sups:
                        st.dataframe(pd.DataFrame([{"Code": s.supplier_code, "Name": s.name, "Type": s.supplier_type} for s in sups]), use_container_width=True)

        # ── TAB 3: BATCHES & WAREHOUSE ───────────────────────────────
        with tabs[2]:
            if not active_company_id or not branches:
                empty_state_card("📥", "Company & Branch Required", "Create a company and branch to manage warehouses and incoming batches.")
            else:
                b_svc = IncomingBatchService()
                wh_svc = WarehouseInventoryService()
                sel_br_label = st.selectbox("Branch Context", list(branch_map.keys()), key="erp_ops_branch")
                sel_branch_id = branch_map[sel_br_label]

                col_w1, col_w2 = st.columns(2)
                with col_w1:
                    section_header("Incoming E-Waste Batch (Weighbridge)")
                    with st.form("erp_inc_batch_form"):
                        bnum = st.text_input("Unique Batch Number", placeholder="INB-2026-001")
                        cat = st.selectbox("E-Waste Category", ["mixed_ewaste", "it_equipment", "mobile_phones", "pcbs", "batteries", "monitors"])
                        gross_kg = st.number_input("Gross Weight (kg)", min_value=0.1, step=1.0, value=100.0)
                        tare_kg = st.number_input("Tare Weight (kg)", min_value=0.0, step=1.0, value=10.0)
                        pval = st.number_input("Purchase Value (USD)", min_value=0.0, step=10.0, value=0.0)
                        if st.form_submit_button("Register Batch & Weighbridge Ticket", type="primary"):
                            try:
                                b = b_svc.register_incoming_batch(db, {
                                    "company_id": active_company_id,
                                    "branch_id": sel_branch_id,
                                    "batch_number": bnum.strip(),
                                    "receiving_date": date.today(),
                                    "ewaste_category": cat,
                                    "gross_weight_kg": gross_kg,
                                    "tare_weight_kg": tare_kg,
                                    "purchase_value": pval,
                                }, actor_id=ctx.user_id)
                                st.success(f"Batch {b.batch_number} registered (Net: {b.net_weight_kg} kg · QR: {b.barcode_qr_code})")
                                st.rerun()
                            except Exception as exc:
                                db.rollback()
                                st.error(str(exc))

                with col_w2:
                    section_header("Warehouses & Stock Ledger")
                    with st.expander("➕ Create Warehouse"):
                        with st.form("erp_new_wh"):
                            wcode = st.text_input("Warehouse Code", placeholder="WH-MAIN-01")
                            wname = st.text_input("Warehouse Name", placeholder="Main Recovered Material Store")
                            wtype = st.selectbox("Type", ["recovered_stock", "raw_ewaste", "hazmat", "dispatch"])
                            if st.form_submit_button("Add Warehouse", type="primary"):
                                try:
                                    db.add(Warehouse(company_id=active_company_id, branch_id=sel_branch_id, warehouse_code=wcode.strip(), warehouse_name=wname.strip(), warehouse_type=wtype, created_by=ctx.user_id))
                                    db.commit()
                                    st.success("Warehouse created.")
                                    st.rerun()
                                except Exception as exc:
                                    db.rollback()
                                    st.error(str(exc))

                batches = db.query(IncomingBatch).filter(IncomingBatch.company_id == active_company_id, IncomingBatch.is_deleted == False).order_by(IncomingBatch.created_at.desc()).all()  # noqa: E712
                if batches:
                    st.dataframe(
                        pd.DataFrame([
                            {"Batch #": b.batch_number, "QR": b.barcode_qr_code, "Category": b.ewaste_category, "Net kg": b.net_weight_kg, "Status": b.batch_status}
                            for b in batches
                        ]),
                        use_container_width=True,
                    )

        # ── TAB 4: MACHINES & COMPLIANCE ─────────────────────────────
        with tabs[3]:
            if not active_company_id or not branches:
                empty_state_card("⚙️", "Company & Branch Required", "Create a company and branch first.")
            else:
                m_svc = LogisticsAndMachineService()
                c_m1, c_m2 = st.columns(2)
                with c_m1:
                    section_header("Processing Machines")
                    with st.form("erp_new_machine"):
                        mcode = st.text_input("Machine Code", placeholder="SHRED-01")
                        mname = st.text_input("Machine Name", placeholder="Primary Dual-Shaft Shredder")
                        mcap = st.number_input("Rated Capacity (kg/hr)", min_value=0.0, value=500.0)
                        if st.form_submit_button("Register Machine", type="primary"):
                            try:
                                m_svc.create_machine(db, {
                                    "company_id": active_company_id,
                                    "branch_id": next(iter(branch_map.values())),
                                    "machine_code": mcode.strip(),
                                    "machine_name": mname.strip(),
                                    "rated_capacity_kg_hr": mcap,
                                }, actor_id=ctx.user_id)
                                st.success("Machine registered.")
                                st.rerun()
                            except Exception as exc:
                                db.rollback()
                                st.error(str(exc))
                with c_m2:
                    section_header("Compliance Document Registry")
                    st.caption("⚠️ Recording documents does NOT confer automatic legal certification.")
                    with st.form("erp_new_compdoc"):
                        dcode = st.text_input("Document Code", placeholder="ENV-MANIFEST-01")
                        dcat = st.text_input("Compliance Category", value="E-Waste Handling Record")
                        dtitle = st.text_input("Document Title")
                        if st.form_submit_button("Record Document", type="primary"):
                            try:
                                db.add(ComplianceDocument(
                                    company_id=active_company_id,
                                    branch_id=next(iter(branch_map.values())),
                                    document_code=dcode.strip(),
                                    compliance_category=dcat.strip(),
                                    title=dtitle.strip(),
                                    is_legal_certification=False,
                                    created_by=ctx.user_id,
                                ))
                                db.commit()
                                st.success("Compliance document logged.")
                                st.rerun()
                            except Exception as exc:
                                db.rollback()
                                st.error(str(exc))

        # ── TAB 5: 15 LIVE DATABASE REPORTS ──────────────────────────
        with tabs[4]:
            if not active_company_id:
                empty_state_card("📊", "Company Context Required", "Register or select a company to generate ERP database reports.")
            else:
                section_header("15 Live Company Database Reports", "Real database queries only — no synthetic placeholder rows")
                REPORT_LABELS = {
                    1: "1. Daily Incoming E-Waste Report",
                    2: "2. Supplier-Wise Purchase Report",
                    3: "3. Batch Processing Report",
                    4: "4. Material Recovery Report",
                    5: "5. Warehouse Stock Report",
                    6: "6. Material Sales Report",
                    7: "7. Customer-Wise Sales Report",
                    8: "8. Purchase & Expense Report (Restricted)",
                    9: "9. Profit & Loss Summary (Restricted · Operational Only)",
                    10: "10. Machine Utilization Report",
                    11: "11. Employee Activity Report",
                    12: "12. Hazardous Waste Tracking Report",
                    13: "13. Environmental Records Report (Non-Certified)",
                    14: "14. AI Prediction Performance Report",
                    15: "15. Branch-Wise Business Performance Report",
                }
                r_num = st.selectbox("Select ERP Report", list(REPORT_LABELS.keys()), format_func=lambda k: REPORT_LABELS[k])
                if r_num in {8, 9} and not (ctx.is_admin or ctx.is_financial_authorized):
                    st.error("🔒 Restricted: Purchase/Expense and P&L reports require authorized finance or administrator access.")
                else:
                    rep = ERPReportsService().generate_by_number(db, r_num, active_company_id)
                    st.json(rep)
                    if isinstance(rep.get("rows"), list) and rep["rows"]:
                        df_rep = pd.DataFrame(rep["rows"])
                        st.dataframe(df_rep, use_container_width=True)
                        st.download_button("⬇️ Download Report CSV", df_rep.to_csv(index=False).encode(), f"erp_report_{r_num}.csv", "text/csv")

        # ── TAB 6: DATABASE ADMINISTRATION (ADMIN ONLY) ────────────────
        with tabs[5]:
            if not ctx.is_admin:
                st.error("🔒 Administrator privileges required to inspect system tables, run migrations, or trigger backups.")
            else:
                section_header("Database Schema, Migrations & Backups", "Central PostgreSQL/SQLite ERP Inspection")
                c_b1, c_b2 = st.columns(2)
                if c_b1.button("💾 Create Live Backup Snapshot", type="primary", use_container_width=True):
                    b_res = admin_svc.create_backup()
                    st.success(f"Backup created ({b_res['tables_backed_up']} tables, {b_res['total_rows']} rows)")
                    st.code(b_res.get("snapshot_path") or b_res.get("sqlite_backup_path") or "")
                if c_b2.button("🔄 Verify / Apply Safe Migrations", type="secondary", use_container_width=True):
                    m_res = admin_svc.run_safe_migration(pre_backup=True)
                    st.success(f"Migrations up to date ({m_res['total_tables']} tables)")

                filter_tbl = st.text_input("Filter 152+ Database Tables", placeholder="e.g. incoming, stock, journal, employee")
                tbl_rows = [
                    {"Table Name": t, "Row Count": cnt}
                    for t, cnt in overview["tables"].items()
                    if not filter_tbl.strip() or filter_tbl.strip().lower() in t.lower()
                ]
                st.dataframe(pd.DataFrame(tbl_rows), use_container_width=True, height=380)

                if tbl_rows:
                    non_empty = [r for r in tbl_rows if r["Row Count"] > 0][:15]
                    if non_empty:
                        fig = go.Figure(go.Bar(x=[r["Table Name"] for r in non_empty], y=[r["Row Count"] for r in non_empty], marker_color="#C9A84C"))
                        plotly_dark_layout(fig, title="Non-Empty Tables Row Distribution", height=280, yaxis_title="Rows")
                        st.plotly_chart(fig, use_container_width=True)

                with st.expander("📜 Applied Schema Migration Revisions"):
                    st.dataframe(pd.DataFrame(overview["migration_status"]["applied_migrations"]), use_container_width=True)
    finally:
        db.close()
