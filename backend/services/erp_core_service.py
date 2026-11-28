"""
E-Waste AI — ERP Core Repository & Service Layer (Modules 1, 2, 3, 4, 11, 12)
==============================================================================
Handles Company & Branch hierarchies, Staff/RBAC, Suppliers & Procurement,
Customers & Sales, Transport & Logistics, and Machines & Production.
All operations enforce company/branch ownership and record audit trails.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Optional

from sqlalchemy.orm import Session

from backend.models.erp_batches_ops import (
    DeliveryRecord,
    Driver,
    EnergyConsumptionRecord,
    Machine,
    MachineCategory,
    MachineDowntime,
    MachineOperatingLog,
    MaintenanceRecord,
    MaintenanceSchedule,
    ProductionLine,
    TransportOrder,
    TransportTripRecord,
    TransportationExpense,
    Transporter,
    Vehicle,
    Workstation,
)
from backend.models.erp_org_staff import (
    BusinessUnit,
    Company,
    CompanyAddress,
    CompanyBranch,
    CompanyContact,
    CompanyDocument,
    CompanyLicense,
    CompanySetting,
    Department,
    Employee,
    EmployeeAttendance,
    EmployeeDepartment,
    EmployeeDesignation,
    EmployeePermission,
    EmployeeRole,
    EmployeeShift,
    EmployeeTrainingRecord,
    FinancialYear,
)
from backend.models.erp_partners import (
    Customer,
    CustomerContact,
    CustomerDocument,
    ProcurementOrder,
    ProcurementOrderItem,
    PurchaseReturn,
    Quotation,
    SalesInvoice,
    SalesOrder,
    SalesOrderItem,
    SalesPayment,
    SalesReturn,
    Supplier,
    SupplierContact,
    SupplierDocument,
    SupplierInvoice,
    SupplierMaterialCategory,
    SupplierPayment,
)
from backend.services.erp_security import record_erp_audit


class CompanyService:
    """Module 1: Multi-company, multi-branch & organization administration."""

    def create_company(self, db: Session, data: dict[str, Any], actor_id: Optional[str] = None) -> Company:
        obj = Company(**data, created_by=actor_id)
        db.add(obj)
        db.flush()
        record_erp_audit(db, "CREATE", "company", "companies", obj.id, company_id=obj.id, user_id=actor_id, after_state={"company_code": obj.company_code})
        db.commit()
        db.refresh(obj)
        return obj

    def list_companies(self, db: Session, company_id: Optional[str] = None) -> list[Company]:
        q = db.query(Company).filter(Company.is_deleted == False)  # noqa: E712
        if company_id:
            q = q.filter(Company.id == company_id)
        return q.order_by(Company.created_at.desc()).all()

    def create_branch(self, db: Session, data: dict[str, Any], actor_id: Optional[str] = None) -> CompanyBranch:
        obj = CompanyBranch(**data, created_by=actor_id)
        db.add(obj)
        db.flush()
        record_erp_audit(db, "CREATE", "company", "company_branches", obj.id, company_id=obj.company_id, branch_id=obj.id, user_id=actor_id, after_state={"branch_code": obj.branch_code})
        db.commit()
        db.refresh(obj)
        return obj

    def list_branches(self, db: Session, company_id: str) -> list[CompanyBranch]:
        return (
            db.query(CompanyBranch)
            .filter(CompanyBranch.company_id == company_id, CompanyBranch.is_deleted == False)  # noqa: E712
            .all()
        )

    def create_department(self, db: Session, data: dict[str, Any], actor_id: Optional[str] = None) -> Department:
        obj = Department(**data, created_by=actor_id)
        db.add(obj)
        db.flush()
        record_erp_audit(db, "CREATE", "company", "departments", obj.id, company_id=obj.company_id, branch_id=obj.branch_id, user_id=actor_id)
        db.commit()
        db.refresh(obj)
        return obj

    def add_company_subrecord(self, db: Session, model_cls, data: dict[str, Any], actor_id: Optional[str] = None):
        obj = model_cls(**data, created_by=actor_id)
        db.add(obj)
        db.flush()
        record_erp_audit(db, "CREATE", "company", model_cls.__tablename__, obj.id, company_id=getattr(obj, "company_id", None), branch_id=getattr(obj, "branch_id", None), user_id=actor_id)
        db.commit()
        db.refresh(obj)
        return obj


class EmployeeService:
    """Module 2: Employees, roles, departments, shifts, attendance & training."""

    def create_role(self, db: Session, data: dict[str, Any], actor_id: Optional[str] = None) -> EmployeeRole:
        role = EmployeeRole(**data, created_by=actor_id)
        db.add(role)
        db.flush()
        record_erp_audit(db, "CREATE", "employee", "employee_roles", role.id, company_id=role.company_id, user_id=actor_id)
        db.commit()
        db.refresh(role)
        return role

    def grant_permission(self, db: Session, data: dict[str, Any], actor_id: Optional[str] = None) -> EmployeePermission:
        perm = EmployeePermission(**data, created_by=actor_id)
        db.add(perm)
        db.flush()
        record_erp_audit(db, "CREATE", "employee", "employee_permissions", perm.id, company_id=perm.company_id, user_id=actor_id, after_state={"permission_key": perm.permission_key})
        db.commit()
        db.refresh(perm)
        return perm

    def create_employee(self, db: Session, data: dict[str, Any], actor_id: Optional[str] = None) -> Employee:
        emp = Employee(**data, created_by=actor_id)
        db.add(emp)
        db.flush()
        if emp.department_id:
            db.add(
                EmployeeDepartment(
                    company_id=emp.company_id,
                    branch_id=emp.branch_id,
                    employee_id=emp.id,
                    department_id=emp.department_id,
                    effective_from=emp.joining_date,
                    is_primary=True,
                    created_by=actor_id,
                )
            )
        record_erp_audit(db, "CREATE", "employee", "employees", emp.id, company_id=emp.company_id, branch_id=emp.branch_id, user_id=actor_id, employee_id=emp.id)
        db.commit()
        db.refresh(emp)
        return emp

    def list_employees(self, db: Session, company_id: str, branch_id: Optional[str] = None) -> list[Employee]:
        q = db.query(Employee).filter(Employee.company_id == company_id, Employee.is_deleted == False)  # noqa: E712
        if branch_id:
            q = q.filter(Employee.branch_id == branch_id)
        return q.order_by(Employee.employee_code).all()

    def record_attendance(self, db: Session, data: dict[str, Any], actor_id: Optional[str] = None) -> EmployeeAttendance:
        att = EmployeeAttendance(**data, created_by=actor_id)
        db.add(att)
        db.flush()
        record_erp_audit(db, "CREATE", "employee", "employee_attendance", att.id, company_id=att.company_id, branch_id=att.branch_id, employee_id=att.employee_id, user_id=actor_id)
        db.commit()
        db.refresh(att)
        return att


class ProcurementService:
    """Module 3: Suppliers, purchase orders, supplier invoices & payments."""

    def create_supplier(self, db: Session, data: dict[str, Any], actor_id: Optional[str] = None) -> Supplier:
        sup = Supplier(**data, created_by=actor_id)
        db.add(sup)
        db.flush()
        record_erp_audit(db, "CREATE", "procurement", "suppliers", sup.id, company_id=sup.company_id, branch_id=sup.branch_id, user_id=actor_id)
        db.commit()
        db.refresh(sup)
        return sup

    def list_suppliers(self, db: Session, company_id: str) -> list[Supplier]:
        return db.query(Supplier).filter(Supplier.company_id == company_id, Supplier.is_deleted == False).all()  # noqa: E712

    def create_procurement_order(
        self,
        db: Session,
        order_data: dict[str, Any],
        items: list[dict[str, Any]] | None = None,
        actor_id: Optional[str] = None,
    ) -> ProcurementOrder:
        po = ProcurementOrder(**order_data, created_by=actor_id)
        db.add(po)
        db.flush()
        total_wt = 0.0
        total_qty = 0.0
        total_price = 0.0
        for item in (items or []):
            qty = float(item.get("quantity", 0.0))
            wt = float(item.get("weight_kg", 0.0))
            unit_p = float(item.get("unit_price", 0.0))
            line_tot = float(item.get("line_total", qty * unit_p))
            total_qty += qty
            total_wt += wt
            total_price += line_tot
            db.add(
                ProcurementOrderItem(
                    company_id=po.company_id,
                    procurement_order_id=po.id,
                    ewaste_category=item.get("ewaste_category", po.ewaste_category),
                    item_description=item.get("item_description"),
                    quantity=qty,
                    weight_kg=wt,
                    unit_price=unit_p,
                    line_total=line_tot,
                    created_by=actor_id,
                )
            )
        if items:
            po.total_quantity = total_qty
            po.total_weight_kg = total_wt
            po.purchase_price_total = total_price
        record_erp_audit(db, "CREATE", "procurement", "procurement_orders", po.id, company_id=po.company_id, branch_id=po.branch_id, user_id=actor_id, after_state={"po_number": po.po_number})
        db.commit()
        db.refresh(po)
        return po

    def create_supplier_invoice_and_payment(
        self,
        db: Session,
        invoice_data: dict[str, Any],
        payment_amount: float = 0.0,
        actor_id: Optional[str] = None,
    ) -> SupplierInvoice:
        inv = SupplierInvoice(**invoice_data, created_by=actor_id)
        if payment_amount > 0:
            inv.paid_amount = payment_amount
            inv.payment_status = "paid" if payment_amount >= inv.total_amount else "partial"
        db.add(inv)
        db.flush()
        if payment_amount > 0:
            db.add(
                SupplierPayment(
                    company_id=inv.company_id,
                    branch_id=inv.branch_id,
                    supplier_id=inv.supplier_id,
                    supplier_invoice_id=inv.id,
                    payment_reference=f"SPAY-{inv.invoice_number}",
                    payment_date=inv.invoice_date,
                    amount=payment_amount,
                    created_by=actor_id,
                )
            )
        record_erp_audit(db, "CREATE", "procurement", "supplier_invoices", inv.id, company_id=inv.company_id, branch_id=inv.branch_id, user_id=actor_id)
        db.commit()
        db.refresh(inv)
        return inv


class SalesService:
    """Module 4: Customers, quotations, sales orders, invoices & receipts."""

    def create_customer(self, db: Session, data: dict[str, Any], actor_id: Optional[str] = None) -> Customer:
        cust = Customer(**data, created_by=actor_id)
        db.add(cust)
        db.flush()
        record_erp_audit(db, "CREATE", "sales", "customers", cust.id, company_id=cust.company_id, branch_id=cust.branch_id, user_id=actor_id)
        db.commit()
        db.refresh(cust)
        return cust

    def list_customers(self, db: Session, company_id: str) -> list[Customer]:
        return db.query(Customer).filter(Customer.company_id == company_id, Customer.is_deleted == False).all()  # noqa: E712

    def create_sales_order(
        self,
        db: Session,
        order_data: dict[str, Any],
        items: list[dict[str, Any]] | None = None,
        actor_id: Optional[str] = None,
    ) -> SalesOrder:
        so = SalesOrder(**order_data, created_by=actor_id)
        db.add(so)
        db.flush()
        subtotal = 0.0
        tax_tot = 0.0
        for item in (items or []):
            qty = float(item["quantity_kg"])
            price = float(item["unit_price"])
            rate = float(item.get("tax_rate_pct", 0.0))
            base = qty * price
            tax = round(base * rate / 100.0, 2)
            line_tot = round(base + tax, 2)
            subtotal += base
            tax_tot += tax
            db.add(
                SalesOrderItem(
                    company_id=so.company_id,
                    sales_order_id=so.id,
                    recovered_material_name=item["recovered_material_name"],
                    inventory_item_id=item.get("inventory_item_id"),
                    quantity_kg=qty,
                    unit_price=price,
                    tax_rate_pct=rate,
                    tax_amount=tax,
                    line_total=line_tot,
                    created_by=actor_id,
                )
            )
        if items:
            so.subtotal_amount = round(subtotal, 2)
            so.tax_amount = round(tax_tot, 2)
            so.total_amount = round(subtotal + tax_tot, 2)
        record_erp_audit(db, "CREATE", "sales", "sales_orders", so.id, company_id=so.company_id, branch_id=so.branch_id, user_id=actor_id, after_state={"so_number": so.so_number})
        db.commit()
        db.refresh(so)
        return so


class LogisticsAndMachineService:
    """Modules 11 & 12: Logistics fleet/trips & production machines/energy/maintenance."""

    def create_machine(self, db: Session, data: dict[str, Any], actor_id: Optional[str] = None) -> Machine:
        m = Machine(**data, created_by=actor_id)
        db.add(m)
        db.flush()
        record_erp_audit(db, "CREATE", "machine", "machines", m.id, company_id=m.company_id, branch_id=m.branch_id, user_id=actor_id)
        db.commit()
        db.refresh(m)
        return m

    def log_machine_operation(
        self,
        db: Session,
        company_id: str,
        branch_id: str,
        machine_id: str,
        operating_hours: float,
        output_kg: float,
        kwh_consumed: float = 0.0,
        energy_cost: float = 0.0,
        log_date: Optional[date] = None,
        actor_id: Optional[str] = None,
    ) -> MachineOperatingLog:
        op_date = log_date or date.today()
        log = MachineOperatingLog(
            company_id=company_id,
            branch_id=branch_id,
            machine_id=machine_id,
            log_date=op_date,
            operating_hours=operating_hours,
            output_kg=output_kg,
            created_by=actor_id,
        )
        db.add(log)
        if kwh_consumed > 0:
            db.add(
                EnergyConsumptionRecord(
                    company_id=company_id,
                    branch_id=branch_id,
                    machine_id=machine_id,
                    recorded_date=op_date,
                    kwh_consumed=kwh_consumed,
                    energy_cost=energy_cost,
                    created_by=actor_id,
                )
            )
        db.flush()
        record_erp_audit(db, "CREATE", "machine", "machine_operating_logs", log.id, company_id=company_id, branch_id=branch_id, user_id=actor_id)
        db.commit()
        db.refresh(log)
        return log

    def create_transport_order(self, db: Session, data: dict[str, Any], actor_id: Optional[str] = None) -> TransportOrder:
        to = TransportOrder(**data, created_by=actor_id)
        db.add(to)
        db.flush()
        record_erp_audit(db, "CREATE", "logistics", "transport_orders", to.id, company_id=to.company_id, branch_id=to.branch_id, user_id=actor_id)
        db.commit()
        db.refresh(to)
        return to
