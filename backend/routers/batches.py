"""
Phase 4 API Routers — Batch & Inventory Management (Task 7)
"""
from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from backend.database import get_db
from backend.schemas.all_schemas import (
    WasteBatchCreate, WasteBatchOut, BatchStatusUpdate,
    DeviceCreate, DeviceOut, RecoveryRecordCreate, RecoveryRecordOut,
    InventoryItemCreate, InventoryItemOut, OperationalCostCreate, OperationalCostOut,
)
from backend.services.batch_service import BatchManagementService, InventoryService

router = APIRouter(prefix="/api/v1/batches", tags=["Batch Management"])
_batch_svc = BatchManagementService()
_inv_svc = InventoryService()


@router.post("", response_model=WasteBatchOut, status_code=201)
def create_batch(payload: WasteBatchCreate, db: Session = Depends(get_db)):
    """Register incoming e-waste batch."""
    batch = _batch_svc.create_batch(
        db, payload.source, payload.total_weight_kg,
        waste_category=payload.waste_category,
        location=payload.location,
        received_date=payload.received_date,
        notes=payload.notes,
    )
    return batch


@router.get("", response_model=list[WasteBatchOut])
def list_batches(status: Optional[str] = None, limit: int = 50, db: Session = Depends(get_db)):
    """List all batches, optionally filtered by status."""
    return _batch_svc.list_batches(db, status=status, limit=limit)


@router.get("/{batch_id}", response_model=WasteBatchOut)
def get_batch(batch_id: str, db: Session = Depends(get_db)):
    batch = _batch_svc.get_batch(db, batch_id)
    if not batch:
        raise HTTPException(404, detail="Batch not found")
    return batch


@router.patch("/{batch_id}/status")
def update_batch_status(batch_id: str, payload: BatchStatusUpdate, db: Session = Depends(get_db)):
    batch = _batch_svc.update_status(db, batch_id, payload.status)
    if not batch:
        raise HTTPException(404, detail="Batch not found")
    return {"success": True, "batch_id": batch_id, "new_status": payload.status}


@router.get("/{batch_id}/history")
def batch_history(batch_id: str, db: Session = Depends(get_db)):
    """Full audit history for a batch."""
    return _batch_svc.get_batch_history(db, batch_id)


@router.post("/{batch_id}/devices", response_model=DeviceOut, status_code=201)
def add_device(batch_id: str, payload: DeviceCreate, db: Session = Depends(get_db)):
    """Register a device within a batch."""
    if not _batch_svc.get_batch(db, batch_id):
        raise HTTPException(404, detail="Batch not found")
    return _batch_svc.add_device(
        db, batch_id,
        device_type=payload.device_type,
        manufacturer=payload.manufacturer,
        model_name=payload.model_name,
        year_manufactured=payload.year_manufactured,
        weight_kg=payload.weight_kg,
        condition=payload.condition,
    )


# ── Recovery Records ───────────────────────────────────────────────────

recovery_router = APIRouter(prefix="/api/v1/recovery", tags=["Recovery Records"])


@recovery_router.post("", response_model=RecoveryRecordOut, status_code=201)
def add_recovery(payload: RecoveryRecordCreate, db: Session = Depends(get_db)):
    """Record recovered material from a batch."""
    record = _inv_svc.record_recovery(
        db, payload.batch_id,
        material_name=payload.material_name,
        recovered_quantity_g=payload.recovered_quantity_g,
        recovery_method=payload.recovery_method,
        recovery_rate_percent=payload.recovery_rate_percent,
        estimated_value_usd=payload.estimated_value_usd,
        price_per_g_usd=payload.price_per_g_usd,
        price_source=payload.price_source,
        notes=payload.notes,
    )
    return record


# ── Inventory ──────────────────────────────────────────────────────────

inventory_router = APIRouter(prefix="/api/v1/inventory", tags=["Inventory"])


@inventory_router.get("")
def get_inventory(material_name: Optional[str] = None, db: Session = Depends(get_db)):
    items = _inv_svc.get_inventory(db, material_name)
    return [
        {
            "id": i.id, "material_name": i.material_name, "quantity_g": i.quantity_g,
            "unit": i.unit, "purity_percent": i.purity_percent,
            "location": i.location, "source": i.source,
        }
        for i in items
    ]


@inventory_router.get("/summary")
def inventory_summary(db: Session = Depends(get_db)):
    return _inv_svc.get_summary(db)


@inventory_router.post("", status_code=201)
def add_inventory_item(payload: InventoryItemCreate, db: Session = Depends(get_db)):
    item = _inv_svc.add_item(
        db,
        material_name=payload.material_name,
        quantity_g=payload.quantity_g,
        unit=payload.unit,
        purity_percent=payload.purity_percent,
        location=payload.location,
        batch_id=payload.batch_id,
        source=payload.source,
    )
    return {"id": item.id, "material_name": item.material_name, "quantity_g": item.quantity_g}
