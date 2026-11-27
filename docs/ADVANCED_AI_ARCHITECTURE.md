# Advanced AI Architecture — E-Waste AI Platform
## Phase 6: Advanced AI & Recovery Intelligence

---

## Overview

The Advanced AI layer is implemented in `backend/services/advanced_intelligence.py` as a single,
singleton `AdvancedIntelligenceEngine` class. It provides structured intelligence services on top
of the ML models trained in Phase 3, without duplicating training or evaluation logic.

---

## Module Structure

```
backend/
└── services/
    └── advanced_intelligence.py        ← Phase 6 engine (all tasks in one file)
        ├── MATERIAL_KNOWLEDGE_BASE     ← Task 2/3: device→material composition KB
        ├── HAZARDOUS_REFERENCE         ← Task 9: hazardous substance reference
        ├── MATERIAL_PRICES_USD_PER_G   ← Task 6: LME-reference commodity prices
        ├── RECOVERY_EFFICIENCY         ← Task 4: material recovery efficiency table
        ├── AdvancedIntelligenceEngine  ← Task 1: central engine class
        │   ├── predict()               ← Task 1: safe model inference
        │   ├── get_device_knowledge()  ← Task 3: material intelligence lookup
        │   ├── estimate_recovery()     ← Task 4: recovery prediction
        │   ├── recommend_recovery_plan()← Task 5: recovery optimization
        │   ├── estimate_processing_cost()← Task 6: economic analysis
        │   ├── compute_trends()        ← Task 7: predictive analytics
        │   ├── detect_anomalies()      ← Task 8: anomaly detection
        │   ├── get_hazardous_info()    ← Task 9: hazardous material safety
        │   └── explain_prediction()   ← Task 10: explainable AI
        └── get_engine()               ← Task 1: singleton accessor
```

---

## Task 1 — Advanced AI Engine

### Design
- **Singleton pattern:** `get_engine()` returns a module-level shared instance.
- **Model loading:** Models are loaded on-demand from the filesystem path stored in the database (`MLModel.file_path`). Once loaded they are cached in `_loaded_models`.
- **CPU-only:** No CUDA dependencies. All sklearn/xgboost models run on CPU by default.
- **Safe inference:** `predict()` returns `{"error": ..., "available": False}` if the model is not loaded or the prediction fails. It never fabricates results.

### Key Methods

| Method | Input | Output |
|--------|-------|--------|
| `list_available_models()` | — | List of dicts from `MLModel` DB table |
| `list_supported_device_types()` | — | List of device type keys from KB |
| `predict(model_id, features)` | str, dict | Prediction dict or error dict |
| `load_model(model_id)` | str | Loaded model object or raises |

---

## Task 2 — Multi-Level E-Waste Classification

Classification support is provided through the ML models trained in Phase 3. The engine:

1. Lists all trained models from the database via `list_available_models()`.
2. Loads and runs inference via `predict(model_id, feature_dict)`.
3. Never claims class predictions beyond what the model's training labels support.
4. Wraps predictions with provenance: `model_id`, `model_version`, `prediction_type`, `timestamp`.

Hierarchical classification (category → device type → component → material) is supported
*only* where multi-level training data was collected in Phase 2/3.

---

## Task 3 — Component & Material Intelligence

The `MATERIAL_KNOWLEDGE_BASE` dictionary contains:

- **6 device types:** laptop, desktop, mobile_phone, television, printer, battery_pack
- **Per device:** average weight, material composition percentages, component list,
  hazardous substance list, confidence rating, and literature source citations
- **Provenance fields:** `source`, `confidence` (high/medium/low)
- **Unknown values:** When device type is not in KB, `get_device_knowledge()` returns
  `{"available": False, "message": "..."}` — never fabricated data.

### Provenance Labels

| Label | Meaning |
|-------|---------|
| `estimate` | Rule-based calculation from KB composition percentages |
| `model_prediction` | Output from a trained ML model |
| `user_provided` | Value entered by an operator |
| `measured` | Value recorded from actual measurement |

---

## Constraints

- No live price feeds — all prices are reference values with an explicit date.
- No regulatory compliance claims.
- No unsafe dismantling instructions.
- All estimates clearly tagged; never presented as measured facts.
- CPU-only inference; no GPU/CUDA requirements.
