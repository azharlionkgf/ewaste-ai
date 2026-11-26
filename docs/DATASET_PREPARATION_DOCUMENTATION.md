# Dataset Preparation Documentation

## Overview

`DatasetPreparer` (`ml/data/dataset_preparer.py`) performs the final step before model training: splitting datasets into train/val/test sets with provenance tracking.

## Tabular Dataset Preparation

### Process

1. Validate target column exists
2. Validate no data leakage (target not in features)
3. Drop rows with missing target values
4. Stratified train/val/test split (falls back to random if needed)
5. Save splits as CSV files
6. Save `provenance.json` alongside splits

### Output Structure

```
data/splits/{dataset_name}/
    train.csv
    val.csv
    test.csv
    provenance.json
```

### Provenance JSON

```json
{
  "dataset_name": "ewaste_classification",
  "source_rows": 1000,
  "source_cols": 12,
  "preparation_config": {
    "train_ratio": 0.70,
    "val_ratio": 0.15,
    "test_ratio": 0.15,
    "random_seed": 42,
    "stratify": true
  },
  "feature_cols": ["weight_kg", "condition", "device_type"],
  "target_col": "category",
  "split_stats": {
    "total_samples": 987,
    "train_samples": 690,
    "val_samples": 148,
    "test_samples": 149
  },
  "created_at": "2026-11-26T06:45:00Z"
}
```

## Image Dataset Preparation

### Expected Input Structure

```
root_dir/
    laptop/
        img1.jpg
        img2.png
    phone/
        img3.jpg
```

### Output Structure

```
output_dir/
    train/
        laptop/  img1.jpg
        phone/   img3.jpg
    val/
        laptop/  ...
    test/
        laptop/  ...

data/splits/{dataset_name}/
    train.csv   (filepath, label, original columns)
    val.csv
    test.csv
    provenance.json
```

## Data Leakage Prevention

> [!CAUTION]
> `DatasetPreparer` raises `ValueError` if `target_col` is in `feature_cols`. This is an explicit guard against the most common form of data leakage.

## Reproducibility

- All splits use a fixed `random_seed` (default: 42)
- Stratified splitting preserves class distribution in each split
- Full provenance JSON is saved — include in research paper appendix
