"""
E-Waste AI — Recycling Decision Support Service (Phase 4 Task 8)
=================================================================
Intelligent recommendations based on AI outputs, materials, and rules.
Clearly shows reasoning behind each recommendation.
Does NOT present as certified safety instructions.
"""

from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

HAZARDOUS_FLAGS = {
    "lead": "Lead — toxic heavy metal. Regulated under RoHS/WEEE. Specialized disposal required.",
    "mercury": "Mercury — highly toxic. Cold cathode fluorescent lamps must be handled by certified facility.",
    "cadmium": "Cadmium — carcinogenic. Ni-Cd batteries require specialized recycling.",
    "lithium": "Lithium batteries — fire risk. Must be discharged and segregated before shredding.",
    "cobalt": "Cobalt — toxic in dust form. Battery dismantling requires ventilation.",
    "toner_dust": "Printer toner — respiratory hazard. Handle with dust protection.",
    "asbestos": "Asbestos — carcinogenic. Specialist contractor required.",
    "pvc": "PVC plastics — toxic fumes when incinerated. Avoid thermal processing.",
    "bfo": "Brominated flame retardants — toxic fumes. Avoid shredding without ventilation.",
}

PROCESS_RULES = {
    "laptop": [
        {"step": 1, "action": "Battery removal", "reason": "Lithium batteries must be removed before shredding — fire risk"},
        {"step": 2, "action": "HDD/SSD data destruction", "reason": "Data security — degauss or shred storage media"},
        {"step": 3, "action": "RAM and PCB extraction", "reason": "High gold/silver content — economic priority"},
        {"step": 4, "action": "Screen separation", "reason": "LCD backlights may contain mercury"},
        {"step": 5, "action": "Chassis to aluminum smelting", "reason": "High-purity aluminum — economic recovery"},
    ],
    "smartphone": [
        {"step": 1, "action": "Battery removal", "reason": "Li-ion battery — fire risk in shredders"},
        {"step": 2, "action": "Data destruction", "reason": "Personal data security"},
        {"step": 3, "action": "PCB extraction", "reason": "Highest precious metal concentration"},
        {"step": 4, "action": "Screen and case separation", "reason": "Material segregation for downstream processing"},
    ],
    "monitor": [
        {"step": 1, "action": "CRT screen identification", "reason": "CRT glass contains lead — specialized handling"},
        {"step": 2, "action": "Backlight lamp removal (LCD)", "reason": "CCFL lamps contain mercury"},
        {"step": 3, "action": "PCB extraction", "reason": "Precious metal recovery"},
        {"step": 4, "action": "Metal chassis separation", "reason": "Steel/aluminum recovery"},
    ],
    "printer": [
        {"step": 1, "action": "Toner cartridge removal", "reason": "Toner dust respiratory hazard"},
        {"step": 2, "action": "PCB extraction", "reason": "Electronic component recovery"},
        {"step": 3, "action": "Metal frame separation", "reason": "Steel/aluminum bulk recovery"},
    ],
    "generic": [
        {"step": 1, "action": "Battery/capacitor identification", "reason": "Energy storage components — safety first"},
        {"step": 2, "action": "PCB and electronic component extraction", "reason": "Precious metal recovery"},
        {"step": 3, "action": "Metal/plastic separation", "reason": "Material stream segregation"},
    ],
}


class DecisionSupportService:
    """
    Generates recycling recommendations based on device type,
    material information, and operational rules.

    Disclaimer is always included — recommendations are guidance, not certified safety instructions.
    """

    def get_recommendations(
        self,
        device_type: Optional[str] = None,
        materials: Optional[list[dict]] = None,
        batch_id: Optional[str] = None,
        ai_prediction: Optional[dict] = None,
    ) -> dict:
        dtype = self._normalize(device_type)

        # Process steps
        steps = PROCESS_RULES.get(dtype, PROCESS_RULES["generic"])

        # Hazard detection
        hazard_flags = []
        if materials:
            for mat in materials:
                name = mat.get("material_name", "").lower()
                if name in HAZARDOUS_FLAGS:
                    hazard_flags.append(HAZARDOUS_FLAGS[name])

        # Device-specific hazard
        device_hazards = {
            "monitor": ["lead", "mercury"],
            "laptop": ["lead", "lithium"],
            "smartphone": ["lithium", "cobalt"],
            "printer": ["toner_dust"],
        }
        for hazard_key in device_hazards.get(dtype, []):
            msg = HAZARDOUS_FLAGS.get(hazard_key)
            if msg and msg not in hazard_flags:
                hazard_flags.append(msg)

        # Build recommendations
        recommendations = []
        reasoning = []

        for step in steps:
            recommendations.append({
                "priority": step["step"],
                "action": step["action"],
                "reason": step["reason"],
                "source": "rule_based",
            })
            reasoning.append(f"Step {step['step']}: {step['reason']}")

        # AI-augmented recommendation
        if ai_prediction and ai_prediction.get("prediction_type") == "actual_model":
            recommendations.append({
                "priority": len(recommendations) + 1,
                "action": f"AI Classification: {ai_prediction.get('prediction', 'N/A')}",
                "reason": "AI model prediction — verify visually before processing",
                "confidence": ai_prediction.get("confidence"),
                "source": "ai_model",
            })
            reasoning.append("AI model classification included — treat as advisory input only.")

        return {
            "batch_id": batch_id,
            "device_type": dtype,
            "recommendations": recommendations,
            "hazard_flags": hazard_flags,
            "reasoning": reasoning,
            "disclaimer": (
                "⚠️ IMPORTANT DISCLAIMER: These recommendations are AI/rule-based guidance for "
                "operational planning only. They do NOT constitute certified safety instructions, "
                "legal compliance documentation, or professional advice. "
                "Hazardous materials (marked ⚠️) MUST be handled by qualified professionals "
                "in accordance with applicable local regulations (WEEE, RoHS, Basel Convention)."
            ),
        }

    def _normalize(self, device_type: Optional[str]) -> str:
        if not device_type:
            return "generic"
        dt = device_type.lower().strip()
        mapping = {
            "laptop": "laptop", "notebook": "laptop",
            "phone": "smartphone", "mobile": "smartphone", "smartphone": "smartphone",
            "monitor": "monitor", "screen": "monitor",
            "printer": "printer",
        }
        return mapping.get(dt, "generic")
