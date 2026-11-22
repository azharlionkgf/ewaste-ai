"""
E-Waste AI — Economic Engine (Stub)
======================================
Estimates economic recovery value based on material weights
and approximate market prices.

IMPORTANT: All valuations are ESTIMATES.
Market prices fluctuate daily. These are indicative values only.
Price data: approximate LME / Kitco historical averages.

Full implementation: Phase 6
"""

# Approximate market prices (USD) — update manually or via API in production
# Source: LME / Kitco approximate 2024-2025 averages
MARKET_PRICES = {
    "gold_usd_per_g":      85.00,   # ~$2,650/troy oz
    "silver_usd_per_g":    0.96,    # ~$30/troy oz
    "copper_usd_per_g":    0.0095,  # ~$9.50/kg
    "palladium_usd_per_g": 33.80,   # ~$1,050/troy oz
    "lithium_usd_per_g":   0.012,   # ~$12/kg
    "cobalt_usd_per_g":    0.025,   # ~$25/kg
    "platinum_usd_per_g":  31.0,
    "source": "Approximate LME/Kitco 2024-2025 averages",
    "is_estimate": True,
}


def calculate_recovery_value(material_weights_g: dict) -> dict:
    """
    Calculate estimated economic recovery value.

    Args:
        material_weights_g: dict of material -> weight in grams

    Returns:
        dict with per-material values and total (all in USD)
        Always includes is_estimate=True.
    """
    result = {
        "is_estimate": True,
        "currency": "USD",
        "price_source": MARKET_PRICES["source"],
        "breakdown": {},
        "total_gross_usd": 0.0,
    }

    for material, weight_g in material_weights_g.items():
        if not isinstance(weight_g, (int, float)):
            continue
        price_key = f"{material}_usd_per_g"
        if price_key in MARKET_PRICES:
            value = round(weight_g * MARKET_PRICES[price_key], 4)
            result["breakdown"][material] = {
                "weight_g": weight_g,
                "price_usd_per_g": MARKET_PRICES[price_key],
                "value_usd": value,
            }
            result["total_gross_usd"] += value

    result["total_gross_usd"] = round(result["total_gross_usd"], 2)
    return result
