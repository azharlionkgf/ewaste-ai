# Material Intelligence Documentation
## E-Waste AI Platform — Phase 6

---

## Purpose

The Material Knowledge Base (KB) provides structured, literature-sourced information about
the material composition of common e-waste device categories. It enables recovery estimation
and economic analysis without requiring a trained model for every device type.

---

## Knowledge Base Structure

Each entry in `MATERIAL_KNOWLEDGE_BASE` contains:

```python
{
    "laptop": {
        "source": "UNEP 2019 / EEA E-waste Statistics",
        "confidence": "medium",
        "avg_weight_kg": 2.5,
        "components": ["PCB", "battery", "display", "chassis", "PSU", "storage", "keyboard"],
        "material_composition_percent": {
            "steel_iron": 20.0,
            "aluminium": 14.0,
            "copper": 7.0,
            "plastics": 23.0,
            "glass": 5.0,
            "rare_earth_metals": 0.3,
            "gold": 0.003,
            "silver": 0.015,
            "lithium": 0.4,
            "other": 30.282,
        },
        "hazardous_substances": ["lead", "mercury", "cadmium", "brominated_flame_retardants"],
    }
}
```

---

## Supported Device Types (v1.0)

| Device Type | Source | Confidence | Avg Weight (kg) |
|------------|--------|------------|-----------------|
| `laptop` | UNEP 2019 / EEA | medium | 2.5 |
| `desktop` | UNEP 2019 / EPA | medium | 8.0 |
| `mobile_phone` | Öko-Institut 2021 | medium | 0.18 |
| `television` | EEA 2020 | medium | 12.0 |
| `printer` | UNEP 2019 | low | 5.0 |
| `battery_pack` | EPA / IEC | high | 1.5 |

> [!NOTE]
> Composition percentages represent **population averages** across many device models.
> Actual composition of individual devices varies significantly.

---

## Provenance & Confidence

All KB entries carry a `confidence` field:

| Confidence | Meaning |
|-----------|---------|
| `high` | Based on multiple independent sources with consistent values |
| `medium` | Based on 1–2 sources; moderate variation expected |
| `low` | Based on limited or older data; use with caution |

---

## Limitations

1. **Not device-specific:** Composition is an average for the category, not for a specific model/brand.
2. **Not real-time:** Data reflects publications available up to the KB version date.
3. **Rounding:** Composition percentages may not sum to exactly 100% due to rounding in sources.
4. **Unknown devices:** Devices not in the KB return `available: False`. Do not extrapolate from similar devices without explicit justification.
5. **Regional variation:** E-waste composition may vary by region, year of manufacture, and product generation.

---

## References

- UNEP (2019). *A New Circular Vision for Electronics: Time for a Global Reboot.* UN Environment Programme.
- EEA (2020). *Waste electrical and electronic equipment statistics.* European Environment Agency.
- EPA (2021). *Electronics Stewardship.* US Environmental Protection Agency.
- Öko-Institut (2021). *Material composition of mobile phones.* Öko-Institut e.V., Freiburg.
- IEC (2019). *Secondary lithium-ion cells and batteries.* International Electrotechnical Commission.
