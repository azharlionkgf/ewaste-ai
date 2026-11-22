"""
E-Waste AI — Device Database (Stub)
=====================================
Scientific reference data for known e-waste device categories.
Sources: Global E-waste Monitor, Graedel et al., EU WEEE Directive.

Full implementation: Phase 6
"""

# E-waste device categories with average weight (kg) per unit
# Source: Baldé et al. (2017) Global E-waste Monitor
DEVICE_CATEGORIES = {
    "smartphone":    {"avg_weight_kg": 0.14, "hazard_level": "medium"},
    "tablet":        {"avg_weight_kg": 0.47, "hazard_level": "medium"},
    "laptop":        {"avg_weight_kg": 2.10, "hazard_level": "medium"},
    "desktop":       {"avg_weight_kg": 7.80, "hazard_level": "medium"},
    "monitor_lcd":   {"avg_weight_kg": 4.50, "hazard_level": "medium"},
    "monitor_crt":   {"avg_weight_kg": 15.0, "hazard_level": "high"},
    "tv_led":        {"avg_weight_kg": 10.5, "hazard_level": "medium"},
    "tv_plasma":     {"avg_weight_kg": 30.0, "hazard_level": "high"},
    "battery_li":    {"avg_weight_kg": 0.05, "hazard_level": "high"},
    "battery_lead":  {"avg_weight_kg": 15.0, "hazard_level": "critical"},
    "pcb_generic":   {"avg_weight_kg": 0.30, "hazard_level": "high"},
    "charger":       {"avg_weight_kg": 0.08, "hazard_level": "low"},
    "cable":         {"avg_weight_kg": 0.05, "hazard_level": "low"},
    "printer":       {"avg_weight_kg": 5.00, "hazard_level": "medium"},
    "other":         {"avg_weight_kg": 1.00, "hazard_level": "medium"},
}

# E-waste classification labels (used for model training)
CLASSIFICATION_LABELS = sorted(DEVICE_CATEGORIES.keys())
NUM_CLASSES = len(CLASSIFICATION_LABELS)


def get_device_info(category: str) -> dict:
    """Return device metadata for a given category."""
    return DEVICE_CATEGORIES.get(category, DEVICE_CATEGORIES["other"])


def get_all_labels() -> list:
    """Return sorted list of all classification labels."""
    return CLASSIFICATION_LABELS
