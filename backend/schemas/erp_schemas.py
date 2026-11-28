"""
E-Waste AI — Pydantic v2 Schemas for Industrial ERP Modules 1–15
================================================================
Uses ConfigDict(from_attributes=True) and explicit numeric bounds.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class ERPBaseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ── Module 1: Company & Branches ─────────────────────────────────────────

class CompanyCreate(BaseModel):
    company_code: str = Field(..., min_length=2, max_length=64)
    legal_name: str = Field(..., min_length=2, max_length=256)
    trade_name: Optional[str] = None
    registration_number: Optional[str] = None
    tax_id: Optional[str] = None
    base_currency: str = "USD"


class CompanyOut(ERPBaseOut):
    id: str
    company_code: str
    legal_name: str
    trade_name: Optional[str] = None
    base_currency: str
    is_active: bool
    created_at: datetime


class BranchCreate(BaseModel):
    company_id: str
    branch_code: str = Field(..., min_length=2, max_length=64)
    branch_name: str = Field(..., min_length=2, max_length=256)
    branch_type: str = "recycling_plant"
    is_head_office: bool = False


class BranchOut(ERPBaseOut):
    id: str
    company_id: str
    branch_code: str
    branch_name: str
    branch_type: str
    is_head_office: bool
    is_active: bool


class DepartmentCreate(BaseModel):
    company_id: str
    branch_id: Optional[str] = None
    dept_code: str = Field(..., min_length=1, max_length=64)
    dept_name: str = Field(..., min_length=2, max_length=128)
    description: Optional[str] = None


# ── Module 2: Employees & RBAC ───────────────────────────────────────────

class EmployeeRoleCreate(BaseModel):
    company_id: str
    role_code: str = Field(..., min_length=2, max_length=64)
    role_name: str = Field(..., min_length=2, max_length=128)
    is_financial_restricted: bool = False
    is_admin_role: bool = False


class EmployeeCreate(BaseModel):
    company_id: str
    branch_id: Optional[str] = None
    user_id: Optional[str] = None
    employee_code: str = Field(..., min_length=2, max_length=64)
    full_name: str = Field(..., min_length=2, max_length=256)
    email: Optional[str] = None
    phone: Optional[str] = None
    department_id: Optional[str] = None
    role_id: Optional[str] = None
    joining_date: date
    authorized_operations: Optional[list[str]] = None


class EmployeeOut(ERPBaseOut):
    id: str
    company_id: str
    branch_id: Optional[str] = None
    employee_code: str
    full_name: str
    joining_date: date
    is_active: bool


# ── Module 3 & 4: Suppliers, Procurement, Customers & Sales ──────────────

class SupplierCreate(BaseModel):
    company_id: str
    branch_id: Optional[str] = None
    supplier_code: str = Field(..., min_length=2, max_length=64)
    name: str = Field(..., min_length=2, max_length=256)
    supplier_type: str = "corporate"
    registration_number: Optional[str] = None
    tax_id: Optional[str] = None


class ProcurementItemIn(BaseModel):
    ewaste_category: str
    item_description: Optional[str] = None
    quantity: float = Field(0.0, ge=0)
    weight_kg: float = Field(0.0, ge=0)
    unit_price: float = Field(0.0, ge=0)


class ProcurementOrderCreate(BaseModel):
    company_id: str
    branch_id: str
    supplier_id: str
    po_number: str = Field(..., min_length=2, max_length=64)
    order_date: date
    ewaste_category: str
    transportation_cost: float = Field(0.0, ge=0)
    items: list[ProcurementItemIn] = Field(default_factory=list)


class CustomerCreate(BaseModel):
    company_id: str
    branch_id: Optional[str] = None
    customer_code: str = Field(..., min_length=2, max_length=64)
    name: str = Field(..., min_length=2, max_length=256)
    customer_type: str = "smelter"


class SalesItemIn(BaseModel):
    recovered_material_name: str
    inventory_item_id: Optional[str] = None
    quantity_kg: float = Field(..., gt=0)
    unit_price: float = Field(..., ge=0)
    tax_rate_pct: float = Field(0.0, ge=0)


class SalesOrderCreate(BaseModel):
    company_id: str
    branch_id: str
    customer_id: str
    so_number: str = Field(..., min_length=2, max_length=64)
    order_date: date
    items: list[SalesItemIn] = Field(default_factory=list)


# ── Module 5 & 6: Incoming Batches & Processing ──────────────────────────

class IncomingBatchCreate(BaseModel):
    company_id: str
    branch_id: str
    warehouse_id: Optional[str] = None
    supplier_id: Optional[str] = None
    procurement_order_id: Optional[str] = None
    responsible_employee_id: Optional[str] = None
    batch_number: str = Field(..., min_length=2, max_length=64)
    barcode_qr_code: Optional[str] = None
    receiving_date: date
    ewaste_category: str
    device_type: Optional[str] = None
    gross_weight_kg: float = Field(..., gt=0)
    tare_weight_kg: float = Field(0.0, ge=0)
    purchase_value: float = Field(0.0, ge=0)
    notes: Optional[str] = None


class BatchStatusTransitionIn(BaseModel):
    new_status: str
    employee_id: Optional[str] = None
    reason: str = ""


class ProcessingJobCreate(BaseModel):
    company_id: str
    branch_id: str
    incoming_batch_id: str
    machine_id: Optional[str] = None
    operator_employee_id: Optional[str] = None
    job_number: str
    process_type: str
    start_time: datetime
    input_weight_kg: float = Field(..., ge=0)
    output_weight_kg: float = Field(0.0, ge=0)
    rejected_quantity_kg: float = Field(0.0, ge=0)
    status: str = "completed"


# ── Module 7, 8 & 9: Materials, Recovery & Warehouse ─────────────────────

class MaterialTypeCreate(BaseModel):
    company_id: str
    material_code: str
    material_name: str
    material_group: str
    is_hazardous: bool = False


class RecoveryJobRecordIn(BaseModel):
    company_id: str
    branch_id: str
    incoming_batch_id: str
    processing_job_id: Optional[str] = None
    responsible_employee_id: Optional[str] = None
    job_number: str
    recovery_date: date
    material_type_id: str
    measured_weight_kg: float = Field(..., ge=0)
    predicted_weight_kg: Optional[float] = Field(None, ge=0)
    estimated_weight_kg: Optional[float] = Field(None, ge=0)
    quality_grade: str = "A"
    final_destination: str = "warehouse"


class WarehouseCreate(BaseModel):
    company_id: str
    branch_id: str
    warehouse_code: str
    warehouse_name: str
    warehouse_type: str = "recovered_stock"
    capacity_kg: float = Field(0.0, ge=0)


class InventoryItemCreateERP(BaseModel):
    company_id: str
    branch_id: str
    material_type_id: Optional[str] = None
    sku_code: str
    item_name: str
    min_stock_kg: float = Field(0.0, ge=0)


class StockTxnIn(BaseModel):
    company_id: str
    branch_id: str
    warehouse_id: str
    inventory_item_id: str
    txn_type: str
    quantity_kg: float
    incoming_batch_id: Optional[str] = None
    reference_type: Optional[str] = None
    reference_id: Optional[str] = None


class MaterialTransferIn(BaseModel):
    company_id: str
    from_branch_id: str
    to_branch_id: str
    from_warehouse_id: str
    to_warehouse_id: str
    inventory_item_id: str
    quantity_kg: float = Field(..., gt=0)
    transfer_number: str
    incoming_batch_id: Optional[str] = None


# ── Module 10, 12, 13, 14: Finance, Machines, Compliance, AI ─────────────

class AccountCreate(BaseModel):
    company_id: str
    account_code: str
    account_name: str
    account_type: str


class JournalLineIn(BaseModel):
    account_id: str
    debit_amount: float = Field(0.0, ge=0)
    credit_amount: float = Field(0.0, ge=0)
    description: Optional[str] = None


class JournalEntryCreate(BaseModel):
    company_id: str
    branch_id: Optional[str] = None
    entry_number: str
    entry_date: date
    description: str
    lines: list[JournalLineIn]


class MachineCreate(BaseModel):
    company_id: str
    branch_id: str
    machine_code: str
    machine_name: str
    rated_capacity_kg_hr: float = Field(0.0, ge=0)


class ComplianceDocCreate(BaseModel):
    company_id: str
    branch_id: str
    document_code: str
    compliance_category: str
    jurisdiction_reference: Optional[str] = None
    title: str


class AIFeedbackIn(BaseModel):
    company_id: str
    branch_id: Optional[str] = None
    ai_prediction_id: str
    is_accurate: bool
    corrected_label: Optional[str] = None
    final_measured_outcome: Optional[dict[str, Any]] = None
