# Predictive Analytics Documentation
## E-Waste AI Platform — Phase 6

---

## Purpose

The Predictive Analytics module computes time-based trend metrics from historical operational data.
It is designed to surface patterns that support operational planning, not to make binding forecasts.

---

## Trend Computation (`compute_trends`)

### Inputs

| Parameter | Default | Description |
|-----------|---------|-------------|
| `days` | 30 | Number of days in the analysis period |

### Outputs (success path)

```python
{
    "period_days": 30,
    "batches_in_period": int,       # Number of WasteBatch records in period
    "total_weight_period_kg": float, # Sum of batch weights in period
    "total_recovered_period_g": float, # Sum of RecoveryRecord.recovered_quantity_g
    "prior_period_weight_kg": float, # Weight in the equivalent prior period
    "weight_change_pct": float | None, # % change vs prior period (None if no prior data)
    "data_sufficient": bool,         # True if batches_in_period >= 3
    "insufficient_data_note": str | None, # Explanation if data_sufficient is False
    "timestamp": str,                # ISO 8601 UTC timestamp of computation
}
```

### Outputs (error / DB unavailable path)

```python
{
    "error": str,                    # Exception message
    "data_sufficient": False,
    "period_days": int,              # Echo of requested period
    "batches_in_period": 0,
    "insufficient_data_note": str,   # Standard explanation of unavailability
}
```

---

## Insufficient Data Handling

A result is marked `data_sufficient: False` when:
- Fewer than **3 batches** exist in the requested period (not enough for a trend).
- A DB error prevents querying the data (schema mismatch, connection failure, etc.).

In both cases, `insufficient_data_note` explains why trends are unavailable.
The UI displays a clear **"Insufficient data"** state rather than showing empty charts or null values.

---

## Supported Trend Types (v1.0)

| Metric | Source | Availability |
|--------|--------|-------------|
| Incoming e-waste volume | `WasteBatch.total_weight_kg` | Requires ≥ 3 batches |
| Material recovery total | `RecoveryRecord.recovered_quantity_g` | Requires ≥ 1 record |
| Weight change vs prior period | Computed from two periods | Requires ≥ 1 batch in prior period |

---

## Forecasting

Demand/volume forecasting (beyond trend comparison) is explicitly marked as **unavailable** when:
- Fewer than 90 days of data exist.
- Fewer than 10 batch records exist.

The UI shows an explanation rather than fabricated forecast values.

---

## Limitations

1. Trends are computed from operational DB records only. External factors (economic, regulatory, seasonal) are not modelled.
2. A short dataset (< 30 days) will show high variance. Treat short-period trends as preliminary.
3. The system does not apply time-series models (ARIMA, Prophet) in v1.0 — only period-over-period comparison.
4. The test environment uses an older DB schema; in that context, `compute_trends()` returns the error path with appropriate flags.
