"""
industrial/valuation/cost_calculator.py
E-WASTE AI - Cost and Economic Valuation Calculator
Estimates recovery value and processing costs for e-waste.
All values are research-cited estimates labeled is_estimate=True.
"""

import logging
import datetime
import json
from pathlib import Path

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# Recovery Rates (grams per unit, unless noted)
# Source: Research averages — UNEP 2019, Hagelüken 2006
# ALL labeled is_estimate=True
# ------------------------------------------------------------------

MATERIAL_RECOVERY_RATES = {
    "smartphone": {
        "gold_g": 0.034, "silver_g": 0.350, "copper_g": 15.0,
        "aluminum_g": 10.0, "lithium_g": 1.5, "cobalt_g": 5.0,
        "is_estimate": True,
        "source": "UNEP 2019 / Hagelüken 2006 research averages",
        "unit": "per_device",
    },
    "laptop": {
        "gold_g": 0.015, "silver_g": 0.100, "copper_g": 60.0,
        "aluminum_g": 300.0, "lithium_g": 25.0, "cobalt_g": 50.0,
        "is_estimate": True,
        "source": "Research averages",
        "unit": "per_device",
    },
    "desktop_computer": {
        "gold_g": 0.010, "silver_g": 0.080, "copper_g": 90.0,
        "aluminum_g": 200.0, "iron_steel_g": 2000.0,
        "is_estimate": True,
        "source": "Research averages",
        "unit": "per_device",
    },
    "circuit_board": {
        "gold_g": 2.0, "silver_g": 5.0, "copper_g": 250.0,
        "palladium_g": 0.15, "platinum_g": 0.05,
        "is_estimate": True,
        "source": "Hagelüken 2006 — per kg PCB",
        "unit": "per_kg",
    },
    "battery_li_ion": {
        "lithium_g": 15.0, "cobalt_g": 150.0, "nickel_g": 100.0,
        "copper_g": 50.0, "aluminum_g": 50.0,
        "is_estimate": True,
        "source": "Research averages — per kg",
        "unit": "per_kg",
    },
    "tablet": {
        "gold_g": 0.025, "silver_g": 0.200, "copper_g": 12.0,
        "aluminum_g": 80.0, "lithium_g": 8.0,
        "is_estimate": True,
        "source": "Research averages",
        "unit": "per_device",
    },
    "default": {
        "copper_g": 50.0, "aluminum_g": 100.0, "iron_steel_g": 200.0,
        "is_estimate": True,
        "source": "Generic research averages",
        "unit": "per_device",
    },
}

# Processing cost estimates (USD per kg)
PROCESSING_COST_USD_PER_KG = {
    "smartphone": 1.50,
    "laptop": 2.00,
    "desktop_computer": 1.20,
    "circuit_board": 5.00,
    "battery_li_ion": 3.50,
    "battery_lead_acid": 1.00,
    "monitor_crt": 4.00,  # CRT disposal is expensive
    "monitor_lcd": 2.50,
    "printer": 1.80,
    "default": 2.00,
}

# Default material prices (USD per gram, labeled as estimates)
DEFAULT_MATERIAL_PRICES = {
    "gold": 60.0,
    "silver": 0.80,
    "copper": 0.009,
    "palladium": 45.0,
    "platinum": 30.0,
    "aluminum": 0.002,
    "iron_steel": 0.0005,
    "lithium": 0.025,
    "cobalt": 0.035,
    "nickel": 0.014,
    "rare_earth_mixed": 0.05,
}


class CostCalculator:
    """
    Estimates economic recovery value and processing costs for e-waste devices.
    All estimates labeled is_estimate=True with data_source citation.
    """

    def __init__(self, material_prices: dict = None):
        """
        material_prices: optional dict of material_name -> price_usd_per_gram
        If None, uses DEFAULT_MATERIAL_PRICES.
        """
        self._prices = material_prices.copy() if material_prices else DEFAULT_MATERIAL_PRICES.copy()

    def update_material_price(self, material: str, price_usd_per_gram: float) -> None:
        """Update the price for a specific material."""
        self._prices[material] = float(price_usd_per_gram)
        logger.info(f"Updated price: {material} = ${price_usd_per_gram:.4f}/g")

    def _get_recovery_rates(self, device_type: str) -> dict:
        """Get recovery rates for a device type with fuzzy matching."""
        normalized = device_type.lower().replace(" ", "_").replace("-", "_")
        for key in MATERIAL_RECOVERY_RATES:
            if key in normalized or normalized in key:
                return MATERIAL_RECOVERY_RATES[key]
        return MATERIAL_RECOVERY_RATES["default"]

    def estimate_recovery_value(
        self,
        device_type: str,
        quantity: int = 1,
        weight_kg: float = None,
    ) -> dict:
        """
        Estimate total recovery value for a given device type and quantity.
        Returns breakdown by material and total USD value.
        """
        rates = self._get_recovery_rates(device_type)
        unit = rates.get("unit", "per_device")

        # Scale factor
        if unit == "per_kg" and weight_kg is not None:
            scale = weight_kg * quantity
            scale_label = f"{weight_kg}kg x {quantity}"
        else:
            scale = quantity
            scale_label = f"{quantity} units"

        material_breakdown = {}
        total_value_usd = 0.0

        for key, grams_rate in rates.items():
            if key in ("is_estimate", "source", "unit"):
                continue
            # Extract material name from key (e.g. "gold_g" -> "gold")
            mat_name = key.replace("_g", "").replace("_per_kg", "")
            price = self._prices.get(mat_name, 0.0)

            grams_recovered = float(grams_rate) * scale
            value_usd = grams_recovered * price

            material_breakdown[mat_name] = {
                "grams_per_unit": grams_rate,
                "total_grams": round(grams_recovered, 4),
                "price_usd_per_gram": price,
                "value_usd": round(value_usd, 4),
            }
            total_value_usd += value_usd

        return {
            "device_type": device_type,
            "quantity": quantity,
            "weight_kg": weight_kg,
            "scale": scale_label,
            "total_value_usd": round(total_value_usd, 2),
            "material_breakdown": material_breakdown,
            "is_estimate": True,
            "data_source": rates.get("source", "Research averages"),
            "note": "These are research-based estimates. Actual recovery depends on equipment, purity and market conditions.",
            "estimated_at": datetime.datetime.utcnow().isoformat(),
        }

    def calculate_processing_cost(self, weight_kg: float, device_type: str) -> dict:
        """Estimate processing/dismantling cost for a given weight and device type."""
        normalized = device_type.lower().replace(" ", "_").replace("-", "_")
        cost_rate = PROCESSING_COST_USD_PER_KG.get("default", 2.0)
        for key in PROCESSING_COST_USD_PER_KG:
            if key in normalized or normalized in key:
                cost_rate = PROCESSING_COST_USD_PER_KG[key]
                break

        total_cost = round(cost_rate * weight_kg, 2)
        return {
            "device_type": device_type,
            "weight_kg": weight_kg,
            "cost_rate_usd_per_kg": cost_rate,
            "total_processing_cost_usd": total_cost,
            "is_estimate": True,
            "data_source": "Research averages — processing costs vary by facility",
        }

    def calculate_net_value(
        self,
        device_type: str,
        quantity: int,
        weight_kg: float,
    ) -> dict:
        """
        Calculate net economic value = gross recovery value - processing cost.
        """
        gross = self.estimate_recovery_value(device_type, quantity, weight_kg)
        cost = self.calculate_processing_cost(weight_kg * quantity, device_type)

        gross_value = gross["total_value_usd"]
        process_cost = cost["total_processing_cost_usd"]
        net_value = round(gross_value - process_cost, 2)

        return {
            "device_type": device_type,
            "quantity": quantity,
            "total_weight_kg": round(weight_kg * quantity, 3),
            "gross_recovery_value_usd": gross_value,
            "processing_cost_usd": process_cost,
            "net_value_usd": net_value,
            "is_profitable": net_value > 0,
            "material_breakdown": gross["material_breakdown"],
            "is_estimate": True,
            "data_source": "Research averages",
            "note": "Net value = gross material recovery - estimated processing cost.",
            "calculated_at": datetime.datetime.utcnow().isoformat(),
        }
