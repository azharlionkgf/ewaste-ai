"""
E-Waste AI — Material Database (Stub)
=======================================
Scientifically sourced material composition data per device type.

Sources:
  - Cucchiella et al. (2015) "Recycling of WEEEs"
  - Graedel et al. (2011) "Recycling Rates of Metals"
  - European Environment Agency Reports
  - UNEP (2013) Metal Recycling Report

All values are ESTIMATES based on published literature.
Actual composition varies by manufacturer, model, and year.

Full implementation: Phase 6
"""

# Material composition estimates (grams per kg of device weight)
# Sources cited above. All values are estimates.
MATERIAL_COMPOSITION = {
    "smartphone": {
        "gold_g_per_kg":      0.034,   # Cucchiella et al. 2015
        "silver_g_per_kg":    0.350,
        "copper_g_per_kg":    15.0,
        "palladium_g_per_kg": 0.015,
        "lithium_g_per_kg":   3.50,
        "cobalt_g_per_kg":    7.00,
        "aluminum_g_per_kg":  25.0,
        "plastic_g_per_kg":   310.0,
        "glass_g_per_kg":     200.0,
        "source": "Cucchiella et al. (2015)",
    },
    "laptop": {
        "gold_g_per_kg":      0.015,
        "silver_g_per_kg":    0.189,
        "copper_g_per_kg":    20.0,
        "palladium_g_per_kg": 0.003,
        "lithium_g_per_kg":   2.00,
        "aluminum_g_per_kg":  180.0,
        "plastic_g_per_kg":   250.0,
        "source": "Graedel et al. (2011)",
    },
    "pcb_generic": {
        "gold_g_per_kg":      0.350,   # PCBs are richest in precious metals
        "silver_g_per_kg":    1.500,
        "copper_g_per_kg":    200.0,
        "palladium_g_per_kg": 0.100,
        "tin_g_per_kg":       30.0,
        "lead_g_per_kg":      20.0,
        "source": "UNEP (2013) Metal Recycling Report",
    },
    "battery_li": {
        "lithium_g_per_kg":   70.0,
        "cobalt_g_per_kg":    150.0,
        "manganese_g_per_kg": 80.0,
        "nickel_g_per_kg":    80.0,
        "copper_g_per_kg":    110.0,
        "source": "European Environment Agency",
    },
}


def get_material_composition(device_category: str) -> dict:
    """
    Return material composition estimates for a device category.
    Returns generic PCB data if category not found.
    All returned values are estimates.
    """
    return MATERIAL_COMPOSITION.get(
        device_category,
        MATERIAL_COMPOSITION.get("pcb_generic", {})
    )


def estimate_recovery_weights(device_category: str, weight_kg: float) -> dict:
    """
    Estimate recoverable material weights for a device.

    Args:
        device_category: Device type string
        weight_kg: Total device weight in kg

    Returns:
        dict of material → estimated weight in grams
        Always includes is_estimate=True flag.
    """
    composition = get_material_composition(device_category)
    result = {"is_estimate": True, "weight_kg": weight_kg}

    for key, value in composition.items():
        if key.endswith("_g_per_kg") and isinstance(value, (int, float)):
            material = key.replace("_g_per_kg", "")
            result[f"{material}_g"] = round(value * weight_kg, 4)

    result["source"] = composition.get("source", "Published literature")
    return result
