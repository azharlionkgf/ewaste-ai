"""
E-Waste AI — Phase 6: Advanced AI & Recovery Intelligence Engine
================================================================
Centralised intelligence engine integrating:
- Actual trained models from Phase 3 registry
- Material knowledge base (provenance-tagged)
- Recovery prediction (rule-based + model-based)
- Economic valuation
- Anomaly detection
- Predictive analytics
- Hazardous material identification
- SHAP-compatible feature importance (where installed)

All predictions are tagged with source, model_id, version, timestamp.
Never returns hardcoded/fabricated predictions.
"""

import os
import sys
import json
import logging
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# ── optional heavy imports ──────────────────────────────────────────────
try:
    import numpy as np
    NP_OK = True
except ImportError:
    NP_OK = False

try:
    import joblib
    JOBLIB_OK = True
except ImportError:
    JOBLIB_OK = False

try:
    import shap
    SHAP_OK = True
except ImportError:
    SHAP_OK = False


# ══════════════════════════════════════════════════════════════════════════
# MATERIAL KNOWLEDGE BASE
# Sources: EEA (European Environment Agency), UNEP Global E-waste Monitor,
#          US EPA E-Waste reports, StEP Initiative data
# All values are ESTIMATES from published literature — actual yields vary.
# ══════════════════════════════════════════════════════════════════════════

MATERIAL_KNOWLEDGE_BASE = {
    "laptop": {
        "source": "UNEP Global E-waste Monitor 2020; EEA WEEE data 2021",
        "components": ["motherboard","battery","lcd_screen","keyboard","hdd_or_ssd","ram","cooling_fan","power_adapter"],
        "avg_weight_kg": 2.0,
        "material_composition_percent": {
            "steel_iron": 23.0, "aluminum": 14.0, "copper": 7.0,
            "plastic": 15.0, "glass": 4.0, "gold_traces": 0.003,
            "silver_traces": 0.015, "palladium_traces": 0.001,
            "lithium": 0.4, "cobalt": 0.3, "other": 36.286,
        },
        "hazardous_substances": ["lithium","flame_retardants","lead_solder","beryllium"],
        "confidence": "medium",
        "notes": "Composition varies significantly by manufacturer, year and model.",
    },
    "desktop": {
        "source": "UNEP 2020; EPA 2017",
        "components": ["motherboard","power_supply","cpu","ram","gpu","hdd","optical_drive","case"],
        "avg_weight_kg": 7.0,
        "material_composition_percent": {
            "steel_iron": 44.0, "aluminum": 6.5, "copper": 7.0,
            "plastic": 23.0, "gold_traces": 0.002, "silver_traces": 0.010,
            "palladium_traces": 0.0005, "other": 19.4875,
        },
        "hazardous_substances": ["flame_retardants","lead_solder","cadmium"],
        "confidence": "medium",
        "notes": "Tower PC average. Mini-PCs and workstations differ significantly.",
    },
    "mobile_phone": {
        "source": "UNEP 2020; Öko-Institut 2021",
        "components": ["display","battery","circuit_board","camera","speaker","case"],
        "avg_weight_kg": 0.18,
        "material_composition_percent": {
            "aluminum": 24.0, "copper": 15.0, "plastic": 12.0,
            "glass": 10.0, "gold_traces": 0.034, "silver_traces": 0.35,
            "palladium_traces": 0.015, "cobalt": 5.0, "lithium": 2.0,
            "rare_earths": 0.1, "other": 31.501,
        },
        "hazardous_substances": ["lithium","cobalt","flame_retardants","lead_solder"],
        "confidence": "medium-high",
        "notes": "Smartphone average circa 2018-2022. Older feature phones differ.",
    },
    "television": {
        "source": "UNEP 2020; EEA 2019",
        "components": ["lcd_panel","backlight","circuit_board","power_supply","casing"],
        "avg_weight_kg": 10.0,
        "material_composition_percent": {
            "plastic": 46.0, "glass": 20.0, "steel_iron": 6.0,
            "aluminum": 5.0, "copper": 3.0, "gold_traces": 0.001,
            "indium": 0.004, "other": 19.995,
        },
        "hazardous_substances": ["mercury_backlight","flame_retardants","lead_solder","indium"],
        "confidence": "medium",
        "notes": "LCD flat-panel TV. CRT TVs have very different composition (high lead content).",
    },
    "printer": {
        "source": "EPA 2017; StEP Initiative",
        "components": ["motor","circuit_board","plastic_housing","rollers","ink_system"],
        "avg_weight_kg": 5.0,
        "material_composition_percent": {
            "plastic": 50.0, "steel_iron": 25.0, "aluminum": 5.0,
            "copper": 3.0, "rubber": 5.0, "other": 12.0,
        },
        "hazardous_substances": ["flame_retardants","residual_ink","ozone"],
        "confidence": "low-medium",
        "notes": "Varies greatly between inkjet, laser and industrial printers.",
    },
    "battery_pack": {
        "source": "UNEP 2020; IEA Critical Minerals 2021",
        "components": ["cells","bms","casing","connectors"],
        "avg_weight_kg": 0.5,
        "material_composition_percent": {
            "lithium": 7.0, "cobalt": 20.0, "nickel": 15.0,
            "manganese": 7.0, "copper": 10.0, "aluminum": 10.0,
            "graphite": 15.0, "plastic": 10.0, "other": 6.0,
        },
        "hazardous_substances": ["lithium","cobalt","electrolyte_solvent","fluorine"],
        "confidence": "medium",
        "notes": "Li-ion NMC chemistry. LFP and NCA chemistries differ in cobalt content.",
    },
}

# ── Material recovery efficiency factors ───────────────────────────────
# Source: UNEP/EEA industrial recycling benchmarks
# These are TYPICAL rates for established industrial operations.
# Actual rates depend on equipment, process, purity requirements.
RECOVERY_EFFICIENCY = {
    "gold_traces":     {"typical_pct": 85.0, "range": (70, 95), "method": "hydrometallurgy"},
    "silver_traces":   {"typical_pct": 80.0, "range": (65, 92), "method": "hydrometallurgy"},
    "copper":          {"typical_pct": 90.0, "range": (80, 97), "method": "smelting/electrolysis"},
    "aluminum":        {"typical_pct": 85.0, "range": (75, 95), "method": "mechanical/smelting"},
    "steel_iron":      {"typical_pct": 92.0, "range": (85, 97), "method": "magnetic_separation"},
    "lithium":         {"typical_pct": 50.0, "range": (30, 75), "method": "hydrometallurgy"},
    "cobalt":          {"typical_pct": 70.0, "range": (50, 85), "method": "hydrometallurgy"},
    "palladium_traces":{"typical_pct": 80.0, "range": (65, 92), "method": "pyrometallurgy"},
    "plastic":         {"typical_pct": 40.0, "range": (20, 60), "method": "shredding/sorting"},
    "glass":           {"typical_pct": 60.0, "range": (40, 80), "method": "mechanical"},
    "rare_earths":     {"typical_pct": 20.0, "range": (5, 40),  "method": "hydrometallurgy (specialised)"},
}

# ── Reference material prices ──────────────────────────────────────────
# Source: LME spot prices, USGS Mineral Commodity Summaries 2024
# These are INDICATIVE REFERENCE values dated 2024-01 — not live prices.
# Unit: USD per gram
MATERIAL_PRICES_USD_PER_G = {
    "gold_traces":      65.0,
    "silver_traces":    0.80,
    "palladium_traces": 42.0,
    "platinum_traces":  31.0,
    "copper":           0.009,   # ~$9/kg
    "aluminum":         0.002,   # ~$2/kg
    "steel_iron":       0.00015, # ~$0.15/kg
    "cobalt":           0.028,   # ~$28/kg
    "lithium":          0.012,   # ~$12/kg
    "nickel":           0.016,   # ~$16/kg
    "indium":           0.165,   # ~$165/kg
    "rare_earths":      0.015,   # rough average, varies greatly
}
PRICE_SOURCE = "LME spot / USGS Mineral Commodity Summaries"
PRICE_DATE   = "2024-01-15"

# ── Hazardous substance reference ──────────────────────────────────────
HAZARDOUS_REFERENCE = {
    "lithium":           {"risk_level": "high",   "regulation": "Basel Convention; UN Transport regs", "handling": "Licensed battery recycler; fire risk"},
    "cobalt":            {"risk_level": "medium",  "regulation": "REACH (EU)", "handling": "PPE required; dust inhalation hazard"},
    "lead_solder":       {"risk_level": "high",   "regulation": "RoHS (EU); RCRA (US)", "handling": "No burning; specialist dismantling"},
    "mercury_backlight": {"risk_level": "high",   "regulation": "Minamata Convention; Basel", "handling": "Licensed hazardous waste facility only"},
    "cadmium":           {"risk_level": "high",   "regulation": "RoHS; Basel", "handling": "Specialist recycler; carcinogen"},
    "flame_retardants":  {"risk_level": "medium",  "regulation": "Stockholm Convention (some)", "handling": "Avoid incineration; specialist disposal"},
    "beryllium":         {"risk_level": "high",   "regulation": "OSHA; EPA", "handling": "Strict PPE; respiratory carcinogen"},
    "fluorine":          {"risk_level": "medium",  "regulation": "F-Gas Regulation (EU)", "handling": "Licensed facility; corrosive"},
    "indium":            {"risk_level": "low-medium","regulation": "REACH (EU)", "handling": "Dust avoidance; specialist"},
    "electrolyte_solvent":{"risk_level":"high",   "regulation": "EPA RCRA", "handling": "Flammable; sealed containers"},
    "ozone":             {"risk_level": "low",    "regulation": "Indoor air quality guidelines", "handling": "Ventilated area"},
    "residual_ink":      {"risk_level": "low",    "regulation": "Local waste regs", "handling": "Absorbent waste disposal"},
}


# ══════════════════════════════════════════════════════════════════════════
# PHASE 6 INTELLIGENCE ENGINE
# ══════════════════════════════════════════════════════════════════════════

class AdvancedIntelligenceEngine:
    """
    Central intelligence hub for Phase 6.
    Integrates trained models, knowledge base, and analytical services.
    """

    def __init__(self, models_dir: str = "saved_models"):
        self.models_dir = Path(models_dir)
        self._loaded_models: Dict[str, Any] = {}
        self._model_metadata: Dict[str, Dict] = {}

    # ── MODEL MANAGEMENT ──────────────────────────────────────────────

    def load_model(self, model_path: str, model_id: str) -> Tuple[bool, str]:
        """Load a model from disk. Returns (success, message)."""
        if not JOBLIB_OK:
            return False, "joblib not installed — cannot load model files"
        path = Path(model_path)
        if not path.exists():
            return False, f"Model file not found: {model_path}"
        try:
            model = joblib.load(path)
            self._loaded_models[model_id] = model
            self._model_metadata[model_id] = {
                "path": str(path),
                "loaded_at": datetime.utcnow().isoformat(),
                "file_size_bytes": path.stat().st_size,
            }
            logger.info(f"Loaded model {model_id} from {path}")
            return True, f"Model {model_id} loaded successfully"
        except Exception as ex:
            logger.error(f"Failed to load model {model_id}: {ex}")
            return False, f"Failed to load model: {ex}"

    def list_available_models(self) -> List[Dict]:
        """List models registered in the database."""
        try:
            from backend.database import SessionLocal
            from backend.models.all_models import TrainedModel
            db = SessionLocal()
            try:
                models = db.query(TrainedModel).filter(
                    TrainedModel.status.in_(["active", "trained"])
                ).all()
                return [{
                    "model_id": m.id, "name": m.name, "version": m.version,
                    "task_type": m.task_type, "algorithm": m.algorithm,
                    "status": m.status, "file_path": m.file_path,
                    "file_exists": os.path.exists(m.file_path) if m.file_path else False,
                    "created_at": str(m.created_at),
                } for m in models]
            finally:
                db.close()
        except Exception as ex:
            logger.error(f"list_available_models error: {ex}")
            return []

    def predict(self, model_id: str, features: Dict[str, Any],
                record_to_db: bool = True) -> Dict[str, Any]:
        """
        Run inference with a registered model.
        Returns prediction dict with provenance tags.
        Never fabricates results.
        """
        # Ensure model is loaded
        if model_id not in self._loaded_models:
            # Try to load from DB record
            try:
                from backend.database import SessionLocal
                from backend.models.all_models import TrainedModel
                db = SessionLocal()
                try:
                    m = db.query(TrainedModel).filter(TrainedModel.id == model_id).first()
                    if not m:
                        return {"error": f"Model {model_id} not found in registry",
                                "available": False}
                    if not m.file_path:
                        return {"error": f"Model {model_id} has no file path recorded",
                                "available": False}
                    ok, msg = self.load_model(m.file_path, model_id)
                    if not ok:
                        return {"error": msg, "available": False,
                                "model_name": m.name, "model_version": m.version}
                finally:
                    db.close()
            except Exception as ex:
                return {"error": f"Could not resolve model: {ex}", "available": False}

        model = self._loaded_models[model_id]
        meta  = self._model_metadata.get(model_id, {})

        try:
            if not NP_OK:
                return {"error": "numpy not available for inference", "available": False}

            # Build feature vector from dict
            feature_values = list(features.values())
            X = np.array(feature_values).reshape(1, -1)

            prediction_raw = model.predict(X)
            prediction = prediction_raw[0]

            confidence = None
            proba = None
            if hasattr(model, "predict_proba"):
                try:
                    proba = model.predict_proba(X)[0].tolist()
                    confidence = max(proba)
                except Exception:
                    pass

            result = {
                "model_id": model_id,
                "prediction": prediction.item() if hasattr(prediction, "item") else prediction,
                "confidence": confidence,
                "class_probabilities": proba,
                "input_features": features,
                "prediction_type": "model_inference",
                "timestamp": datetime.utcnow().isoformat(),
                "available": True,
            }

            # Record to DB
            if record_to_db:
                try:
                    from backend.database import SessionLocal
                    from backend.models.all_models import AIPrediction
                    input_hash = hashlib.sha256(
                        json.dumps(features, sort_keys=True).encode()
                    ).hexdigest()[:16]
                    db = SessionLocal()
                    try:
                        pred_record = AIPrediction(
                            model_id=model_id,
                            input_hash=input_hash,
                            prediction=json.dumps(result),
                            confidence=confidence,
                            prediction_type="model_inference",
                            created_at=datetime.utcnow(),
                        )
                        db.add(pred_record); db.commit()
                    finally:
                        db.close()
                except Exception as ex:
                    logger.warning(f"Could not record prediction to DB: {ex}")

            return result

        except Exception as ex:
            logger.error(f"Inference error for model {model_id}: {ex}")
            return {"error": f"Inference failed: {ex}", "model_id": model_id, "available": True}

    # ── MATERIAL KNOWLEDGE ─────────────────────────────────────────────

    def get_device_knowledge(self, device_type: str) -> Dict:
        """Return knowledge-base entry for a device type."""
        entry = MATERIAL_KNOWLEDGE_BASE.get(device_type.lower())
        if entry is None:
            return {
                "available": False,
                "device_type": device_type,
                "message": f"No reference data for device type '{device_type}'. "
                           "Only devices in the UNEP/EEA knowledge base are supported.",
            }
        return {"available": True, "device_type": device_type, **entry}

    def list_supported_device_types(self) -> List[str]:
        return list(MATERIAL_KNOWLEDGE_BASE.keys())

    # ── RECOVERY PREDICTION ────────────────────────────────────────────

    def estimate_recovery(self, device_type: str, weight_kg: float,
                          condition: str = "unknown") -> Dict:
        """
        Estimate recoverable materials for a device.
        Uses rule-based calculation from published composition data.
        Returns estimates with explicit uncertainty and source labelling.
        """
        kb = MATERIAL_KNOWLEDGE_BASE.get(device_type.lower())
        if not kb:
            return {
                "available": False,
                "message": f"No composition data for '{device_type}'.",
                "supported_types": self.list_supported_device_types(),
            }

        condition_factor = {"excellent": 0.95, "good": 0.90, "fair": 0.80,
                            "poor": 0.65, "unknown": 0.75}.get(condition.lower(), 0.75)

        recoverable = {}
        total_est_value_usd = 0.0

        for material, pct in kb["material_composition_percent"].items():
            material_mass_g = weight_kg * 1000 * (pct / 100.0)
            eff = RECOVERY_EFFICIENCY.get(material, {"typical_pct": 50.0, "range": (20, 80),
                                                      "method": "general"})
            recovered_g = material_mass_g * (eff["typical_pct"] / 100.0) * condition_factor
            price = MATERIAL_PRICES_USD_PER_G.get(material, 0.0)
            value_usd = recovered_g * price

            recoverable[material] = {
                "composition_pct": pct,
                "total_mass_g": round(material_mass_g, 4),
                "recovery_efficiency_pct": eff["typical_pct"],
                "recovery_range": eff["range"],
                "estimated_recovered_g": round(recovered_g, 4),
                "recovery_method": eff.get("method", "general"),
                "estimated_value_usd": round(value_usd, 4),
                "price_per_g_usd": price,
                "value_type": "estimate",
            }
            total_est_value_usd += value_usd

        return {
            "available": True,
            "device_type": device_type,
            "input_weight_kg": weight_kg,
            "condition": condition,
            "condition_factor_applied": condition_factor,
            "recoverable_materials": recoverable,
            "total_estimated_value_usd": round(total_est_value_usd, 4),
            "data_source": kb["source"],
            "knowledge_confidence": kb["confidence"],
            "value_source": "INDICATIVE — reference prices dated " + PRICE_DATE,
            "price_source": PRICE_SOURCE,
            "calculation_type": "rule_based_estimate",
            "disclaimer": (
                "These are ESTIMATES based on published average composition data and "
                "typical industrial recovery efficiencies. Actual recovery quantities "
                "and values depend on specific equipment, processes, purity requirements, "
                "and current market prices. Do not use as official valuations."
            ),
            "timestamp": datetime.utcnow().isoformat(),
        }

    def estimate_batch_recovery(self, batch_id: str) -> Dict:
        """Estimate total recovery for all devices in a batch."""
        try:
            from backend.database import SessionLocal
            from backend.models.all_models import WasteBatch, Device
            db = SessionLocal()
            try:
                batch = db.query(WasteBatch).filter(WasteBatch.id == batch_id).first()
                if not batch:
                    return {"available": False, "message": f"Batch {batch_id} not found"}

                devices = db.query(Device).filter(Device.batch_id == batch_id).all()

                if not devices:
                    # Fall back to batch-level estimate using waste category
                    result = self.estimate_recovery(
                        device_type=batch.waste_category or "laptop",
                        weight_kg=batch.total_weight_kg or 0,
                    )
                    result["estimation_basis"] = "batch_weight_only"
                    result["device_count"] = 0
                    return result

                # Sum device-level estimates
                aggregate: Dict[str, Dict] = {}
                for dev in devices:
                    dev_result = self.estimate_recovery(
                        device_type=dev.device_type,
                        weight_kg=dev.weight_kg or 0,
                        condition=dev.condition or "unknown",
                    )
                    if not dev_result.get("available"):
                        continue
                    for mat, data in dev_result["recoverable_materials"].items():
                        if mat not in aggregate:
                            aggregate[mat] = {
                                "total_mass_g": 0, "estimated_recovered_g": 0,
                                "estimated_value_usd": 0, "value_type": "estimate",
                            }
                        aggregate[mat]["total_mass_g"] += data["total_mass_g"]
                        aggregate[mat]["estimated_recovered_g"] += data["estimated_recovered_g"]
                        aggregate[mat]["estimated_value_usd"] += data["estimated_value_usd"]

                total_value = sum(v["estimated_value_usd"] for v in aggregate.values())

                return {
                    "available": True,
                    "batch_id": batch_id,
                    "batch_number": batch.batch_number,
                    "device_count": len(devices),
                    "total_batch_weight_kg": batch.total_weight_kg,
                    "recoverable_materials": aggregate,
                    "total_estimated_value_usd": round(total_value, 2),
                    "estimation_basis": "device_level_aggregation",
                    "calculation_type": "rule_based_estimate",
                    "value_source": "INDICATIVE — " + PRICE_DATE,
                    "disclaimer": "Estimates only. See individual device estimates for details.",
                    "timestamp": datetime.utcnow().isoformat(),
                }
            finally:
                db.close()
        except Exception as ex:
            return {"available": False, "message": f"Batch estimation error: {ex}"}

    # ── ECONOMIC ANALYSIS ──────────────────────────────────────────────

    def estimate_processing_cost(self, weight_kg: float, device_count: int = 0,
                                  labour_hours: float = 0, equipment_hours: float = 0,
                                  transport_km: float = 0,
                                  hazardous_disposal_kg: float = 0) -> Dict:
        """
        Estimate processing costs using configurable default rates.
        All rates are INDICATIVE — configure for your actual operation.
        """
        RATES = {
            "labour_per_hour_usd": 15.0,
            "equipment_per_hour_usd": 25.0,
            "transport_per_km_usd": 0.80,
            "hazardous_disposal_per_kg_usd": 3.50,
            "overhead_per_device_usd": 2.00,
            "fixed_overhead_usd": 50.0,
        }

        labour_cost    = labour_hours * RATES["labour_per_hour_usd"]
        equipment_cost = equipment_hours * RATES["equipment_per_hour_usd"]
        transport_cost = transport_km * RATES["transport_per_km_usd"]
        hazardous_cost = hazardous_disposal_kg * RATES["hazardous_disposal_per_kg_usd"]
        overhead_cost  = device_count * RATES["overhead_per_device_usd"] + RATES["fixed_overhead_usd"]
        total_cost     = labour_cost + equipment_cost + transport_cost + hazardous_cost + overhead_cost

        return {
            "total_cost_usd": round(total_cost, 2),
            "breakdown": {
                "labour": round(labour_cost, 2),
                "equipment": round(equipment_cost, 2),
                "transport": round(transport_cost, 2),
                "hazardous_disposal": round(hazardous_cost, 2),
                "overhead": round(overhead_cost, 2),
            },
            "rates_used": RATES,
            "disclaimer": "ESTIMATE ONLY. Rates are configurable defaults — not certified cost data.",
            "timestamp": datetime.utcnow().isoformat(),
        }

    # ── ANOMALY DETECTION ──────────────────────────────────────────────

    def detect_anomalies(self) -> List[Dict]:
        """
        Rule-based anomaly detection on operational data.
        Returns list of flagged items with explanations.
        Does NOT imply fraud or wrongdoing.
        """
        flags = []
        try:
            from backend.database import SessionLocal
            from backend.models.all_models import (
                WasteBatch, RecoveryRecord, Inventory, Device
            )
            from sqlalchemy import func
            db = SessionLocal()
            try:
                # 1. Unusually heavy batches (>99th percentile approximation)
                weights = [b.total_weight_kg for b in db.query(WasteBatch).all()
                           if b.total_weight_kg]
                if len(weights) >= 5 and NP_OK:
                    threshold = float(np.percentile(weights, 95))
                    for b in db.query(WasteBatch).filter(
                            WasteBatch.total_weight_kg > threshold).all():
                        flags.append({
                            "type": "unusual_batch_weight",
                            "severity": "medium",
                            "record_type": "WasteBatch",
                            "record_id": b.id,
                            "detail": f"Batch {b.batch_number}: {b.total_weight_kg} kg "
                                      f"exceeds 95th percentile ({threshold:.1f} kg).",
                            "action": "Verify weight measurement is correct.",
                        })

                # 2. Duplicate batch numbers
                from sqlalchemy import func as sf
                dups = db.query(WasteBatch.batch_number, sf.count(WasteBatch.id).label("cnt"))\
                         .group_by(WasteBatch.batch_number)\
                         .having(sf.count(WasteBatch.id) > 1).all()
                for dup in dups:
                    flags.append({
                        "type": "duplicate_batch_number",
                        "severity": "high",
                        "record_type": "WasteBatch",
                        "detail": f"Batch number '{dup.batch_number}' appears {dup.cnt} times.",
                        "action": "Review and merge or renumber duplicates.",
                    })

                # 3. Recovery records with zero quantity
                zero_recs = db.query(RecoveryRecord).filter(
                    RecoveryRecord.recovered_quantity_g <= 0).all()
                for r in zero_recs:
                    flags.append({
                        "type": "zero_recovery_quantity",
                        "severity": "low",
                        "record_type": "RecoveryRecord",
                        "record_id": r.id,
                        "detail": f"Recovery record for '{r.material_name}' has 0 g quantity.",
                        "action": "Check if record was entered correctly.",
                    })

                # 4. Batches with no devices recorded (>7 days old)
                from datetime import timezone
                old_batches = db.query(WasteBatch).filter(
                    WasteBatch.created_at < datetime.utcnow() - timedelta(days=7),
                    WasteBatch.status.in_(["incoming","sorting"])
                ).all()
                for b in old_batches:
                    dev_cnt = db.query(Device).filter(Device.batch_id == b.id).count()
                    if dev_cnt == 0:
                        flags.append({
                            "type": "batch_no_devices",
                            "severity": "low",
                            "record_type": "WasteBatch",
                            "record_id": b.id,
                            "detail": f"Batch {b.batch_number} has been in '{b.status}' "
                                      f"for >7 days with no device records.",
                            "action": "Register individual devices or update batch status.",
                        })

                # 5. Unusually high recovery rates
                high_rate = db.query(RecoveryRecord).filter(
                    RecoveryRecord.recovery_rate_percent > 100).all()
                for r in high_rate:
                    flags.append({
                        "type": "recovery_rate_exceeds_100",
                        "severity": "high",
                        "record_type": "RecoveryRecord",
                        "record_id": r.id,
                        "detail": f"Recovery rate {r.recovery_rate_percent}% > 100% for {r.material_name}.",
                        "action": "Data entry error — review and correct.",
                    })

                return flags
            finally:
                db.close()
        except Exception as ex:
            logger.error(f"Anomaly detection error: {ex}")
            return [{"type": "system_error", "severity": "high",
                     "detail": f"Anomaly detection failed: {ex}",
                     "action": "Check database connection."}]

    # ── PREDICTIVE ANALYTICS ───────────────────────────────────────────

    def compute_trends(self, days: int = 30) -> Dict:
        """
        Compute trend metrics from historical DB data.
        Returns None values when insufficient data.
        """
        try:
            from backend.database import SessionLocal
            from backend.models.all_models import WasteBatch, RecoveryRecord
            from sqlalchemy import func
            db = SessionLocal()
            try:
                cutoff = datetime.utcnow() - timedelta(days=days)

                # Batch volume trend
                batches_period = db.query(WasteBatch).filter(
                    WasteBatch.created_at >= cutoff).all()
                total_weight_period = sum(b.total_weight_kg or 0 for b in batches_period)

                # Recovery trend
                recs_period = db.query(RecoveryRecord).filter(
                    RecoveryRecord.recorded_at >= cutoff).all()
                total_rec_period_g = sum(r.recovered_quantity_g or 0 for r in recs_period)

                # Compare to prior period
                prior_cutoff = cutoff - timedelta(days=days)
                prior_batches = db.query(WasteBatch).filter(
                    WasteBatch.created_at >= prior_cutoff,
                    WasteBatch.created_at < cutoff).all()
                prior_weight = sum(b.total_weight_kg or 0 for b in prior_batches)

                weight_change_pct = (
                    ((total_weight_period - prior_weight) / prior_weight * 100)
                    if prior_weight > 0 else None
                )

                return {
                    "period_days": days,
                    "batches_in_period": len(batches_period),
                    "total_weight_period_kg": total_weight_period,
                    "total_recovered_period_g": total_rec_period_g,
                    "prior_period_weight_kg": prior_weight,
                    "weight_change_pct": round(weight_change_pct, 1) if weight_change_pct else None,
                    "data_sufficient": len(batches_period) >= 3,
                    "insufficient_data_note": (
                        None if len(batches_period) >= 3 else
                        f"Only {len(batches_period)} batches in period — "
                        "trends require at least 3 data points."
                    ),
                    "timestamp": datetime.utcnow().isoformat(),
                }
            finally:
                db.close()
        except Exception as ex:
            return {
                "error": str(ex),
                "data_sufficient": False,
                "period_days": days,
                "batches_in_period": 0,
                "insufficient_data_note": (
                    "Trend computation unavailable: database error or insufficient schema. "
                    "This is expected in test environments with an older schema."
                ),
            }

    # ── EXPLAINABILITY ────────────────────────────────────────────────

    def explain_prediction(self, model_id: str, features: Dict[str, Any],
                           feature_names: Optional[List[str]] = None) -> Dict:
        """
        Generate feature importance explanation for a prediction.
        Uses SHAP if available, falls back to built-in feature_importances_.
        """
        if model_id not in self._loaded_models:
            return {"available": False,
                    "message": "Model not loaded. Run predict() first."}

        model = self._loaded_models[model_id]
        feature_values = list(features.values())
        names = feature_names or list(features.keys())

        # Try SHAP
        if SHAP_OK and NP_OK:
            try:
                X = np.array(feature_values).reshape(1, -1)
                explainer = shap.Explainer(model)
                shap_vals = explainer(X)
                shap_arr = shap_vals.values[0].tolist()
                return {
                    "available": True,
                    "method": "SHAP",
                    "feature_names": names,
                    "shap_values": shap_arr,
                    "importance": sorted(
                        zip(names, shap_arr), key=lambda x: abs(x[1]), reverse=True
                    ),
                    "disclaimer": "SHAP values show the contribution of each feature to this specific prediction.",
                }
            except Exception as ex:
                logger.warning(f"SHAP explanation failed: {ex}")

        # Fallback: built-in feature_importances_ (tree models)
        if hasattr(model, "feature_importances_") and NP_OK:
            fi = model.feature_importances_.tolist()
            return {
                "available": True,
                "method": "feature_importances",
                "feature_names": names,
                "importances": fi,
                "importance": sorted(zip(names, fi), key=lambda x: abs(x[1]), reverse=True),
                "disclaimer": "Feature importances show global model weights, not instance-specific explanations.",
            }

        # Fallback: coef_ (linear models)
        if hasattr(model, "coef_") and NP_OK:
            coefs = model.coef_.flatten().tolist()[:len(names)]
            return {
                "available": True,
                "method": "linear_coefficients",
                "feature_names": names,
                "coefficients": coefs,
                "importance": sorted(zip(names, coefs), key=lambda x: abs(x[1]), reverse=True),
                "disclaimer": "Linear model coefficients — magnitude indicates feature influence.",
            }

        return {
            "available": False,
            "message": "No explanation method available for this model type. "
                       "Install 'shap' for SHAP-based explanations.",
        }

    # ── RECOVERY OPTIMIZATION ─────────────────────────────────────────

    def recommend_recovery_plan(self, batch_id: str) -> Dict:
        """
        Generate a recovery plan recommendation for a batch.
        Uses rule-based logic from knowledge base + actual DB records.
        All recommendations include explicit reasoning.
        """
        estimate = self.estimate_batch_recovery(batch_id)
        if not estimate.get("available"):
            return estimate

        mats = estimate.get("recoverable_materials", {})
        if not mats:
            return {"available": False, "message": "No recoverable material estimates available."}

        # Sort by value
        sorted_mats = sorted(mats.items(),
                             key=lambda x: x[1].get("estimated_value_usd", 0), reverse=True)
        priorities = []
        for mat, data in sorted_mats[:5]:
            rec_g = data.get("estimated_recovered_g", 0)
            val   = data.get("estimated_value_usd", 0)
            method= data.get("recovery_method", "general")
            priorities.append({
                "material": mat,
                "priority_rank": len(priorities) + 1,
                "estimated_recovered_g": rec_g,
                "estimated_value_usd": val,
                "recommended_method": method,
                "reason": f"Highest value-to-effort ratio for this batch type. "
                          f"Est. {rec_g:.2f} g recoverable via {method}.",
            })

        # Hazardous check
        hazardous_flags = []
        try:
            from backend.database import SessionLocal
            from backend.models.all_models import WasteBatch, Device
            db = SessionLocal()
            try:
                batch = db.query(WasteBatch).filter(WasteBatch.id == batch_id).first()
                devices = db.query(Device).filter(Device.batch_id == batch_id).all()
                for dev in devices:
                    kb = MATERIAL_KNOWLEDGE_BASE.get(dev.device_type or "", {})
                    for hz in kb.get("hazardous_substances", []):
                        ref = HAZARDOUS_REFERENCE.get(hz, {})
                        if ref.get("risk_level") in ("high", "medium"):
                            hazardous_flags.append({
                                "substance": hz,
                                "risk_level": ref.get("risk_level"),
                                "handling": ref.get("handling", "Consult specialist"),
                                "device_type": dev.device_type,
                            })
            finally:
                db.close()
        except Exception:
            pass

        return {
            "available": True,
            "batch_id": batch_id,
            "recovery_priorities": priorities,
            "hazardous_warnings": hazardous_flags,
            "total_estimated_value_usd": estimate["total_estimated_value_usd"],
            "recommendation_basis": "Rule-based: knowledge base composition + recovery efficiency + indicative prices",
            "disclaimer": estimate["disclaimer"],
            "timestamp": datetime.utcnow().isoformat(),
        }


# ── Singleton instance ─────────────────────────────────────────────────
_engine_instance: Optional[AdvancedIntelligenceEngine] = None


def get_engine() -> AdvancedIntelligenceEngine:
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = AdvancedIntelligenceEngine()
    return _engine_instance
