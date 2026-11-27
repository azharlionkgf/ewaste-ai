"""
E-Waste AI — Environmental & Compliance Reporting Service (Phase 4 Task 9)
===========================================================================
Tracks waste quantities, recoveries, and estimates environmental impact.
Uses configurable, documented calculation assumptions.
Does NOT auto-claim legal compliance.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from backend.models.all_models import EnvironmentalReport, RecoveryRecord, WasteBatch

logger = logging.getLogger(__name__)

# ── CO2 Avoidance Factors ──────────────────────────────────────────────
# Source: European Environment Agency estimates
# kg CO2 avoided per kg of material recycled (vs. virgin production)
CO2_AVOIDANCE_FACTORS_KG_PER_KG: dict[str, float] = {
    "aluminum": 9.1,
    "copper": 3.5,
    "steel": 1.5,
    "gold": 20000.0 / 1000,   # gold mining is extremely CO2 intensive
    "silver": 150.0 / 1000,
    "lithium": 15.0,
    "cobalt": 25.0,
    "plastic": 1.5,
    "default": 2.0,
}

CO2_DATA_SOURCE = "EEA estimates (indicative values, methodology in assumptions)"


class EnvironmentalReportingService:
    """Generate environmental impact estimates for e-waste processing."""

    def generate_batch_environmental_report(
        self,
        db: Session,
        batch_id: str,
        generated_by: str = "system",
    ) -> dict:
        """Generate environmental impact estimates for a batch."""
        batch = db.query(WasteBatch).filter(WasteBatch.id == batch_id).first()
        if not batch:
            return {"error": "Batch not found"}

        recoveries = db.query(RecoveryRecord).filter(RecoveryRecord.batch_id == batch_id).all()

        total_waste_kg = batch.total_weight_kg or 0.0
        total_recovered_g = sum(r.recovered_quantity_g or 0 for r in recoveries)
        total_recovered_kg = total_recovered_g / 1000.0

        recycling_rate = (total_recovered_kg / total_waste_kg * 100) if total_waste_kg > 0 else 0.0

        # CO2 estimate
        co2_avoided = 0.0
        material_co2 = []
        for rec in recoveries:
            factor = CO2_AVOIDANCE_FACTORS_KG_PER_KG.get(
                rec.material_name or "", CO2_AVOIDANCE_FACTORS_KG_PER_KG["default"]
            )
            qty_kg = (rec.recovered_quantity_g or 0) / 1000.0
            avoided = factor * qty_kg
            co2_avoided += avoided
            material_co2.append({
                "material": rec.material_name,
                "recovered_kg": round(qty_kg, 4),
                "co2_factor_kg_per_kg": factor,
                "co2_avoided_kg": round(avoided, 4),
            })

        assumptions = {
            "co2_factors_source": CO2_DATA_SOURCE,
            "recycling_rate_method": "recovered_mass / total_batch_mass",
            "hazardous_identification": "Based on material type flags, not certified analysis",
            "disclaimer": "Environmental estimates are indicative. Not legally certified.",
        }

        # Save to DB
        report = EnvironmentalReport(
            batch_id=batch_id,
            report_period_start=batch.received_date,
            report_period_end=datetime.utcnow(),
            total_waste_kg=total_waste_kg,
            total_recovered_kg=total_recovered_kg,
            recycling_rate_percent=round(recycling_rate, 2),
            co2_avoided_kg_estimate=round(co2_avoided, 4),
            co2_calculation_method=CO2_DATA_SOURCE,
            assumptions=assumptions,
            is_certified=False,
            certification_note=(
                "This report is auto-generated and NOT certified by any regulatory authority. "
                "For compliance submissions, engage a certified environmental auditor."
            ),
            generated_by=generated_by,
        )
        db.add(report)
        db.commit()

        return {
            "batch_id": batch_id,
            "batch_number": batch.batch_number,
            "total_waste_kg": total_waste_kg,
            "total_recovered_kg": round(total_recovered_kg, 4),
            "recycling_rate_percent": round(recycling_rate, 2),
            "co2_avoided_kg_estimate": round(co2_avoided, 4),
            "material_co2_breakdown": material_co2,
            "assumptions": assumptions,
            "is_certified": False,
            "certification_note": report.certification_note,
            "generated_at": report.generated_at.isoformat(),
        }

    def get_period_summary(
        self,
        db: Session,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> dict:
        """Aggregate statistics across all batches in a time period."""
        q = db.query(WasteBatch)
        if start_date:
            q = q.filter(WasteBatch.received_date >= start_date)
        if end_date:
            q = q.filter(WasteBatch.received_date <= end_date)
        batches = q.all()

        total_waste = sum(b.total_weight_kg or 0 for b in batches)
        batch_ids = [b.id for b in batches]

        total_recovered_g = 0.0
        if batch_ids:
            recoveries = db.query(RecoveryRecord).filter(
                RecoveryRecord.batch_id.in_(batch_ids)
            ).all()
            total_recovered_g = sum(r.recovered_quantity_g or 0 for r in recoveries)

        return {
            "batch_count": len(batches),
            "total_waste_kg": round(total_waste, 2),
            "total_recovered_g": round(total_recovered_g, 2),
            "total_recovered_kg": round(total_recovered_g / 1000, 4),
            "recycling_rate_percent": round(
                (total_recovered_g / 1000 / total_waste * 100) if total_waste > 0 else 0, 2
            ),
            "period_start": start_date.isoformat() if start_date else None,
            "period_end": end_date.isoformat() if end_date else None,
        }
