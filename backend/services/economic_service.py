"""
E-Waste AI — Economic Intelligence Engine (Phase 4 Task 6)
===========================================================
Estimates financial value of recovered materials and processing costs.
All prices are indicative market references — clearly labeled.
Never fabricates financial results.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

# ── Indicative Market Prices ───────────────────────────────────────────
# Source: indicative global commodity prices (USD).
# These are REFERENCE values and change daily.
# In production, integrate a real-time commodity price API.
# Timestamp indicates when these were last manually updated.

INDICATIVE_PRICES_USD_PER_G = {
    "gold": 60.0,           # ~$1,850/troy oz → ~$60/g
    "silver": 0.78,         # ~$24/troy oz → ~$0.78/g
    "platinum": 29.0,
    "palladium": 43.0,
    "cobalt": 0.033,        # ~$33,000/metric ton → ~$0.033/g
    "lithium": 0.015,       # LCE pricing, varies widely
    "copper": 0.009,        # ~$9,000/metric ton
    "aluminum": 0.0022,     # ~$2,200/metric ton
    "steel": 0.0005,        # ~$500/metric ton (scrap)
    "tin": 0.027,
    "indium": 0.17,
    "neodymium": 0.08,
    "dysprosium": 0.3,
    "plastic": 0.0001,      # mixed plastic recycling value — very low
    "glass": 0.00005,       # mixed glass recycling
}

PRICE_DATA_DATE = "2024-01-15"
PRICE_SOURCE = "Indicative commodity market references (not live prices)"

# ── Processing Cost Estimates ──────────────────────────────────────────
# Typical processing costs in USD per kg of e-waste processed.
# Source: Industry reports and academic studies.

PROCESSING_COSTS_USD_PER_KG = {
    "sorting": 0.50,
    "dismantling": 2.50,
    "shredding": 1.00,
    "hydrometallurgical": 15.00,
    "pyrometallurgical": 8.00,
    "battery_recycling": 5.00,
    "default": 4.00,
}


class EconomicIntelligenceService:
    """
    Estimates financial recovery value and processing costs for e-waste.

    All estimates clearly indicate:
    - Price source and timestamp
    - That prices are indicative, not real-time
    - That actual costs depend on processing methods and scale
    """

    def analyze_batch_economics(
        self,
        materials: list[dict],
        weight_kg: float,
        processing_type: str = "default",
        custom_prices: Optional[dict] = None,
    ) -> dict:
        """
        Estimate economic value for a batch.

        Args:
            materials: List of material dicts with material_name and recoverable_quantity_g
            weight_kg: Total batch weight in kg
            processing_type: Processing method for cost estimation
            custom_prices: Optional override prices (USD/g)

        Returns:
            Economic analysis with gross value, costs, net value, and disclaimers
        """
        prices = {**INDICATIVE_PRICES_USD_PER_G, **(custom_prices or {})}

        material_breakdown = []
        gross_value_usd = 0.0

        for mat in materials:
            name = mat.get("material_name", "")
            qty_g = mat.get("recoverable_quantity_g", 0.0)
            price = prices.get(name)

            if price and qty_g > 0:
                value_usd = qty_g * price
                gross_value_usd += value_usd
                material_breakdown.append({
                    "material": name,
                    "quantity_g": round(qty_g, 4),
                    "price_per_g_usd": price,
                    "estimated_value_usd": round(value_usd, 4),
                    "price_source": PRICE_SOURCE,
                    "price_date": PRICE_DATA_DATE,
                })
            else:
                material_breakdown.append({
                    "material": name,
                    "quantity_g": round(qty_g, 4),
                    "price_per_g_usd": None,
                    "estimated_value_usd": None,
                    "note": f"No price reference available for '{name}'",
                })

        # Processing costs
        cost_per_kg = PROCESSING_COSTS_USD_PER_KG.get(
            processing_type, PROCESSING_COSTS_USD_PER_KG["default"]
        )
        processing_cost = cost_per_kg * weight_kg
        net_value = gross_value_usd - processing_cost

        assumptions = [
            f"Prices as of {PRICE_DATA_DATE} — not real-time values",
            f"Processing cost: ${cost_per_kg}/kg ({processing_type} method)",
            "Recovery rates per published composition surveys",
            "Excludes transport, compliance, and overhead costs",
            "Market prices are for refined/pure materials — actual smelter payouts vary",
        ]

        return {
            "weight_kg": weight_kg,
            "gross_recovery_value_usd": round(gross_value_usd, 2),
            "estimated_processing_cost_usd": round(processing_cost, 2),
            "net_value_usd": round(net_value, 2),
            "material_breakdown": material_breakdown,
            "price_sources": [PRICE_SOURCE],
            "price_data_date": PRICE_DATA_DATE,
            "assumptions": assumptions,
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "disclaimer": (
                "⚠️ Financial Disclaimer: These are ESTIMATES using indicative commodity prices. "
                "Actual recovery values depend on current market prices, material purity, "
                "processing efficiency, and smelter agreements. "
                "Do not use for accounting or financial decisions without verification."
            ),
        }

    def get_price_reference(self, material_name: str) -> Optional[dict]:
        """Get price reference for a specific material."""
        price = INDICATIVE_PRICES_USD_PER_G.get(material_name.lower())
        if price is None:
            return None
        return {
            "material": material_name,
            "price_per_g_usd": price,
            "price_per_kg_usd": price * 1000,
            "source": PRICE_SOURCE,
            "date": PRICE_DATA_DATE,
            "note": "Indicative reference price only — verify with current market data",
        }

    def all_prices(self) -> dict:
        return {
            "prices_usd_per_g": INDICATIVE_PRICES_USD_PER_G,
            "source": PRICE_SOURCE,
            "date": PRICE_DATA_DATE,
        }
