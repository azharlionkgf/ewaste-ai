"""
E-Waste AI — FastAPI Industrial ERP Routers (Modules 1–15, Reports & Admin)
===========================================================================
All endpoints enforce JWT authentication, role-based permissions, strict
company/branch isolation, input validation, and unified audit logging.
"""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.erp_batches_ops import IncomingBatch, Machine
from backend.models.erp_finance_env_ai_audit import ChartOfAccount, ComplianceDocument
from backend.models.erp_org_staff import CompanyBranch
from backend.models.erp_recovery_inv import ERPInventoryItem, InventoryStock, Warehouse
from backend.schemas.erp_schemas import (
    AIFeedbackIn,
    AccountCreate,
    BatchStatusTransitionIn,
    BranchCreate,
    CompanyCreate,
    ComplianceDocCreate,
    CustomerCreate,
    DepartmentCreate,
    EmployeeCreate,
    EmployeeRoleCreate,
    IncomingBatchCreate,
    InventoryItemCreateERP,
    JournalEntryCreate,
    MachineCreate,
    MaterialTransferIn,
    MaterialTypeCreate,
    ProcessingJobCreate,
    ProcurementOrderCreate,
    RecoveryJobRecordIn,
    SalesOrderCreate,
    StockTxnIn,
    SupplierCreate,
    WarehouseCreate,
)
from backend.services.erp_admin_service import ERPAdminService
from backend.services.erp_core_service import (
    CompanyService,
    EmployeeService,
    LogisticsAndMachineService,
    ProcurementService,
    SalesService,
)
from backend.services.erp_operations_service import (
    ComplianceAIService,
    FinanceLedgerService,
    IncomingBatchService,
    ProcessingAndRecoveryService,
    WarehouseInventoryService,
)
from backend.services.erp_reports_service import ERPReportsService
from backend.services.erp_security import (
    ERPSecurityContext,
    enforce_company_branch_scope,
    require_erp_permission,
)

erp_router = APIRouter(prefix="/api/v1/erp", tags=["Industrial ERP"])

_company_svc = CompanyService()
_emp_svc = EmployeeService()
_proc_svc = ProcurementService()
_sales_svc = SalesService()
_mach_svc = LogisticsAndMachineService()
_batch_svc = IncomingBatchService()
_proc_rec_svc = ProcessingAndRecoveryService()
_wh_svc = WarehouseInventoryService()
_fin_svc = FinanceLedgerService()
_comp_ai_svc = ComplianceAIService()
_rep_svc = ERPReportsService()
_admin_svc = ERPAdminService()


# ── Module 1: Companies & Branches ───────────────────────────────────────

@erp_router.post("/companies", status_code=status.HTTP_201_CREATED)
def create_company(
    payload: CompanyCreate,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("company:write", admin_only=True)),
):
    c = _company_svc.create_company(db, payload.model_dump(), actor_id=ctx.user_id)
    return {"id": c.id, "company_code": c.company_code, "legal_name": c.legal_name}


@erp_router.get("/companies")
def list_companies(
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("company:read")),
):
    rows = _company_svc.list_companies(db, company_id=ctx.company_id)
    return [{"id": c.id, "company_code": c.company_code, "legal_name": c.legal_name, "is_active": c.is_active} for c in rows]


@erp_router.post("/branches", status_code=status.HTTP_201_CREATED)
def create_branch(
    payload: BranchCreate,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("company:write")),
):
    enforce_company_branch_scope(ctx, payload.company_id)
    b = _company_svc.create_branch(db, payload.model_dump(), actor_id=ctx.user_id)
    return {"id": b.id, "company_id": b.company_id, "branch_code": b.branch_code, "branch_name": b.branch_name}


@erp_router.get("/companies/{company_id}/branches")
def list_branches(
    company_id: str,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("company:read")),
):
    enforce_company_branch_scope(ctx, company_id)
    rows = _company_svc.list_branches(db, company_id)
    return [{"id": b.id, "branch_code": b.branch_code, "branch_name": b.branch_name, "branch_type": b.branch_type} for b in rows]


@erp_router.post("/departments", status_code=status.HTTP_201_CREATED)
def create_department(
    payload: DepartmentCreate,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("company:write")),
):
    enforce_company_branch_scope(ctx, payload.company_id, payload.branch_id)
    d = _company_svc.create_department(db, payload.model_dump(), actor_id=ctx.user_id)
    return {"id": d.id, "dept_code": d.dept_code, "dept_name": d.dept_name}


# ── Module 2: Employees & Roles ──────────────────────────────────────────

@erp_router.post("/roles", status_code=status.HTTP_201_CREATED)
def create_employee_role(
    payload: EmployeeRoleCreate,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("employee:write", admin_only=True)),
):
    enforce_company_branch_scope(ctx, payload.company_id)
    r = _emp_svc.create_role(db, payload.model_dump(), actor_id=ctx.user_id)
    return {"id": r.id, "role_code": r.role_code, "role_name": r.role_name}


@erp_router.post("/employees", status_code=status.HTTP_201_CREATED)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("employee:write")),
):
    enforce_company_branch_scope(ctx, payload.company_id, payload.branch_id)
    e = _emp_svc.create_employee(db, payload.model_dump(), actor_id=ctx.user_id)
    return {"id": e.id, "employee_code": e.employee_code, "full_name": e.full_name}


@erp_router.get("/companies/{company_id}/employees")
def list_employees(
    company_id: str,
    branch_id: Optional[str] = None,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("employee:read")),
):
    enforce_company_branch_scope(ctx, company_id, branch_id)
    rows = _emp_svc.list_employees(db, company_id, branch_id=branch_id)
    return [{"id": e.id, "employee_code": e.employee_code, "full_name": e.full_name, "branch_id": e.branch_id} for e in rows]


# ── Module 3 & 4: Suppliers, Procurement, Customers & Sales ──────────────

@erp_router.post("/suppliers", status_code=status.HTTP_201_CREATED)
def create_supplier(
    payload: SupplierCreate,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("procurement:write")),
):
    enforce_company_branch_scope(ctx, payload.company_id, payload.branch_id)
    s = _proc_svc.create_supplier(db, payload.model_dump(), actor_id=ctx.user_id)
    return {"id": s.id, "supplier_code": s.supplier_code, "name": s.name}


@erp_router.post("/procurement-orders", status_code=status.HTTP_201_CREATED)
def create_procurement_order(
    payload: ProcurementOrderCreate,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("procurement:write")),
):
    enforce_company_branch_scope(ctx, payload.company_id, payload.branch_id)
    order_data = payload.model_dump(exclude={"items"})
    po = _proc_svc.create_procurement_order(db, order_data, [i.model_dump() for i in payload.items], actor_id=ctx.user_id)
    return {"id": po.id, "po_number": po.po_number, "total_weight_kg": po.total_weight_kg, "purchase_price_total": po.purchase_price_total}


@erp_router.post("/customers", status_code=status.HTTP_201_CREATED)
def create_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("sales:write")),
):
    enforce_company_branch_scope(ctx, payload.company_id, payload.branch_id)
    c = _sales_svc.create_customer(db, payload.model_dump(), actor_id=ctx.user_id)
    return {"id": c.id, "customer_code": c.customer_code, "name": c.name}


@erp_router.post("/sales-orders", status_code=status.HTTP_201_CREATED)
def create_sales_order(
    payload: SalesOrderCreate,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("sales:write")),
):
    enforce_company_branch_scope(ctx, payload.company_id, payload.branch_id)
    order_data = payload.model_dump(exclude={"items"})
    so = _sales_svc.create_sales_order(db, order_data, [i.model_dump() for i in payload.items], actor_id=ctx.user_id)
    return {"id": so.id, "so_number": so.so_number, "total_amount": so.total_amount}


# ── Module 5 & 6: Incoming Batches & Processing ──────────────────────────

@erp_router.post("/incoming-batches", status_code=status.HTTP_201_CREATED)
def register_incoming_batch(
    payload: IncomingBatchCreate,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("batch:write")),
):
    enforce_company_branch_scope(ctx, payload.company_id, payload.branch_id)
    try:
        b = _batch_svc.register_incoming_batch(db, payload.model_dump(), actor_id=ctx.user_id)
        return {"id": b.id, "batch_number": b.batch_number, "net_weight_kg": b.net_weight_kg, "barcode_qr_code": b.barcode_qr_code}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@erp_router.get("/companies/{company_id}/incoming-batches")
def list_incoming_batches(
    company_id: str,
    branch_id: Optional[str] = None,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("batch:read")),
):
    enforce_company_branch_scope(ctx, company_id, branch_id)
    q = db.query(IncomingBatch).filter(IncomingBatch.company_id == company_id, IncomingBatch.is_deleted == False)  # noqa: E712
    if branch_id:
        q = q.filter(IncomingBatch.branch_id == branch_id)
    rows = q.order_by(IncomingBatch.created_at.desc()).all()
    return [
        {"id": b.id, "batch_number": b.batch_number, "net_weight_kg": b.net_weight_kg, "batch_status": b.batch_status, "branch_id": b.branch_id}
        for b in rows
    ]


@erp_router.patch("/incoming-batches/{batch_id}/status")
def transition_incoming_batch(
    batch_id: str,
    payload: BatchStatusTransitionIn,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("batch:write")),
):
    batch = db.query(IncomingBatch).filter(IncomingBatch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Incoming batch not found")
    enforce_company_branch_scope(ctx, batch.company_id, batch.branch_id)
    updated = _batch_svc.transition_batch_status(db, batch_id, payload.new_status, employee_id=payload.employee_id, reason=payload.reason, actor_id=ctx.user_id)
    return {"id": updated.id, "batch_status": updated.batch_status}


@erp_router.post("/processing-jobs", status_code=status.HTTP_201_CREATED)
def create_processing_job(
    payload: ProcessingJobCreate,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("processing:write")),
):
    enforce_company_branch_scope(ctx, payload.company_id, payload.branch_id)
    job = _proc_rec_svc.record_processing_job(db, payload.model_dump(), actor_id=ctx.user_id)
    return {"id": job.id, "job_number": job.job_number, "status": job.status}


# ── Module 7, 8 & 9: Materials, Recovery & Warehouse ─────────────────────

@erp_router.post("/material-types", status_code=status.HTTP_201_CREATED)
def create_material_type(
    payload: MaterialTypeCreate,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("recovery:write")),
):
    enforce_company_branch_scope(ctx, payload.company_id)
    from backend.models.erp_recovery_inv import MaterialType
    m = MaterialType(**payload.model_dump(), created_by=ctx.user_id)
    db.add(m)
    db.commit()
    db.refresh(m)
    return {"id": m.id, "material_code": m.material_code, "material_name": m.material_name}


@erp_router.post("/recovery-jobs", status_code=status.HTTP_201_CREATED)
def record_recovery_job(
    payload: RecoveryJobRecordIn,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("recovery:write")),
):
    enforce_company_branch_scope(ctx, payload.company_id, payload.branch_id)
    job_data = {
        "company_id": payload.company_id,
        "branch_id": payload.branch_id,
        "incoming_batch_id": payload.incoming_batch_id,
        "processing_job_id": payload.processing_job_id,
        "responsible_employee_id": payload.responsible_employee_id,
        "job_number": payload.job_number,
        "recovery_date": payload.recovery_date,
        "status": "completed",
    }
    rec = _proc_rec_svc.record_recovery_job_and_output(
        db, job_data, payload.material_type_id, payload.measured_weight_kg,
        predicted_weight_kg=payload.predicted_weight_kg,
        estimated_weight_kg=payload.estimated_weight_kg,
        quality_grade=payload.quality_grade,
        final_destination=payload.final_destination,
        actor_id=ctx.user_id,
    )
    return {"id": rec.id, "measured_weight_kg": rec.measured_weight_kg, "predicted_weight_kg": rec.predicted_weight_kg}


@erp_router.post("/warehouses", status_code=status.HTTP_201_CREATED)
def create_warehouse(
    payload: WarehouseCreate,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("warehouse:write")),
):
    enforce_company_branch_scope(ctx, payload.company_id, payload.branch_id)
    w = Warehouse(**payload.model_dump(), created_by=ctx.user_id)
    db.add(w)
    db.commit()
    db.refresh(w)
    return {"id": w.id, "warehouse_code": w.warehouse_code, "warehouse_name": w.warehouse_name}


@erp_router.post("/inventory-items", status_code=status.HTTP_201_CREATED)
def create_inventory_item_erp(
    payload: InventoryItemCreateERP,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("warehouse:write")),
):
    enforce_company_branch_scope(ctx, payload.company_id, payload.branch_id)
    item = ERPInventoryItem(**payload.model_dump(), created_by=ctx.user_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "sku_code": item.sku_code, "item_name": item.item_name}


@erp_router.post("/inventory/transactions", status_code=status.HTTP_201_CREATED)
def post_inventory_transaction(
    payload: StockTxnIn,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("warehouse:write")),
):
    enforce_company_branch_scope(ctx, payload.company_id, payload.branch_id)
    try:
        stock = _wh_svc.apply_stock_transaction(
            db, payload.company_id, payload.branch_id, payload.warehouse_id,
            payload.inventory_item_id, payload.txn_type, payload.quantity_kg,
            incoming_batch_id=payload.incoming_batch_id,
            reference_type=payload.reference_type, reference_id=payload.reference_id,
            employee_id=ctx.employee_id, actor_id=ctx.user_id,
        )
        return {"stock_id": stock.id, "closing_stock_kg": stock.closing_stock_kg}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@erp_router.post("/inventory/transfers", status_code=status.HTTP_201_CREATED)
def transfer_material_between_branches(
    payload: MaterialTransferIn,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("warehouse:write")),
):
    enforce_company_branch_scope(ctx, payload.company_id, payload.from_branch_id)
    try:
        tr = _wh_svc.transfer_between_branches(
            db, payload.company_id, payload.from_branch_id, payload.to_branch_id,
            payload.from_warehouse_id, payload.to_warehouse_id, payload.inventory_item_id,
            payload.quantity_kg, payload.transfer_number,
            incoming_batch_id=payload.incoming_batch_id,
            employee_id=ctx.employee_id, actor_id=ctx.user_id,
        )
        return {"id": tr.id, "transfer_number": tr.transfer_number, "quantity_kg": tr.quantity_kg}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# ── Module 10: Finance & Accounting (Strictly Restricted) ────────────────

@erp_router.post("/finance/accounts", status_code=status.HTTP_201_CREATED)
def create_account(
    payload: AccountCreate,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("finance:write", financial=True)),
):
    enforce_company_branch_scope(ctx, payload.company_id)
    acc = ChartOfAccount(**payload.model_dump(), created_by=ctx.user_id)
    db.add(acc)
    db.commit()
    db.refresh(acc)
    return {"id": acc.id, "account_code": acc.account_code, "account_name": acc.account_name}


@erp_router.post("/finance/journal-entries", status_code=status.HTTP_201_CREATED)
def post_journal_entry(
    payload: JournalEntryCreate,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("finance:write", financial=True)),
):
    enforce_company_branch_scope(ctx, payload.company_id, payload.branch_id)
    try:
        je = _fin_svc.create_journal_entry(
            db, payload.company_id, payload.branch_id,
            payload.entry_number, payload.entry_date, payload.description,
            [l.model_dump() for l in payload.lines], actor_id=ctx.user_id,
        )
        return {"id": je.id, "entry_number": je.entry_number, "total_debit": je.total_debit, "is_balanced": je.is_balanced, "is_audited_statement": je.is_audited_statement}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# ── Module 12, 13 & 14: Machines, Compliance & AI Feedback ───────────────

@erp_router.post("/machines", status_code=status.HTTP_201_CREATED)
def create_machine(
    payload: MachineCreate,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("machine:write")),
):
    enforce_company_branch_scope(ctx, payload.company_id, payload.branch_id)
    m = _mach_svc.create_machine(db, payload.model_dump(), actor_id=ctx.user_id)
    return {"id": m.id, "machine_code": m.machine_code, "machine_name": m.machine_name}


@erp_router.post("/compliance/documents", status_code=status.HTTP_201_CREATED)
def record_compliance_doc(
    payload: ComplianceDocCreate,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("compliance:write")),
):
    enforce_company_branch_scope(ctx, payload.company_id, payload.branch_id)
    doc = ComplianceDocument(**payload.model_dump(), created_by=ctx.user_id)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return {"id": doc.id, "document_code": doc.document_code, "is_legal_certification": doc.is_legal_certification}


@erp_router.post("/ai/feedback", status_code=status.HTTP_201_CREATED)
def submit_ai_feedback(
    payload: AIFeedbackIn,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("ai:write")),
):
    enforce_company_branch_scope(ctx, payload.company_id, payload.branch_id)
    try:
        fb = _comp_ai_svc.verify_ai_prediction(
            db, payload.company_id, payload.branch_id, payload.ai_prediction_id,
            payload.is_accurate, corrected_label=payload.corrected_label,
            final_measured_outcome=payload.final_measured_outcome,
            reviewer_employee_id=ctx.employee_id, actor_id=ctx.user_id,
        )
        return {"id": fb.id, "is_accurate": fb.is_accurate}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


# ── Module 15 / 15 Real Database Reports ─────────────────────────────────

@erp_router.get("/reports/{report_number}")
def run_erp_report(
    report_number: int,
    company_id: str,
    branch_id: Optional[str] = None,
    db: Session = Depends(get_db),
    ctx: ERPSecurityContext = Depends(require_erp_permission("reports:read")),
):
    enforce_company_branch_scope(ctx, company_id, branch_id)
    if report_number in {8, 9} and not (ctx.is_admin or ctx.is_financial_authorized):
        raise HTTPException(status_code=403, detail="Financial reports restricted to authorized finance/admin roles")
    try:
        return _rep_svc.generate_by_number(db, report_number, company_id, branch_id=branch_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# ── Database & System Administration (Admin Only) ────────────────────────

@erp_router.get("/admin/overview")
def erp_admin_overview(
    _ctx: ERPSecurityContext = Depends(require_erp_permission("admin:access", admin_only=True)),
):
    return _admin_svc.get_database_overview()


@erp_router.post("/admin/backup")
def erp_admin_backup(
    _ctx: ERPSecurityContext = Depends(require_erp_permission("admin:access", admin_only=True)),
):
    return _admin_svc.create_backup()
