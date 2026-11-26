# Data Cleaning Documentation

## Overview

The `AdvancedDataCleaner` (located at `ml/data/cleaner_advanced.py`) performs automated data cleaning while preserving the original dataset.

## Cleaning Operations

| Operation | Default | Description |
|-----------|---------|-------------|
| Drop empty columns | ✅ Enabled | Removes columns where every value is NaN |
| Remove duplicates | ✅ Enabled | Drops exact duplicate rows |
| Fix data types | ✅ Enabled | Converts string columns to numeric if ≥80% parse successfully |
| Normalize text | ✅ Enabled | `str.strip().str.lower()` on all object columns |
| Handle missing values | ✅ Enabled | Configurable strategy (see below) |
| Flag outliers | ✅ Enabled | Adds `_outlier_{col}` boolean flag columns |
| Detect inconsistent categories | ✅ Always | Finds values that differ only in case/spacing |

## Missing Value Strategies

| Strategy | Numeric Columns | Categorical Columns |
|----------|----------------|---------------------|
| `median` (default) | Filled with column median | Filled with mode |
| `mean` | Filled with column mean | Filled with mode |
| `mode` | Filled with mode | Filled with mode |
| `constant` | Filled with `fill_constant` value | Filled with `fill_constant` |
| `drop_row` | Rows with any missing value removed | Rows with any missing value removed |

## Outlier Detection Methods

| Method | Parameter | Logic |
|--------|-----------|-------|
| `iqr` (default) | threshold=1.5 | Values outside Q1 − 1.5×IQR or Q3 + 1.5×IQR are flagged |
| `zscore` | threshold=3.0 | Values with |z| > threshold are flagged |

> [!NOTE]
> Outliers are **flagged** (a boolean column is added), never silently deleted. The user decides what to do with flagged records.

## Cleaning Report Structure

```json
{
  "rows_before": 1000,
  "rows_after": 987,
  "rows_removed": 13,
  "cols_before": 15,
  "cols_after": 14,
  "columns_dropped": ["empty_col"],
  "missing_filled": 42,
  "duplicates_removed": 13,
  "outliers_flagged": 28,
  "type_fixes": 2,
  "text_normalizations": 180,
  "config_used": {...},
  "operations_log": [
    {
      "operation": "remove_duplicates",
      "duplicates_removed": 13,
      "detail": "Removed 13 duplicate rows",
      "timestamp": "2026-11-26T06:30:00Z"
    }
  ],
  "timestamp": "2026-11-26T06:30:01Z"
}
```

## What is Preserved

- Original raw file in `data/raw/` — never touched
- Cleaning config is saved alongside the cleaned output
- Operations log records every change with timestamps
- Cleaned output saved to `data/cleaned/{name}_cleaned.csv`
