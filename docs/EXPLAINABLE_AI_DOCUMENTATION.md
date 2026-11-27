# Explainable AI Documentation
## E-Waste AI Platform — Phase 6

---

## Purpose

The Explainable AI (XAI) module provides transparency into model predictions by surfacing
feature importance information. This helps operators understand *why* a model reached a
particular prediction, within the limits of the model type.

---

## `explain_prediction(model_id, features, feature_names)` Method

### Inputs

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_id` | str | ID of a loaded model (must exist in `_loaded_models`) |
| `features` | dict | `{feature_name: value}` mapping |
| `feature_names` | list | Optional; overrides keys from `features` dict |

### Output (success)

```python
{
    "available": True,
    "model_id": str,
    "method": str,          # "SHAP" | "feature_importances" | "linear_coefficients"
    "importance": {
        "feature_name": float,  # Higher = more important
        ...
    },
    "features_used": list,
    "disclaimer": str,          # Always present — explains limitations
    "timestamp": str,           # ISO 8601 UTC
}
```

### Output (model not loaded)

```python
{
    "available": False,
    "message": "Model not loaded. Run predict() first.",
}
```

---

## Explanation Methods (in priority order)

### 1. SHAP (SHapley Additive exPlanations)

- Used when `shap` package is installed.
- Supports TreeExplainer for tree-based models (RandomForest, XGBoost, etc.).
- Provides local explanations (per-prediction feature contributions).
- Returns `method: "SHAP"`.

### 2. Feature Importances (sklearn)

- Used when model has `.feature_importances_` attribute (tree ensembles).
- Returns global feature importance from the trained model.
- Returns `method: "feature_importances"`.

### 3. Linear Coefficients

- Used when model has `.coef_` attribute (LogisticRegression, LinearSVC, Ridge, etc.).
- Returns absolute coefficient values as importance proxy.
- Returns `method: "linear_coefficients"`.

### 4. Unavailable

- If none of the above apply (e.g., KNN, SVM with RBF kernel), returns `available: False`
  with a message explaining that explanation is not supported for this model type.

---

## Correlation ≠ Causation

> [!WARNING]
> Feature importance shows which features are most **correlated** with the model's output.
> It does not prove that those features *cause* the predicted outcome.
> Domain expertise is required to interpret explanations.

---

## Confidence & Limitations

All explanation results include a `disclaimer` field. Contents vary by method:

| Method | Disclaimer Includes |
|--------|-------------------|
| SHAP | SHAP is local — explanation is for this specific prediction |
| Feature Importances | Global importance — may not reflect individual prediction |
| Linear Coefficients | Assumes linear relationship; may not reflect non-linear interactions |

---

## Prediction Provenance

Every prediction and explanation is tagged with:

| Field | Value |
|-------|-------|
| `model_id` | Identifier of the model used |
| `timestamp` | ISO 8601 UTC time of inference |
| `prediction_type` | `"classification"` or `"regression"` |
| `explanation_method` | Method used for explanation |

---

## Limitations

1. SHAP explanations for large models may be slow on CPU. Use with ≤ 100 features for interactive use.
2. Global feature importance (method 2) does not reflect the contribution to any specific prediction.
3. Explanation quality degrades for models trained on very small datasets (< 100 samples).
4. The system does not support gradient-based explanations (LIME, Integrated Gradients) in v1.0.
