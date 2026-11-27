"""
E-Waste AI — Industrial Batch Management Service (Phase 4 Task 7)
==================================================================
Company workflow: incoming registration, batch tracking, audit history.
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from backend.models.all_models import (
    AIPrediction,
    Component,
    Device,
    InventoryItem,
    OperationalCost,
    ProcessingOperation,
    RecoveryRecord,
    WasteBatch,
)

logger = logging.getLogger(__name__)


def _batch_number() -> str:
    """Generate unique batch number: EWASTE-YYYYMMDD-XXXX"""
    today = datetime.utcnow().strftime("%Y%m%d")
    suffix = str(uuid.uuid4())[:4].upper()
    return f"EWASTE-{today}-{suffix}"


class BatchManagementService:
    """Industrial batch lifecycle management."""

    def create_batch(self, db: Session, source: str, weight_kg: float, **kwargs) -> WasteBatch:
        batch = WasteBatch(
            batch_number=_batch_number(),
            source=source,
            total_weight_kg=weight_kg,
            received_date=kwargs.get("received_date", datetime.utcnow()),
            waste_category=kwargs.get("waste_category"),
            location=kwargs.get("location"),
            notes=kwargs.get("notes"),
            status="received",
        )
        db.add(batch)
        db.commit()
        db.refresh(batch)
        logger.info("Created batch %s (%.2f kg from %s)", batch.batch_number, weight_kg, source)
        return batch

    def get_batch(self, db: Session, batch_id: str) -> Optional[WasteBatch]:
        return db.query(WasteBatch).filter(WasteBatch.id == batch_id).first()

    def get_batch_by_number(self, db: Session, batch_number: str) -> Optional[WasteBatch]:
        return db.query(WasteBatch).filter(WasteBatch.batch_number == batch_number).first()

    def list_batches(self, db: Session, status: Optional[str] = None, limit: int = 50) -> list[WasteBatch]:
        q = db.query(WasteBatch)
        if status:
            q = q.filter(WasteBatch.status == status)
        return q.order_by(WasteBatch.created_at.desc()).limit(limit).all()

    def update_status(self, db: Session, batch_id: str, new_status: str) -> Optional[WasteBatch]:
        batch = self.get_batch(db, batch_id)
        if batch:
            batch.status = new_status
            batch.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(batch)
        return batch

    def add_device(self, db: Session, batch_id: str, **kwargs) -> Device:
        device = Device(batch_id=batch_id, **{k: v for k, v in kwargs.items() if v is not None})
        db.add(device)
        db.commit()
        db.refresh(device)
        return device

    def get_batch_history(self, db: Session, batch_id: str) -> dict:
        """Return full audit history for a batch."""
        batch = self.get_batch(db, batch_id)
        if not batch:
            return {"error": "Batch not found"}

        devices = db.query(Device).filter(Device.batch_id == batch_id).all()
        operations = db.query(ProcessingOperation).filter(ProcessingOperation.batch_id == batch_id).all()
        recovery = db.query(RecoveryRecord).filter(RecoveryRecord.batch_id == batch_id).all()
        costs = db.query(OperationalCost).filter(OperationalCost.batch_id == batch_id).all()

        return {
            "batch": {
                "id": batch.id,
                "batch_number": batch.batch_number,
                "source": batch.source,
                "status": batch.status,
                "total_weight_kg": batch.total_weight_kg,
                "received_date": str(batch.received_date),
            },
            "devices_count": len(devices),
            "operations": [{"type": op.operation_type, "status": op.status, "time": str(op.created_at)} for op in operations],
            "recovery_records": len(recovery),
            "total_recovered_g": sum(r.recovered_quantity_g or 0 for r in recovery),
            "total_costs_usd": sum(c.amount_usd or 0 for c in costs),
        }


class InventoryService:
    """Material inventory management."""

    def add_item(self, db: Session, **kwargs) -> InventoryItem:
        item = InventoryItem(**{k: v for k, v in kwargs.items() if v is not None})
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    def get_inventory(self, db: Session, material_name: Optional[str] = None) -> list[InventoryItem]:
        q = db.query(InventoryItem)
        if material_name:
            q = q.filter(InventoryItem.material_name.ilike(f"%{material_name}%"))
        return q.order_by(InventoryItem.material_name).all()

    def get_summary(self, db: Session) -> list[dict]:
        """Aggregate inventory by material name."""
        items = db.query(InventoryItem).all()
        summary: dict[str, float] = {}
        for item in items:
            summary[item.material_name] = summary.get(item.material_name, 0) + (item.quantity_g or 0)
        return [{"material": k, "total_quantity_g": round(v, 4)} for k, v in sorted(summary.items())]

    def record_recovery(self, db: Session, batch_id: str, **kwargs) -> RecoveryRecord:
        record = RecoveryRecord(batch_id=batch_id, **{k: v for k, v in kwargs.items() if v is not None})
        db.add(record)
        # Also update inventory
        mat_name = kwargs.get("material_name")
        qty = kwargs.get("recovered_quantity_g", 0)
        if mat_name and qty:
            existing = db.query(InventoryItem).filter(
                InventoryItem.material_name == mat_name,
                InventoryItem.batch_id == batch_id,
            ).first()
            if existing:
                existing.quantity_g = (existing.quantity_g or 0) + qty
                existing.updated_at = datetime.utcnow()
            else:
                db.add(InventoryItem(
                    material_name=mat_name,
                    quantity_g=qty,
                    batch_id=batch_id,
                    source="recycled",
                ))
        db.commit()
        db.refresh(record)
        return record
