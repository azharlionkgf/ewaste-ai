# Recovery Optimization Documentation
## E-Waste AI Platform — Phase 6

---

## Purpose

The Recovery Optimization Engine provides decision-support for e-waste processing operations.
It does **not** make autonomous decisions — it surfaces recommended actions with traceable
reasoning so that operators can make informed choices.

---

## Recovery Estimation Methodology

### Formula

```
estimated_recovered_g(material) =
    device_weight_kg × 1000
    × composition_percent(material) / 100
    × recovery_efficiency(material)
    × condition_factor(condition)
```

### Recovery Efficiency Table (`RECOVERY_EFFICIENCY`)

| Material | Efficiency | Notes |
|----------|-----------|-------|
| steel_iron | 0.90 | High recovery via magnetic separation |
| aluminium | 0.85 | Established smelting process |
| copper | 0.80 | Pyrometallurgy / hydrometallurgy |
| plastics | 0.60 | Mixed fraction, varies by type |
| glass | 0.70 | Requires sorting by type |
| rare_earth_metals | 0.30 | Technically challenging; specialist facility required |
| gold | 0.75 | Wet chemistry / fire assay |
| silver | 0.70 | Wet chemistry |
| lithium | 0.50 | Battery-specific hydrometallurgy |

> [!IMPORTANT]
> These are industry-average efficiencies from published literature.
> Actual facility efficiency may differ significantly based on equipment, scale, and operator skill.

### Condition Factors

| Condition | Factor | Description |
|-----------|--------|-------------|
| `good` | 1.0 | Device functional or near-functional; minimal corrosion |
| `fair` | 0.9 | Moderate wear; some components may be damaged |
| `poor` | 0.75 | Significant physical damage or corrosion |
| (default) | 0.85 | Unknown condition; conservative estimate |

---

## Recovery Planning (`recommend_recovery_plan`)

For a given batch, the engine:

1. Queries the DB for all devices in the batch.
2. For each device, looks up KB composition and applies the estimation formula.
3. Aggregates by material across all devices.
4. Identifies the **top 3 materials by estimated value**.
5. Flags any hazardous substances present.
6. Returns recommended sorting priorities with rationale.

If the batch is not found or the DB is unavailable, returns `{"available": False, ...}`.

---

## Efficiency Tracking

The engine supports recording **measured recovery** (via `RecoveryRecord`) for later comparison
against estimates. This enables:

- Calculating actual vs. estimated recovery ratio.
- Identifying systematic over/under-estimation by device type.
- Improving future estimates through operational feedback.

> [!WARNING]
> Estimates are **never** updated retroactively based on measured data without explicit operator confirmation.
> Measured values are stored separately and never overwrite estimated values.

---

## Limitations

1. Estimates are batch-level averages. Individual device recovery may vary.
2. Processing constraints (equipment availability, throughput) are not modelled.
3. Cross-contamination between material streams is not accounted for.
4. The engine does not replace the judgment of a certified recycling engineer.
