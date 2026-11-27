# E-Waste AI — AI Model Integration Guide (Phase 4)

## Overview

Phase 4 integrates actual trained models from Phase 3 into the production backend.

**Core principle:** Never return hardcoded or fabricated predictions.  
If no suitable model is available, the API clearly states this and provides instructions.

## AIModelEngine

Located at: `backend/services/ai_model_service.py`

### Model Loading
- Reads the Phase 3 model registry at `models/registry/registry.json`
- Loads model files from `saved_models/` directory
- Caches loaded models in memory for performance

### Prediction Flow
```
API Request → task_type → find active model → load model → prepare features → predict → save to DB → return result
```

### Prediction Types
| Type | Meaning |
|------|---------|
| `actual_model` | Real prediction from a trained sklearn/CNN model |
| `unavailable` | No model trained for this task yet |
| `rule_loaded_no_inference` | Model found but runtime unavailable (e.g., no torch) |

## E-Waste Task Types

| Task Type | Description | Model Type |
|-----------|-------------|------------|
| `ewaste_classification` | WEEE category classification | Classifier |
| `device_identification` | Device type identification | Classifier |
| `component_classification` | Component type prediction | Classifier |
| `material_classification` | Material type prediction | Classifier |
| `recovery_quantity` | Recovery quantity prediction (g) | Regressor |
| `economic_value` | Economic value prediction (USD) | Regressor |
| `recycling_outcome` | Recycling outcome prediction | Classifier |

## Training a Model for Use in Phase 4

1. Open AI Training Laboratory in the Streamlit app
2. Select dataset, task type, and algorithm
3. Train and evaluate the model
4. Click "Activate" to set as the active model for that task
5. The Phase 4 API will automatically find and use this model

## Recovery Intelligence (Rule-Based)

When no AI model is available, the system uses published composition data:

- **Source:** EEA (European Environment Agency) / UNEP material composition surveys
- **Coverage:** Laptop, Smartphone, Desktop PC, Monitor, Printer, Tablet, Generic
- **Materials:** Gold, Silver, Copper, Aluminum, Steel, Lithium, Cobalt, Tin, Plastic, Glass, Indium
- **All results labeled:** `source: "rule_based"` with full data source citation

## Research Traceability

Every AI prediction is stored with:
- `model_id` and `model_version` from registry
- `dataset_version` used for training
- `input_hash` (SHA-256 of input)
- `prediction_type` (actual_model / rule_based / unavailable)
- `created_at` timestamp

This ensures full reproducibility for research paper evidence.
