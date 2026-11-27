# Economic Intelligence Documentation
## E-Waste AI Platform — Phase 6

---

## Purpose

The Economic Intelligence module provides cost/value estimation for e-waste processing operations.
All figures are **estimates** — not financial guarantees. They are labelled accordingly throughout
the UI and API responses.

---

## Material Prices

### Source

Prices are stored in `MATERIAL_PRICES_USD_PER_G` with metadata:

```python
PRICE_SOURCE = "LME / commodity reference — indicative only, NOT live market prices"
PRICE_DATE   = "2024-01-15"
```

> [!CAUTION]
> These are **reference prices** from January 2024. Metal commodity prices fluctuate daily.
> Do not use these figures for financial reporting, procurement decisions, or regulatory submissions.
> Always verify against current market data before making commercial decisions.

### Reference Price Table (USD per gram, Jan 2024)

| Material | Price (USD/g) | Source |
|---------|-------------|--------|
| copper | 0.0085 | LME copper cash |
| aluminium | 0.0024 | LME aluminium cash |
| steel_iron | 0.0005 | Hot-rolled coil reference |
| gold | 63.50 | London PM fix |
| silver | 0.76 | London silver fix |
| rare_earth_metals | 0.082 | USGS / average REE basket |
| lithium | 0.015 | Lithium carbonate spot |
| plastics | 0.0003 | Mixed plastics bale |
| glass | 0.00015 | Cullet reference |

---

## Processing Cost Estimation

### Method (`estimate_processing_cost`)

```
labour_cost     = labour_hours × LABOUR_RATE_PER_HOUR
transport_cost  = transport_km × TRANSPORT_RATE_PER_KM
handling_cost   = device_count × HANDLING_COST_PER_DEVICE
overhead_cost   = weight_kg × OVERHEAD_PER_KG
total_cost      = sum of above
```

### Default Rate Parameters

| Parameter | Default Value | Unit |
|-----------|-------------|------|
| Labour rate | 15.00 USD | per hour |
| Transport rate | 0.50 USD | per km |
| Handling cost | 2.00 USD | per device |
| Overhead | 0.10 USD | per kg |

> [!NOTE]
> These defaults reflect typical small-to-medium facility costs in a generic market.
> Actual costs vary significantly by country, facility size, and equipment.

---

## Profit/Loss Estimation

```
gross_recovery_value = sum(material_recovered_g × price_per_g)
net_value            = gross_recovery_value - total_processing_cost
```

The UI shows this as an **estimate** with:
- Price source label
- Price date
- Disclaimer that actual market prices apply

---

## Disclaimer (shown in all API responses)

> ESTIMATE ONLY — Figures are indicative. Actual recovery, processing costs and market
> prices will differ. Do not use for financial reporting or compliance purposes.

---

## Configuration

Material prices can be updated by operators via the Settings page. User-configured prices are:
- Stored in the application database (future implementation).
- Tagged with `value_source: "user_configured"` and a last-updated timestamp.
- Never silently overwritten by system defaults.
