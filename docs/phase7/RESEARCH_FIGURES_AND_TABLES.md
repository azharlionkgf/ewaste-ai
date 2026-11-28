# Research Figures & Tables — Phase 7
## E-Waste AI Platform
**Date:** 2026-11-28 | **Source Data:** `docs/phase7/phase7_measurements.json` (Synthetic Validation Benchmarks Only)

---

## Table 1: Classification Benchmark (Untouched 10% Hold-out, `n=50`, `seed=42`)

| Model | Val Acc | Test Acc | Test Prec (W) | Test Rec (W) | Test F1 (W) | Fit Time (s) | Infer Time (ms) |
|-------|---------|----------|---------------|--------------|-------------|--------------|-----------------|
| `DummyClassifier` | 0.3400 | 0.3400 | 0.1156 | 0.3400 | 0.1725 | 0.0006 | 0.102 |
| `LogisticRegression` | 0.6000 | 0.7000 | 0.6952 | 0.7000 | 0.6870 | 0.0158 | 0.328 |
| `RandomForestClassifier` | 0.8600 | 0.9000 | 0.9011 | 0.9000 | 0.9000 | 0.1842 | 7.822 |
| `GradientBoostingClassifier` | 0.8400 | 0.8800 | 0.8839 | 0.8800 | 0.8779 | 0.5672 | 1.259 |

---

## Table 2: Confusion Matrices on Untouched Test Split (`n=50`, Classes `0, 1, 2`)

### 2a. `RandomForestClassifier` (Test Accuracy: `0.9000`)

| True \ Predicted | Class 0 | Class 1 | Class 2 | Support |
|------------------|---------|---------|---------|---------|
| **Class 0** | 15 | 2 | 0 | 17 |
| **Class 1** | 0 | 15 | 2 | 17 |
| **Class 2** | 1 | 0 | 15 | 16 |

### 2b. `GradientBoostingClassifier` (Test Accuracy: `0.8800`)

| True \ Predicted | Class 0 | Class 1 | Class 2 | Support |
|------------------|---------|---------|---------|---------|
| **Class 0** | 16 | 1 | 0 | 17 |
| **Class 1** | 0 | 16 | 1 | 17 |
| **Class 2** | 3 | 1 | 12 | 16 |

### 2c. `LogisticRegression` (Test Accuracy: `0.7000`)

| True \ Predicted | Class 0 | Class 1 | Class 2 | Support |
|------------------|---------|---------|---------|---------|
| **Class 0** | 16 | 0 | 1 | 17 |
| **Class 1** | 1 | 12 | 4 | 17 |
| **Class 2** | 6 | 3 | 7 | 16 |

---

## Table 3: Random Forest Gini Feature Importance Ranking (Experiment E3)

| Rank | Feature | Importance Score | Relative Share (%) |
|------|---------|------------------|--------------------|
| 1 | `feature_1` | 0.1940 | 19.40% |
| 2 | `feature_3` | 0.1401 | 14.01% |
| 3 | `feature_4` | 0.1193 | 11.93% |
| 4 | `feature_6` | 0.1184 | 11.84% |
| 5 | `feature_9` | 0.1155 | 11.55% |
| 6 | `feature_2` | 0.1038 | 10.38% |
| 7 | `feature_7` | 0.0763 | 7.63% |
| 8 | `feature_8` | 0.0484 | 4.84% |
| 9 | `feature_0` | 0.0426 | 4.26% |
| 10 | `feature_5` | 0.0415 | 4.15% |

*Top 5 features cumulative share: `0.6873` (`68.73%`). Correlation / split importance does not imply causation.*

---

## Table 4: Regression Benchmark (Untouched 10% Hold-out, `n=30`, `seed=42`)

| Model | Test MAE | Test \(R^2\) | Fit Time (s) | Infer Time (ms) |
|-------|----------|--------------|--------------|-----------------|
| `DummyRegressor` | 98.6669 | -0.0008 | 0.0007 | 0.260 |
| `Ridge` | 8.6533 | 0.9925 | 0.0095 | 0.876 |
| `GradientBoostingRegressor` | 25.7628 | 0.9300 | 0.1205 | 0.677 |
| `RandomForestRegressor` | 29.2819 | 0.9043 | 0.2080 | 6.891 |

---

## Table 5: End-to-End Pipeline Scaling Profile (CPU, Python `tracemalloc`)

| Dataset Rows | CSV Parse (ms) | Clean (ms) | Preprocess (ms) | RF Train (ms) | RF Infer (ms) | Peak Memory (MB) |
|--------------|----------------|------------|-----------------|---------------|---------------|------------------|
| 200 | 15.01 | 166.48 | 149.93 | 1,240.94 | 35.30 | 0.32 |
| 1,000 | 12.68 | 224.17 | 115.36 | 1,129.11 | 22.29 | 1.11 |
| 5,000 | 29.86 | 569.67 | 239.45 | 2,101.39 | 43.52 | 4.34 |
