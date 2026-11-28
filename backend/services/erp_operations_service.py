"""
E-Waste AI — ERP Operational, Recovery, Warehouse & Ledger Services
=====================================================================
Modules 5, 6, 7, 8, 9, 10, 13, 14, 15 business logic with transactional safety,
strict measured vs estimated separation, and double-entry debit==credit guards.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Optional

from sqlalchemy.orm import Session

from backend.models.all_models import AIPrediction
from backend.models.erp_batches_ops import (
    BatchItem,
    BatchStatusHistory,
    DismantlingOperation,
    IncomingBatch,
    IncomingInspection,
    MaterialReceivingRecord,
    ProcessingJob,
    QualityInspection,
    SortingOperation,
    WeighbridgeRecord,
)
from backend.models.erp_finance_env_ai_audit import (
    AIPredictionFeedback,
    AccountingVoucher,
    ChartOfAccount,
    ComplianceDocument,
    Expense,
    HazardousWasteMovement,
    IncomeRecord,
    JournalEntry,
    JournalEntryLine,
    RecoveryRecommendation,
)
from backend.models.erp_recovery_inv import (
    ComponentMaterialMapping,
    ERPInventoryItem,
    HazardousMaterialRecord,
    InventoryStock,
    InventoryTransaction,
    MaterialLossRecord,
    MaterialType,
    MaterialTransfer,
    RecoveredMaterial,
    RecoveryJob,
    RecoveryJobInput,
    RecoveryJobOutput,
    RecoveryMeasurement,
    StockAuditRecord,
    StockMovement,
    Warehouse,
)
from backend.services.erp_security import record_erp_audit


class IncomingBatchService:
    """Module 5: Incoming e-waste registration, weighbridge, inspection & traceability."""

    def register_incoming_batch(
        self,
        db: Session,
        data: dict[str, Any],
        actor_id: Optional[str] = None,
    ) -> IncomingBatch:
        gross = float(data["gross_weight_kg"])
        tare = float(data.get("tare_weight_kg", 0.0))
        if tare > gross:
            raise ValueError("Tare weight cannot exceed gross weight")
        net = round(gross - tare, 4)

        batch_num = data["batch_number"]
        qr_code = data.get("barcode_qr_code") or f"QR-{data['company_id'][:8]}-{batch_num}"
        batch = IncomingBatch(
            company_id=data["company_id"],
            branch_id=data.get("branch_id"),
            warehouse_id=data.get("warehouse_id"),
            supplier_id=data.get("supplier_id"),
            procurement_order_id=data.get("procurement_order_id"),
            responsible_employee_id=data.get("responsible_employee_id"),
            batch_number=batch_num,
            barcode_qr_code=qr_code,
            receiving_date=data.get("receiving_date", date.today()),
            ewaste_category=data["ewaste_category"],
            device_type=data.get("device_type"),
            gross_weight_kg=gross,
            tare_weight_kg=tare,
            net_weight_kg=net,
            inspection_status=data.get("inspection_status", "pending"),
            purchase_value=float(data.get("purchase_value", 0.0)),
            batch_status="received",
            notes=data.get("notes"),
            created_by=actor_id,
        )
        db.add(batch)
        db.flush()

        db.add(
            WeighbridgeRecord(
                company_id=batch.company_id,
                branch_id=batch.branch_id,
                incoming_batch_id=batch.id,
                ticket_number=f"WB-{batch.batch_number}",
                gross_weight_kg=gross,
                tare_weight_kg=tare,
                net_weight_kg=net,
                operator_employee_id=batch.responsible_employee_id,
                created_by=actor_id,
            )
        )
        db.add(
            BatchStatusHistory(
                company_id=batch.company_id,
                branch_id=batch.branch_id,
                incoming_batch_id=batch.id,
                previous_status=None,
                new_status="received",
                changed_by_employee_id=batch.responsible_employee_id,
                reason="Initial weighbridge receiving",
                created_by=actor_id,
            )
        )
        record_erp_audit(
            db, "CREATE", "incoming_batch", "incoming_batches", batch.id,
            company_id=batch.company_id, branch_id=batch.branch_id,
            user_id=actor_id, employee_id=batch.responsible_employee_id,
            after_state={"batch_number": batch.batch_number, "net_weight_kg": net},
        )
        db.commit()
        db.refresh(batch)
        return batch

    def transition_batch_status(
        self,
        db: Session,
        batch_id: str,
        new_status: str,
        employee_id: Optional[str] = None,
        reason: str = "",
        actor_id: Optional[str] = None,
    ) -> IncomingBatch:
        batch = db.query(IncomingBatch).filter(IncomingBatch.id == batch_id).first()
        if not batch:
            raise ValueError("IncomingBatch not found")
        prev = batch.batch_status
        batch.batch_status = new_status
        batch.updated_by = actor_id
        db.add(
            BatchStatusHistory(
                company_id=batch.company_id,
                branch_id=batch.branch_id,
                incoming_batch_id=batch.id,
                previous_status=prev,
                new_status=new_status,
                changed_by_employee_id=employee_id,
                reason=reason,
                created_by=actor_id,
            )
        )
        record_erp_audit(
            db, "STATUS_CHANGE", "incoming_batch", "incoming_batches", batch.id,
            company_id=batch.company_id, branch_id=batch.branch_id,
            user_id=actor_id, employee_id=employee_id,
            before_state={"batch_status": prev}, after_state={"batch_status": new_status},
        )
        db.commit()
        db.refresh(batch)
        return batch


class ProcessingAndRecoveryService:
    """Modules 6, 7 & 8: Authorized sorting, dismantling, processing, material recovery & QA."""

    def record_processing_job(self, db: Session, data: dict[str, Any], actor_id: Optional[str] = None) -> ProcessingJob:
        job = ProcessingJob(**data, created_by=actor_id)
        db.add(job)
        db.flush()
        record_erp_audit(
            db, "CREATE", "processing", "processing_jobs", job.id,
            company_id=job.company_id, branch_id=job.branch_id,
            user_id=actor_id, employee_id=job.operator_employee_id,
        )
        db.commit()
        db.refresh(job)
        return job

    def map_component_material_estimate(
        self,
        db: Session,
        company_id: str,
        material_type_id: str,
        estimated_pct: float,
        source_id: Optional[str] = None,
        component_category_id: Optional[str] = None,
        verification_status: str = "unverified",
        confidence_score: Optional[float] = None,
        actor_id: Optional[str] = None,
    ) -> ComponentMaterialMapping:
        # Enforces guard: component composition estimates are NEVER marked as measured recovery
        rec = ComponentMaterialMapping(
            company_id=company_id,
            component_category_id=component_category_id,
            material_type_id=material_type_id,
            source_id=source_id,
            estimated_pct=estimated_pct,
            verification_status=verification_status,
            confidence_score=confidence_score,
            is_measured_recovery=False,
            created_by=actor_id,
        )
        db.add(rec)
        db.commit()
        db.refresh(rec)
        return rec

    def record_recovery_job_and_output(
        self,
        db: Session,
        job_data: dict[str, Any],
        material_type_id: str,
        measured_weight_kg: float,
        predicted_weight_kg: Optional[float] = None,
        estimated_weight_kg: Optional[float] = None,
        quality_grade: str = "A",
        final_destination: str = "warehouse",
        actor_id: Optional[str] = None,
    ) -> RecoveredMaterial:
        if measured_weight_kg < 0:
            raise ValueError("Measured recovered weight cannot be negative")
        job = RecoveryJob(**job_data, created_by=actor_id)
        db.add(job)
        db.flush()

        db.add(
            RecoveryJobOutput(
                company_id=job.company_id,
                recovery_job_id=job.id,
                material_type_id=material_type_id,
                output_weight_kg=measured_weight_kg,
                measurement_type="measured",
                quality_grade=quality_grade,
                destination=final_destination,
                created_by=actor_id,
            )
        )
        db.add(
            RecoveryMeasurement(
                company_id=job.company_id,
                branch_id=job.branch_id,
                recovery_job_id=job.id,
                material_type_id=material_type_id,
                measurement_category="measured",
                weight_kg=measured_weight_kg,
                measured_by_employee_id=job.responsible_employee_id,
                created_by=actor_id,
            )
        )
        rec = RecoveredMaterial(
            company_id=job.company_id,
            branch_id=job.branch_id,
            incoming_batch_id=job.incoming_batch_id,
            recovery_job_id=job.id,
            material_type_id=material_type_id,
            measured_weight_kg=measured_weight_kg,
            predicted_weight_kg=predicted_weight_kg,
            estimated_weight_kg=estimated_weight_kg,
            quality_grade=quality_grade,
            recovery_date=job.recovery_date,
            responsible_employee_id=job.responsible_employee_id,
            final_destination=final_destination,
            created_by=actor_id,
        )
        db.add(rec)
        db.flush()
        record_erp_audit(
            db, "CREATE", "recovery", "recovered_materials", rec.id,
            company_id=job.company_id, branch_id=job.branch_id,
            user_id=actor_id, employee_id=job.responsible_employee_id,
            after_state={"measured_weight_kg": measured_weight_kg, "predicted_weight_kg": predicted_weight_kg},
        )
        db.commit()
        db.refresh(rec)
        return rec


class WarehouseInventoryService:
    """Module 9: Transactional warehouse stock ledger blocking inconsistent/negative balances."""

    def apply_stock_transaction(
        self,
        db: Session,
        company_id: str,
        branch_id: str,
        warehouse_id: str,
        inventory_item_id: str,
        txn_type: str,
        quantity_kg: float,
        incoming_batch_id: Optional[str] = None,
        reference_type: Optional[str] = None,
        reference_id: Optional[str] = None,
        employee_id: Optional[str] = None,
        actor_id: Optional[str] = None,
        auto_commit: bool = True,
    ) -> InventoryStock:
        valid_types = {"OPENING", "RECEIVE", "ISSUE", "SALE", "TRANSFER_IN", "TRANSFER_OUT", "ADJUST"}
        t = txn_type.upper()
        if t not in valid_types:
            raise ValueError(f"Unsupported inventory transaction type: {txn_type}")
        if t != "ADJUST" and quantity_kg <= 0:
            raise ValueError("Transaction quantity must be strictly positive")

        try:
            q = db.query(InventoryStock).filter(
                InventoryStock.company_id == company_id,
                InventoryStock.warehouse_id == warehouse_id,
                InventoryStock.inventory_item_id == inventory_item_id,
            )
            if incoming_batch_id:
                q = q.filter(InventoryStock.incoming_batch_id == incoming_batch_id)
            else:
                q = q.filter(InventoryStock.incoming_batch_id.is_(None))
            stock = q.first()

            if stock is None:
                stock = InventoryStock(
                    company_id=company_id,
                    branch_id=branch_id,
                    warehouse_id=warehouse_id,
                    inventory_item_id=inventory_item_id,
                    incoming_batch_id=incoming_batch_id,
                    opening_stock_kg=0.0,
                    received_stock_kg=0.0,
                    issued_stock_kg=0.0,
                    sold_stock_kg=0.0,
                    closing_stock_kg=0.0,
                    reserved_stock_kg=0.0,
                    created_by=actor_id,
                )
                db.add(stock)
                db.flush()

            new_closing = stock.closing_stock_kg
            if t == "OPENING":
                stock.opening_stock_kg = round(stock.opening_stock_kg + quantity_kg, 4)
                new_closing = round(new_closing + quantity_kg, 4)
            elif t in {"RECEIVE", "TRANSFER_IN"}:
                stock.received_stock_kg = round(stock.received_stock_kg + quantity_kg, 4)
                new_closing = round(new_closing + quantity_kg, 4)
            elif t == "ISSUE":
                new_closing = round(new_closing - quantity_kg, 4)
                stock.issued_stock_kg = round(stock.issued_stock_kg + quantity_kg, 4)
            elif t == "SALE":
                new_closing = round(new_closing - quantity_kg, 4)
                stock.sold_stock_kg = round(stock.sold_stock_kg + quantity_kg, 4)
            elif t == "TRANSFER_OUT":
                new_closing = round(new_closing - quantity_kg, 4)
                stock.issued_stock_kg = round(stock.issued_stock_kg + quantity_kg, 4)
            elif t == "ADJUST":
                new_closing = round(new_closing + quantity_kg, 4)

            if new_closing < 0:
                raise ValueError(
                    f"Insufficient stock for {t}: available {stock.closing_stock_kg:.4f} kg, requested {quantity_kg:.4f} kg"
                )
            stock.closing_stock_kg = new_closing
            stock.updated_by = actor_id

            db.add(
                InventoryTransaction(
                    company_id=company_id,
                    branch_id=branch_id,
                    warehouse_id=warehouse_id,
                    inventory_item_id=inventory_item_id,
                    incoming_batch_id=incoming_batch_id,
                    txn_type=t,
                    quantity_kg=quantity_kg,
                    balance_after_kg=new_closing,
                    reference_type=reference_type,
                    reference_id=reference_id,
                    performed_by_employee_id=employee_id,
                    created_by=actor_id,
                )
            )
            record_erp_audit(
                db, f"STOCK_{t}", "warehouse", "inventory_stock", stock.id,
                company_id=company_id, branch_id=branch_id, user_id=actor_id, employee_id=employee_id,
                after_state={"closing_stock_kg": new_closing, "quantity_kg": quantity_kg},
            )
            if auto_commit:
                db.commit()
                db.refresh(stock)
            else:
                db.flush()
            return stock
        except Exception:
            if auto_commit:
                db.rollback()
            raise

    def transfer_between_branches(
        self,
        db: Session,
        company_id: str,
        from_branch_id: str,
        to_branch_id: str,
        from_warehouse_id: str,
        to_warehouse_id: str,
        inventory_item_id: str,
        quantity_kg: float,
        transfer_number: str,
        incoming_batch_id: Optional[str] = None,
        employee_id: Optional[str] = None,
        actor_id: Optional[str] = None,
    ) -> MaterialTransfer:
        try:
            self.apply_stock_transaction(
                db, company_id, from_branch_id, from_warehouse_id, inventory_item_id,
                "TRANSFER_OUT", quantity_kg, incoming_batch_id=incoming_batch_id,
                reference_type="material_transfer", reference_id=transfer_number,
                employee_id=employee_id, actor_id=actor_id, auto_commit=False,
            )
            self.apply_stock_transaction(
                db, company_id, to_branch_id, to_warehouse_id, inventory_item_id,
                "TRANSFER_IN", quantity_kg, incoming_batch_id=incoming_batch_id,
                reference_type="material_transfer", reference_id=transfer_number,
                employee_id=employee_id, actor_id=actor_id, auto_commit=False,
            )
            transfer = MaterialTransfer(
                company_id=company_id,
                from_branch_id=from_branch_id,
                to_branch_id=to_branch_id,
                from_warehouse_id=from_warehouse_id,
                to_warehouse_id=to_warehouse_id,
                inventory_item_id=inventory_item_id,
                incoming_batch_id=incoming_batch_id,
                transfer_number=transfer_number,
                quantity_kg=quantity_kg,
                status="completed",
                created_by=actor_id,
            )
            db.add(transfer)
            db.add(
                StockMovement(
                    company_id=company_id,
                    branch_id=from_branch_id,
                    inventory_item_id=inventory_item_id,
                    from_warehouse_id=from_warehouse_id,
                    to_warehouse_id=to_warehouse_id,
                    incoming_batch_id=incoming_batch_id,
                    quantity_kg=quantity_kg,
                    reference_no=transfer_number,
                    created_by=actor_id,
                )
            )
            db.commit()
            db.refresh(transfer)
            return transfer
        except Exception:
            db.rollback()
            raise


class FinanceLedgerService:
    """Module 10: Validated double-entry accounting ledger (not audited financial statements)."""

    def create_journal_entry(
        self,
        db: Session,
        company_id: str,
        branch_id: Optional[str],
        entry_number: str,
        entry_date: date,
        description: str,
        lines: list[dict[str, Any]],
        post_immediately: bool = True,
        actor_id: Optional[str] = None,
    ) -> JournalEntry:
        if not lines or len(lines) < 2:
            raise ValueError("Double-entry journal requires at least two lines")

        total_debit = round(sum(float(l.get("debit_amount", 0.0)) for l in lines), 4)
        total_credit = round(sum(float(l.get("credit_amount", 0.0)) for l in lines), 4)
        if abs(total_debit - total_credit) > 1e-4 or total_debit <= 0:
            raise ValueError(
                f"Unbalanced journal entry rejected: debit={total_debit} != credit={total_credit}"
            )

        entry = JournalEntry(
            company_id=company_id,
            branch_id=branch_id,
            entry_number=entry_number,
            entry_date=entry_date,
            description=description,
            total_debit=total_debit,
            total_credit=total_credit,
            is_balanced=True,
            is_posted=post_immediately,
            is_audited_statement=False,
            created_by=actor_id,
        )
        db.add(entry)
        db.flush()

        for l in lines:
            acc = db.query(ChartOfAccount).filter(
                ChartOfAccount.id == l["account_id"],
                ChartOfAccount.company_id == company_id,
            ).first()
            if not acc:
                raise ValueError(f"Account {l['account_id']} does not belong to company {company_id}")
            db.add(
                JournalEntryLine(
                    company_id=company_id,
                    journal_entry_id=entry.id,
                    account_id=acc.id,
                    debit_amount=round(float(l.get("debit_amount", 0.0)), 4),
                    credit_amount=round(float(l.get("credit_amount", 0.0)), 4),
                    description=l.get("description"),
                    created_by=actor_id,
                )
            )
        record_erp_audit(
            db, "POST_JOURNAL", "finance", "journal_entries", entry.id,
            company_id=company_id, branch_id=branch_id, user_id=actor_id,
            after_state={"entry_number": entry_number, "total_debit": total_debit, "total_credit": total_credit},
        )
        db.commit()
        db.refresh(entry)
        return entry


class ComplianceAIService:
    """Modules 13, 14 & 15: Compliance docs, hazardous movements, and AI feedback linking."""

    def verify_ai_prediction(
        self,
        db: Session,
        company_id: str,
        branch_id: Optional[str],
        ai_prediction_id: str,
        is_accurate: bool,
        corrected_label: Optional[str] = None,
        final_measured_outcome: Optional[dict[str, Any]] = None,
        reviewer_employee_id: Optional[str] = None,
        actor_id: Optional[str] = None,
    ) -> AIPredictionFeedback:
        pred = db.query(AIPrediction).filter(AIPrediction.id == ai_prediction_id).first()
        if not pred:
            raise ValueError("AIPrediction not found")
        pred.company_id = pred.company_id or company_id
        pred.branch_id = pred.branch_id or branch_id
        pred.human_verified = True
        pred.review_status = "verified"
        pred.verified_by = reviewer_employee_id or actor_id
        pred.verified_at = datetime.utcnow()
        pred.final_measured_outcome = final_measured_outcome

        fb = AIPredictionFeedback(
            company_id=company_id,
            branch_id=branch_id,
            ai_prediction_id=ai_prediction_id,
            reviewer_employee_id=reviewer_employee_id,
            is_accurate=is_accurate,
            corrected_label=corrected_label,
            final_measured_outcome=final_measured_outcome,
            created_by=actor_id,
        )
        db.add(fb)
        db.flush()
        record_erp_audit(
            db, "VERIFY_AI", "ai_automation", "ai_predictions", pred.id,
            company_id=company_id, branch_id=branch_id, user_id=actor_id, employee_id=reviewer_employee_id,
        )
        db.commit()
        db.refresh(fb)
        return fb
