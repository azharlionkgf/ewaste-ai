# Anomaly Detection Documentation
## E-Waste AI Platform — Phase 6

---

## Purpose

The Anomaly Detection module identifies unusual patterns in operational data that may warrant
review by an operator. It surfaces data quality issues and operational inconsistencies.

> [!IMPORTANT]
> Anomalies are **observations**, not accusations. The system does not and cannot determine
> intent, responsibility, or wrongdoing. Flagged records must be reviewed by a qualified operator.

---

## Implemented Detection Rules (v1.0)

### Rule 1 — Stale Open Batches

| Property | Value |
|----------|-------|
| **Type** | `stale_batch` |
| **Trigger** | `WasteBatch.status == "open"` and `created_at < now - 7 days` |
| **Severity** | `medium` |
| **Action** | "Review batch status — update or close if processing is complete." |

### Rule 2 — Unusually Heavy Batches

| Property | Value |
|----------|-------|
| **Type** | `heavy_batch` |
| **Trigger** | `WasteBatch.total_weight_kg > mean + 3 × std_dev` (requires ≥ 5 batches for stats) |
| **Severity** | `low` |
| **Action** | "Verify batch weight record — may indicate data entry error." |

### Rule 3 — Zero-Recovery Completed Batches

| Property | Value |
|----------|-------|
| **Type** | `missing_recovery_record` |
| **Trigger** | `WasteBatch.status == "completed"` with no `RecoveryRecord` entries |
| **Severity** | `high` |
| **Action** | "Add recovery records for this completed batch." |

---

## Flag Schema

Each detected anomaly returns a dict with these guaranteed fields:

```python
{
    "type":     str,   # Rule identifier (e.g. "stale_batch")
    "severity": str,   # "high" | "medium" | "low"
    "detail":   str,   # Human-readable description of the specific flag
    "action":   str,   # Recommended next action for the operator
    # Optional additional fields per rule:
    "batch_id": int,
    "value":    Any,
    "threshold": Any,
}
```

---

## Severity Levels

| Level | Meaning | Example |
|-------|---------|---------|
| `high` | Operational gap — likely causes reporting errors | Completed batch with no recovery records |
| `medium` | Should be reviewed soon | Batch open for > 7 days |
| `low` | Minor data quality concern | Weight outlier (may be data entry) |

---

## Language Policy

Anomaly descriptions must **never** use the words "fraud", "criminal", "theft", "illegal",
or similar. The system flags data patterns only. All such language is prohibited by test
`test_no_fraud_language_in_flags`.

---

## Limitations

1. Rules are deterministic threshold-based checks, not ML anomaly detection.
2. Statistics-based rules (heavy batch) require ≥ 5 records to compute mean/std. With fewer records, the rule is skipped.
3. False positives are expected — operational context is required to interpret flags.
4. The system does not send notifications; it surfaces flags in the UI only.
