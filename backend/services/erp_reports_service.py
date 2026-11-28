"""
E-Waste AI — Industrial ERP Reporting Engine (15 Real Database Reports)
=======================================================================
Generates all 15 requested company database reports strictly from live
company/branch-scoped database records. Never fabricates business numbers;
financial and environmental summaries include clear non-certification notices.
"""

from __future__ import annotations

from datetime import date
from typing import Any, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.models.all_models import AIPrediction, EnvironmentalReport
from backend.models.erp_batches_ops import (
    IncomingBatch,
    Machine,
    MachineDowntime,
    MachineOperatingLog,
    ProcessingJob,
)
from backend.models.erp_finance_env_ai_audit import (
    AIPredictionFeedback,
    Expense,
    HazardousWasteMovement,
    IncomeRecord,
    JournalEntry,
)
from backend.models.erp_org_staff import CompanyBranch, Employee, EmployeeActivityLog
from backend.models.erp_partners import (
    Customer,
    ProcurementOrder,
    SalesOrder,
    SalesOrderItem,
    Supplier,
)
from backend.models.erp_recovery_inv import (
    ERPInventoryItem,
    HazardousMaterialRecord,
    InventoryStock,
    MaterialLossRecord,
    MaterialType,
    RecoveredMaterial,
    Warehouse,
)


class ERPReportsService:
    """All 15 production ERP database reports backed by real SQLAlchemy queries."""

    def _apply_scope(self, query, model, company_id: str, branch_id: Optional[str]):
        query = query.filter(model.company_id == company_id, model.is_deleted == False)  # noqa: E712
        if branch_id and hasattr(model, "branch_id"):
            query = query.filter(model.branch_id == branch_id)
        return query

    # 1. Daily incoming e-waste report
    def daily_incoming_ewaste_report(self, db: Session, company_id: str, branch_id: Optional[str] = None) -> dict[str, Any]:
        q = self._apply_scope(db.query(IncomingBatch), IncomingBatch, company_id, branch_id)
        rows = q.order_by(IncomingBatch.receiving_date.desc()).all()
        daily: dict[str, dict[str, Any]] = {}
        for b in rows:
            day = str(b.receiving_date)
            bucket = daily.setdefault(day, {"date": day, "batch_count": 0, "gross_kg": 0.0, "net_kg": 0.0, "purchase_value": 0.0})
            bucket["batch_count"] += 1
            bucket["gross_kg"] = round(bucket["gross_kg"] + (b.gross_weight_kg or 0.0), 3)
            bucket["net_kg"] = round(bucket["net_kg"] + (b.net_weight_kg or 0.0), 3)
            bucket["purchase_value"] = round(bucket["purchase_value"] + (b.purchase_value or 0.0), 2)
        return {"report": "daily_incoming_ewaste", "rows": list(daily.values()), "total_batches": len(rows)}

    # 2. Supplier-wise purchase report
    def supplier_purchase_report(self, db: Session, company_id: str, branch_id: Optional[str] = None) -> dict[str, Any]:
        q = self._apply_scope(db.query(ProcurementOrder), ProcurementOrder, company_id, branch_id)
        orders = q.all()
        sup_map = {s.id: s.name for s in db.query(Supplier).filter(Supplier.company_id == company_id).all()}
        agg: dict[str, dict[str, Any]] = {}
        for o in orders:
            entry = agg.setdefault(o.supplier_id, {
                "supplier_id": o.supplier_id, "supplier_name": sup_map.get(o.supplier_id, "Unknown"),
                "orders_count": 0, "total_weight_kg": 0.0, "total_purchase_value": 0.0, "transport_cost": 0.0,
            })
            entry["orders_count"] += 1
            entry["total_weight_kg"] = round(entry["total_weight_kg"] + (o.total_weight_kg or 0.0), 3)
            entry["total_purchase_value"] = round(entry["total_purchase_value"] + (o.purchase_price_total or 0.0), 2)
            entry["transport_cost"] = round(entry["transport_cost"] + (o.transportation_cost or 0.0), 2)
        return {"report": "supplier_wise_purchase", "rows": list(agg.values())}

    # 3. Batch processing report
    def batch_processing_report(self, db: Session, company_id: str, branch_id: Optional[str] = None) -> dict[str, Any]:
        jobs = self._apply_scope(db.query(ProcessingJob), ProcessingJob, company_id, branch_id).all()
        rows = [
            {
                "job_number": j.job_number, "incoming_batch_id": j.incoming_batch_id,
                "process_type": j.process_type, "status": j.status,
                "input_weight_kg": j.input_weight_kg, "output_weight_kg": j.output_weight_kg,
                "rejected_quantity_kg": j.rejected_quantity_kg,
            }
            for j in jobs
        ]
        return {"report": "batch_processing", "rows": rows, "total_jobs": len(rows)}

    # 4. Material recovery report
    def material_recovery_report(self, db: Session, company_id: str, branch_id: Optional[str] = None) -> dict[str, Any]:
        recs = self._apply_scope(db.query(RecoveredMaterial), RecoveredMaterial, company_id, branch_id).all()
        losses = self._apply_scope(db.query(MaterialLossRecord), MaterialLossRecord, company_id, branch_id).all()
        mat_map = {m.id: m.material_name for m in db.query(MaterialType).filter(MaterialType.company_id == company_id).all()}
        rows = [
            {
                "incoming_batch_id": r.incoming_batch_id,
                "material_name": mat_map.get(r.material_type_id, r.material_type_id),
                "measured_weight_kg": r.measured_weight_kg,
                "predicted_weight_kg": r.predicted_weight_kg,
                "estimated_weight_kg": r.estimated_weight_kg,
                "quality_grade": r.quality_grade,
                "recovery_date": str(r.recovery_date),
            }
            for r in recs
        ]
        return {
            "report": "material_recovery",
            "rows": rows,
            "total_measured_kg": round(sum(r.measured_weight_kg or 0.0 for r in recs), 3),
            "total_loss_kg": round(sum(l.loss_weight_kg or 0.0 for l in losses), 3),
        }

    # 5. Warehouse stock report
    def warehouse_stock_report(self, db: Session, company_id: str, branch_id: Optional[str] = None) -> dict[str, Any]:
        stocks = self._apply_scope(db.query(InventoryStock), InventoryStock, company_id, branch_id).all()
        wh_map = {w.id: w.warehouse_name for w in db.query(Warehouse).filter(Warehouse.company_id == company_id).all()}
        item_map = {i.id: (i.item_name, i.min_stock_kg) for i in db.query(ERPInventoryItem).filter(ERPInventoryItem.company_id == company_id).all()}
        rows = []
        for s in stocks:
            iname, min_kg = item_map.get(s.inventory_item_id, (s.inventory_item_id, 0.0))
            rows.append({
                "warehouse": wh_map.get(s.warehouse_id, s.warehouse_id),
                "item": iname,
                "opening_kg": s.opening_stock_kg,
                "received_kg": s.received_stock_kg,
                "issued_kg": s.issued_stock_kg,
                "sold_kg": s.sold_stock_kg,
                "closing_kg": s.closing_stock_kg,
                "below_min_alert": s.closing_stock_kg < min_kg,
            })
        return {"report": "warehouse_stock", "rows": rows, "total_closing_kg": round(sum(r["closing_kg"] for r in rows), 3)}

    # 6. Material sales report
    def material_sales_report(self, db: Session, company_id: str, branch_id: Optional[str] = None) -> dict[str, Any]:
        orders = self._apply_scope(db.query(SalesOrder), SalesOrder, company_id, branch_id).all()
        so_ids = {o.id for o in orders}
        items = db.query(SalesOrderItem).filter(SalesOrderItem.company_id == company_id).all() if so_ids else []
        by_mat: dict[str, dict[str, Any]] = {}
        for it in items:
            if it.sales_order_id not in so_ids:
                continue
            m = by_mat.setdefault(it.recovered_material_name, {"material": it.recovered_material_name, "quantity_kg": 0.0, "revenue_total": 0.0})
            m["quantity_kg"] = round(m["quantity_kg"] + (it.quantity_kg or 0.0), 3)
            m["revenue_total"] = round(m["revenue_total"] + (it.line_total or 0.0), 2)
        return {"report": "material_sales", "rows": list(by_mat.values())}

    # 7. Customer-wise sales report
    def customer_sales_report(self, db: Session, company_id: str, branch_id: Optional[str] = None) -> dict[str, Any]:
        orders = self._apply_scope(db.query(SalesOrder), SalesOrder, company_id, branch_id).all()
        cust_map = {c.id: c.name for c in db.query(Customer).filter(Customer.company_id == company_id).all()}
        agg: dict[str, dict[str, Any]] = {}
        for o in orders:
            e = agg.setdefault(o.customer_id, {"customer_id": o.customer_id, "customer_name": cust_map.get(o.customer_id, "Unknown"), "orders_count": 0, "total_sales": 0.0})
            e["orders_count"] += 1
            e["total_sales"] = round(e["total_sales"] + (o.total_amount or 0.0), 2)
        return {"report": "customer_wise_sales", "rows": list(agg.values())}

    # 8. Purchase and expense report
    def purchase_and_expense_report(self, db: Session, company_id: str, branch_id: Optional[str] = None) -> dict[str, Any]:
        pos = self._apply_scope(db.query(ProcurementOrder), ProcurementOrder, company_id, branch_id).all()
        exps = self._apply_scope(db.query(Expense), Expense, company_id, branch_id).all()
        po_tot = round(sum((p.purchase_price_total or 0.0) + (p.transportation_cost or 0.0) for p in pos), 2)
        exp_tot = round(sum(e.amount or 0.0 for e in exps), 2)
        return {
            "report": "purchase_and_expense",
            "procurement_orders_count": len(pos),
            "procurement_total": po_tot,
            "operating_expenses_count": len(exps),
            "operating_expenses_total": exp_tot,
            "combined_outflow": round(po_tot + exp_tot, 2),
        }

    # 9. Profit and loss summary (explicit operational disclaimer)
    def profit_and_loss_summary(self, db: Session, company_id: str, branch_id: Optional[str] = None) -> dict[str, Any]:
        incomes = self._apply_scope(db.query(IncomeRecord), IncomeRecord, company_id, branch_id).all()
        sales_orders = self._apply_scope(db.query(SalesOrder), SalesOrder, company_id, branch_id).all()
        outflows = self.purchase_and_expense_report(db, company_id, branch_id)
        income_rev = sum(i.amount or 0.0 for i in incomes)
        sales_rev = sum(s.total_amount or 0.0 for s in sales_orders)
        total_revenue = round(income_rev if income_rev > 0 else sales_rev, 2)
        net_pl = round(total_revenue - outflows["combined_outflow"], 2)
        return {
            "report": "profit_and_loss_summary",
            "total_revenue": total_revenue,
            "procurement_cost": outflows["procurement_total"],
            "operating_expenses": outflows["operating_expenses_total"],
            "net_operational_surplus": net_pl,
            "is_audited_statement": False,
            "disclaimer": "Operational database ledger summary only — NOT an audited statutory financial statement.",
        }

    # 10. Machine utilization report
    def machine_utilization_report(self, db: Session, company_id: str, branch_id: Optional[str] = None) -> dict[str, Any]:
        machines = self._apply_scope(db.query(Machine), Machine, company_id, branch_id).all()
        logs = self._apply_scope(db.query(MachineOperatingLog), MachineOperatingLog, company_id, branch_id).all()
        dts = self._apply_scope(db.query(MachineDowntime), MachineDowntime, company_id, branch_id).all()
        rows = []
        for m in machines:
            op_h = sum(l.operating_hours or 0.0 for l in logs if l.machine_id == m.id)
            out_kg = sum(l.output_kg or 0.0 for l in logs if l.machine_id == m.id)
            dt_h = sum(d.downtime_hours or 0.0 for d in dts if d.machine_id == m.id)
            util = round((op_h / (op_h + dt_h) * 100.0) if (op_h + dt_h) > 0 else 0.0, 2)
            rows.append({"machine_code": m.machine_code, "machine_name": m.machine_name, "operating_hours": op_h, "downtime_hours": dt_h, "utilization_pct": util, "output_kg": out_kg})
        return {"report": "machine_utilization", "rows": rows}

    # 11. Employee activity report
    def employee_activity_report(self, db: Session, company_id: str, branch_id: Optional[str] = None) -> dict[str, Any]:
        emps = self._apply_scope(db.query(Employee), Employee, company_id, branch_id).all()
        logs = self._apply_scope(db.query(EmployeeActivityLog), EmployeeActivityLog, company_id, branch_id).all()
        emp_map = {e.id: e.full_name for e in emps}
        counts: dict[str, int] = {}
        for l in logs:
            counts[l.employee_id] = counts.get(l.employee_id, 0) + 1
        rows = [{"employee_id": eid, "full_name": emp_map.get(eid, eid), "activity_count": cnt} for eid, cnt in counts.items()]
        return {"report": "employee_activity", "total_employees": len(emps), "total_events": len(logs), "rows": rows}

    # 12. Hazardous waste tracking report
    def hazardous_waste_tracking_report(self, db: Session, company_id: str, branch_id: Optional[str] = None) -> dict[str, Any]:
        records = self._apply_scope(db.query(HazardousMaterialRecord), HazardousMaterialRecord, company_id, branch_id).all()
        moves = self._apply_scope(db.query(HazardousWasteMovement), HazardousWasteMovement, company_id, branch_id).all()
        return {
            "report": "hazardous_waste_tracking",
            "identified_records_count": len(records),
            "identified_weight_kg": round(sum(r.quantity_kg or 0.0 for r in records), 3),
            "dispatched_movements_count": len(moves),
            "dispatched_weight_kg": round(sum(m.quantity_kg or 0.0 for m in moves), 3),
        }

    # 13. Environmental records report
    def environmental_records_report(self, db: Session, company_id: str, branch_id: Optional[str] = None) -> dict[str, Any]:
        q = db.query(EnvironmentalReport).filter(EnvironmentalReport.company_id == company_id, EnvironmentalReport.is_deleted == False)  # noqa: E712
        if branch_id:
            q = q.filter(EnvironmentalReport.branch_id == branch_id)
        reps = q.all()
        return {
            "report": "environmental_records",
            "records_count": len(reps),
            "total_waste_kg": round(sum(r.total_waste_kg or 0.0 for r in reps), 3),
            "total_recovered_kg": round(sum(r.total_recovered_kg or 0.0 for r in reps), 3),
            "is_certified": False,
            "disclaimer": "Internal operational records summary — does NOT represent legal regulatory certification.",
        }

    # 14. AI prediction performance report
    def ai_prediction_performance_report(self, db: Session, company_id: str, branch_id: Optional[str] = None) -> dict[str, Any]:
        preds = db.query(AIPrediction).filter(AIPrediction.company_id == company_id).all()
        fbs = self._apply_scope(db.query(AIPredictionFeedback), AIPredictionFeedback, company_id, branch_id).all()
        evaluated = [f for f in fbs if f.is_accurate is not None]
        acc = round(sum(1 for f in evaluated if f.is_accurate) / len(evaluated), 4) if evaluated else None
        return {
            "report": "ai_prediction_performance",
            "total_predictions": len(preds),
            "human_verified_count": len(fbs),
            "verified_accuracy": acc,
        }

    # 15. Branch-wise business performance report
    def branch_business_performance_report(self, db: Session, company_id: str) -> dict[str, Any]:
        branches = db.query(CompanyBranch).filter(CompanyBranch.company_id == company_id, CompanyBranch.is_deleted == False).all()  # noqa: E712
        rows = []
        for b in branches:
            inc_cnt = db.query(IncomingBatch).filter(IncomingBatch.company_id == company_id, IncomingBatch.branch_id == b.id).count()
            rec_kg = db.query(func.sum(RecoveredMaterial.measured_weight_kg)).filter(RecoveredMaterial.company_id == company_id, RecoveredMaterial.branch_id == b.id).scalar() or 0.0
            sales_tot = db.query(func.sum(SalesOrder.total_amount)).filter(SalesOrder.company_id == company_id, SalesOrder.branch_id == b.id).scalar() or 0.0
            rows.append({
                "branch_code": b.branch_code, "branch_name": b.branch_name,
                "incoming_batches": inc_cnt, "measured_recovered_kg": round(rec_kg, 3),
                "sales_total": round(sales_tot, 2),
            })
        return {"report": "branch_business_performance", "rows": rows}

    def generate_by_number(self, db: Session, report_num: int, company_id: str, branch_id: Optional[str] = None) -> dict[str, Any]:
        dispatch = {
            1: lambda: self.daily_incoming_ewaste_report(db, company_id, branch_id),
            2: lambda: self.supplier_purchase_report(db, company_id, branch_id),
            3: lambda: self.batch_processing_report(db, company_id, branch_id),
            4: lambda: self.material_recovery_report(db, company_id, branch_id),
            5: lambda: self.warehouse_stock_report(db, company_id, branch_id),
            6: lambda: self.material_sales_report(db, company_id, branch_id),
            7: lambda: self.customer_sales_report(db, company_id, branch_id),
            8: lambda: self.purchase_and_expense_report(db, company_id, branch_id),
            9: lambda: self.profit_and_loss_summary(db, company_id, branch_id),
            10: lambda: self.machine_utilization_report(db, company_id, branch_id),
            11: lambda: self.employee_activity_report(db, company_id, branch_id),
            12: lambda: self.hazardous_waste_tracking_report(db, company_id, branch_id),
            13: lambda: self.environmental_records_report(db, company_id, branch_id),
            14: lambda: self.ai_prediction_performance_report(db, company_id, branch_id),
            15: lambda: self.branch_business_performance_report(db, company_id),
        }
        fn = dispatch.get(report_num)
        if not fn:
            raise ValueError(f"Unsupported report number {report_num}; expected 1..15")
        return fn()
