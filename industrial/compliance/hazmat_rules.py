"""
industrial/compliance/hazmat_rules.py
E-WASTE AI - Hazardous Materials Rules and Compliance
RoHS / WEEE directive hazmat handling guidelines.
"""

import logging
import datetime

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# Hazardous Material Definitions (RoHS / WEEE Directive)
# ------------------------------------------------------------------

HAZMAT_MATERIALS = {
    "mercury": {
        "cas_number": "7439-97-6",
        "description": "Mercury — used in fluorescent backlights (CFL, CCFL), switches, thermostats.",
        "max_concentration_ppm": 1000,
        "handling_requirements": [
            "Sealed container with airtight closure",
            "Mercury-specific PPE (respirator, gloves, goggles)",
            "No open drains or sinks nearby",
            "Use mercury spill kit for accidents",
        ],
        "disposal_method": "Certified mercury recycler or hazmat disposal facility",
        "regulatory_ref": "RoHS Directive 2011/65/EU — Annex II; WEEE Directive 2012/19/EU",
        "health_risk": "HIGH — neurotoxin, bioaccumulates",
    },
    "lead": {
        "cas_number": "7439-92-1",
        "description": "Lead — in solder (pre-RoHS), CRT glass, batteries.",
        "max_concentration_ppm": 1000,
        "handling_requirements": [
            "Gloves and dust mask when handling CRT or old solder joints",
            "No eating/drinking in handling area",
            "Hand washing protocol after handling",
        ],
        "disposal_method": "Lead smelter / certified battery recycler",
        "regulatory_ref": "RoHS Directive 2011/65/EU — Annex II",
        "health_risk": "HIGH — neurotoxin, especially for children",
    },
    "cadmium": {
        "cas_number": "7440-43-9",
        "description": "Cadmium — in NiCd batteries, some semiconductors, pigments.",
        "max_concentration_ppm": 100,
        "handling_requirements": [
            "Respirator required when processing NiCd batteries",
            "Cadmium-designated waste bins",
            "Fire suppression nearby — cadmium fumes from burning are toxic",
        ],
        "disposal_method": "NiCd battery recycler or hazmat facility",
        "regulatory_ref": "RoHS Directive 2011/65/EU — Annex II",
        "health_risk": "HIGH — carcinogen, kidney damage",
    },
    "chromium_vi": {
        "cas_number": "18540-29-9",
        "description": "Hexavalent chromium — in some metal coatings, dyes.",
        "max_concentration_ppm": 1000,
        "handling_requirements": [
            "Chemical-resistant gloves",
            "Avoid inhalation of dust",
            "Eye protection required",
        ],
        "disposal_method": "Chromium waste reduction facility",
        "regulatory_ref": "RoHS Directive 2011/65/EU — Annex II",
        "health_risk": "HIGH — carcinogen",
    },
    "PBB": {
        "cas_number": "various",
        "description": "Polybrominated biphenyls — flame retardants in older plastic casings.",
        "max_concentration_ppm": 1000,
        "handling_requirements": [
            "Do not incinerate — produces toxic dioxins",
            "Segregate from general plastics",
        ],
        "disposal_method": "Specialised halogenated plastics recycler",
        "regulatory_ref": "RoHS Directive 2011/65/EU — Annex II",
        "health_risk": "MEDIUM-HIGH — endocrine disruptor",
    },
    "PBDE": {
        "cas_number": "various",
        "description": "Polybrominated diphenyl ethers — flame retardants in PCBs and plastics.",
        "max_concentration_ppm": 1000,
        "handling_requirements": [
            "Do not shred without proper ventilation",
            "Do not incinerate",
        ],
        "disposal_method": "Specialised halogenated plastics recycler",
        "regulatory_ref": "RoHS Directive 2011/65/EU — Annex II",
        "health_risk": "MEDIUM-HIGH — endocrine disruptor, persistent organic pollutant",
    },
}

# ------------------------------------------------------------------
# Device → Likely Hazmat Mapping
# ------------------------------------------------------------------

DEVICE_HAZMAT_MAP = {
    "smartphone": ["lead", "PBB", "PBDE"],
    "laptop": ["lead", "mercury", "PBB", "PBDE"],
    "desktop_computer": ["lead", "PBB", "PBDE"],
    "tablet": ["lead", "PBB", "PBDE"],
    "monitor_crt": ["lead", "mercury"],
    "monitor_lcd": ["mercury"],
    "television_crt": ["lead", "mercury"],
    "television_lcd": ["mercury", "PBB", "PBDE"],
    "printer": ["lead", "PBB", "PBDE"],
    "battery_nicd": ["cadmium"],
    "battery_lead_acid": ["lead"],
    "battery_li_ion": ["lead"],
    "circuit_board": ["lead", "cadmium", "chromium_vi", "PBB", "PBDE"],
    "charger": ["lead", "PBB", "PBDE"],
    "cable": ["lead", "PBB", "PBDE"],
    "default": ["lead", "PBB", "PBDE"],
}


class HazmatChecker:
    """Checks hazardous material presence and generates compliance guidance."""

    def check_device(self, device_type: str) -> dict:
        """Return hazmat materials and handling instructions for a device type."""
        normalized = device_type.lower().replace(" ", "_").replace("-", "_")

        # Match device type
        matched_key = "default"
        for key in DEVICE_HAZMAT_MAP:
            if key in normalized or normalized in key:
                matched_key = key
                break

        hazmat_keys = DEVICE_HAZMAT_MAP[matched_key]
        materials = {k: HAZMAT_MATERIALS[k] for k in hazmat_keys if k in HAZMAT_MATERIALS}

        all_handling = []
        for m in materials.values():
            all_handling.extend(m.get("handling_requirements", []))

        return {
            "device_type": device_type,
            "matched_profile": matched_key,
            "hazmat_materials_present": list(materials.keys()),
            "material_details": materials,
            "combined_handling_instructions": list(dict.fromkeys(all_handling)),
            "compliance_notes": [
                "Follow RoHS Directive 2011/65/EU restrictions.",
                "Follow WEEE Directive 2012/19/EU disposal requirements.",
                "Segregate hazmat devices before processing.",
                "Train handlers in hazmat awareness.",
            ],
            "checked_at": datetime.datetime.utcnow().isoformat(),
        }

    def get_disposal_instructions(self, material_name: str) -> dict:
        """Return disposal instructions for a specific hazardous material."""
        mat = HAZMAT_MATERIALS.get(material_name)
        if not mat:
            raise KeyError(f"Material '{material_name}' not in hazmat registry. Known: {list(HAZMAT_MATERIALS.keys())}")
        return {"material": material_name, **mat}

    def generate_hazmat_report(self, batch_items: list) -> dict:
        """
        Generate a consolidated hazmat report for a list of batch items.
        batch_items: list of dicts with 'device_type' key.
        """
        all_hazmats = set()
        item_reports = []

        for item in batch_items:
            device_type = item.get("device_type", "unknown")
            report = self.check_device(device_type)
            item_reports.append({
                "device_type": device_type,
                "hazmats": report["hazmat_materials_present"],
            })
            all_hazmats.update(report["hazmat_materials_present"])

        return {
            "total_items": len(batch_items),
            "unique_hazmat_types": sorted(all_hazmats),
            "hazmat_count": len(all_hazmats),
            "item_breakdown": item_reports,
            "risk_level": "HIGH" if {"mercury", "cadmium", "chromium_vi"} & all_hazmats else "MEDIUM",
            "recommendation": (
                "Requires certified hazmat disposal facility."
                if {"mercury", "cadmium"} & all_hazmats
                else "Standard WEEE-compliant recycler acceptable."
            ),
            "generated_at": datetime.datetime.utcnow().isoformat(),
        }
