"""
Phase 4 API Routers — Recovery Intelligence + Economics + Decision Support (Tasks 5-8)
"""
from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from backend.database import get_db
from backend.schemas.all_schemas import RecoveryEstimateRequest, EconomicAnalysisRequest
from backend.services.recovery_service import RecoveryIntelligenceService
from backend.services.economic_service import EconomicIntelligenceService
from backend.services.decision_service import DecisionSupportService
from backend.services.environmental_service import EnvironmentalReportingService
from backend.services.report_service import ReportGenerationService

# ── Recovery ───────────────────────────────────────────────────────────
recovery_router = APIRouter(prefix="/api/v1/intelligence/recovery", tags=["Recovery Intelligence"])
_recovery_svc = RecoveryIntelligenceService()


@recovery_router.post("/estimate")
def estimate_recovery(request: RecoveryEstimateRequest):
    """Estimate recoverable materials for a device type and weight."""
    result = _recovery_svc.estimate_recovery(
        device_type=request.device_type,
        weight_kg=request.weight_kg,
    )
    return result


@recovery_router.get("/device-types")
def supported_device_types():
    """List device types with available composition data."""
    from backend.services.recovery_service import DEVICE_COMPOSITION_G_PER_KG
    return {
        "supported_types": list(DEVICE_COMPOSITION_G_PER_KG.keys()),
        "note": "Composition data based on published EEA/UNEP surveys.",
    }


# ── Economics ──────────────────────────────────────────────────────────
economics_router = APIRouter(prefix="/api/v1/intelligence/economics", tags=["Economic Intelligence"])
_econ_svc = EconomicIntelligenceService()


@economics_router.post("/analyze")
def economic_analysis(request: EconomicAnalysisRequest):
    """Estimate economic value of recovered materials."""
    if not request.materials:
        # Quick estimate from device type + weight
        if not request.device_type or not request.weight_kg:
            raise HTTPException(400, detail="Provide either 'materials' list or 'device_type' + 'weight_kg'")
        estimate = _recovery_svc.estimate_recovery(
            device_type=request.device_type,
            weight_kg=request.weight_kg,
        )
        materials = estimate.get("materials", [])
    else:
        materials = request.materials

    return _econ_svc.analyze_batch_economics(
        materials=materials,
        weight_kg=request.weight_kg or 1.0,
        processing_cost_usd=request.processing_cost_usd,
    )


@economics_router.get("/prices")
def material_prices():
    """Get indicative material price references."""
    return _econ_svc.all_prices()


@economics_router.get("/prices/{material_name}")
def material_price(material_name: str):
    """Get price reference for a specific material."""
    price = _econ_svc.get_price_reference(material_name)
    if price is None:
        raise HTTPException(404, detail=f"No price reference for material '{material_name}'")
    return price


# ── Decision Support ───────────────────────────────────────────────────
decision_router = APIRouter(prefix="/api/v1/intelligence/decisions", tags=["Decision Support"])
_decision_svc = DecisionSupportService()


@decision_router.post("/recommend")
def get_recommendations(
    device_type: Optional[str] = None,
    batch_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Get recycling process recommendations for a device type."""
    return _decision_svc.get_recommendations(
        device_type=device_type,
        batch_id=batch_id,
    )


# ── Environmental ──────────────────────────────────────────────────────
environmental_router = APIRouter(prefix="/api/v1/environmental", tags=["Environmental Reporting"])
_env_svc = EnvironmentalReportingService()


@environmental_router.post("/report/{batch_id}")
def generate_env_report(batch_id: str, db: Session = Depends(get_db)):
    """Generate environmental impact report for a batch."""
    return _env_svc.generate_batch_environmental_report(db, batch_id)


@environmental_router.get("/summary")
def environmental_summary(db: Session = Depends(get_db)):
    """Get environmental summary across all batches."""
    return _env_svc.get_period_summary(db)


# ── Reports ────────────────────────────────────────────────────────────
reports_router = APIRouter(prefix="/api/v1/reports", tags=["Report Generation"])
_report_svc = ReportGenerationService()


@reports_router.post("/batch/{batch_id}")
def batch_report(batch_id: str, format: str = "json", db: Session = Depends(get_db)):
    """Generate downloadable batch report."""
    from backend.services.batch_service import BatchManagementService
    batch_svc = BatchManagementService()
    history = batch_svc.get_batch_history(db, batch_id)
    return _report_svc.generate_batch_report(history, format=format)


@reports_router.post("/inventory")
def inventory_report(format: str = "json", db: Session = Depends(get_db)):
    """Generate inventory report."""
    from backend.services.batch_service import InventoryService
    inv_svc = InventoryService()
    items = inv_svc.get_summary(db)
    return _report_svc.generate_inventory_report(items, format=format)


@reports_router.post("/ai-predictions")
def ai_prediction_report(format: str = "json", db: Session = Depends(get_db)):
    """Generate AI predictions report."""
    from backend.models.all_models import AIPrediction
    preds = db.query(AIPrediction).order_by(AIPrediction.created_at.desc()).limit(500).all()
    data = [{"id": p.id, "task": p.task_type, "prediction": p.prediction, "confidence": p.confidence} for p in preds]
    return _report_svc.generate_ai_report(data, format=format)
