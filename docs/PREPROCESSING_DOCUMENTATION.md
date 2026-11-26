# Preprocessing Documentation

## Overview

`AdvancedPreprocessor` (`ml/data/preprocessor_advanced.py`) handles feature scaling, categorical encoding, and stratified train/val/test splitting.

## Scalers

| Name | Class | When to Use |
|------|-------|-------------|
| `standard` (default) | `StandardScaler` | Most ML models; zero mean, unit variance |
| `minmax` | `MinMaxScaler` | Neural networks; scales to [0, 1] |
| `robust` | `RobustScaler` | Data with outliers; uses IQR |
| `none` | — | Tree-based models (RF, XGBoost, CatBoost) |

## Categorical Encoders

| Name | Class | When to Use |
|------|-------|-------------|
| `onehot` (default) | `OneHotEncoder` | Nominal categories with no ordinal relationship |
| `label` | `OrdinalEncoder` | Ordinal categories or tree-based models |
| `none` | — | Pre-encoded data |

## Train/Val/Test Split

- Default: 70% / 15% / 15%
- Stratified by default (preserves class distribution in each split)
- Falls back to random split if stratification fails (too few samples per class)
- Random seed recorded for reproducibility (default: 42)

## Leakage Prevention

> [!CAUTION]
> The preprocessor raises `ValueError` if `target_col` appears in `feature_cols`. This prevents the most common form of data leakage.

## Preprocessing Report

```json
{
  "total_samples": 950,
  "features_used": ["weight_kg", "condition", "device_type"],
  "numeric_features": ["weight_kg"],
  "categorical_features": ["condition", "device_type"],
  "target_column": "category",
  "class_names": ["laptop", "phone", "tablet"],
  "n_classes": 3,
  "scaler": "standard",
  "encoder": "onehot",
  "split": {"train": 665, "val": 143, "test": 142},
  "stratified": true,
  "random_seed": 42,
  "leakage_check": "PASSED — target not in features",
  "timestamp": "2026-11-26T06:35:00Z"
}
```

## Reproducibility

The full preprocessing config is JSON-serializable and can be saved with `AdvancedPreprocessor.save_config()` for research paper appendix inclusion.
