# Baseline Comparison Report — Phase 7
## E-Waste AI Platform
**Date:** 2026-11-28 | **Source Artifact:** `docs/phase7/phase7_measurements.json` & `docs/phase7/baseline_results.json`

> **DISCLOSURE:** All comparative results below come from deterministic `sklearn` synthetic datasets (`random_state=42`) evaluated under an identical 80/10/10 split with train-only scaling (`StandardScaler`). They validate algorithmic ranking and pipeline integrity and do NOT represent physical e-waste facility performance.

---

## 1. Classification Comparison (`synthetic_classification_500x10_3class`, Test `n=50`)

| Model | Val Accuracy (`n=50`) | Test Accuracy (`n=50`) | Test Weighted Precision | Test Weighted Recall | Test Weighted F1 | Train Time (s) | Test Inference (ms) |
|-------|-----------------------|------------------------|-------------------------|----------------------|------------------|----------------|---------------------|
| **DummyClassifier** (`most_frequent`) | 0.3400 | 0.3400 | 0.1156 | 0.3400 | 0.1725 | 0.0006 | 0.102 |
| **LogisticRegression** (`max_iter=500`) | 0.6000 | 0.7000 | 0.6952 | 0.7000 | 0.6870 | 0.0158 | 0.328 |
| **GradientBoostingClassifier** (`50 trees`) | 0.8400 | 0.8800 | 0.8839 | 0.8800 | 0.8779 | 0.5672 | 1.259 |
| **RandomForestClassifier** (`50 trees`) | **0.8600** | **0.9000** | **0.9011** | **0.9000** | **0.9000** | 0.1842 | 7.822 |

*Cross-reference (automated unit test `TestBaselineComparison` on 80/20 split of same 500x10 dataset, `baseline_results.json`):* Dummy `0.3300` acc / `0.1638` F1; LogisticRegression `0.7200` acc / `0.7125` F1; RandomForest `0.8800` acc / `0.8798` F1.

### Key Findings (Classification)
1. **Substantial Gain Over Majority Baseline:** `RandomForestClassifier` outperforms `DummyClassifier` by `+0.5600` test accuracy (`0.9000` vs `0.3400`) and `+0.7275` weighted F1.
2. **Non-Linearity Advantage:** Because `make_classification(..., n_classes=3, n_informative=5)` produces multi-cluster decision boundaries, tree ensembles (`RandomForest`: `0.9000`, `GradientBoosting`: `0.8800`) exceed linear `LogisticRegression` (`0.7000`) by `18–20` percentage points.
3. **Speed vs Accuracy Trade-off:** `LogisticRegression` trains `11.7x` faster and predicts `23.8x` faster than `RandomForestClassifier`, whereas `GradientBoostingClassifier` predicts `6.2x` faster than `RandomForest` at test time (`1.259 ms` vs `7.822 ms`).

---

## 2. Regression Comparison (`synthetic_regression_300x8`, Test `n=30`)

| Model | Test MAE | Test \(R^2\) | Train Time (s) | Test Inference (ms) |
|-------|----------|--------------|----------------|---------------------|
| **DummyRegressor** (`mean`) | 98.6669 | -0.0008 | 0.0007 | 0.260 |
| **Ridge** | **8.6533** | **0.9925** | 0.0095 | 0.876 |
| **GradientBoostingRegressor** (`50 trees`) | 25.7628 | 0.9300 | 0.1205 | 0.677 |
| **RandomForestRegressor** (`50 trees`) | 29.2819 | 0.9043 | 0.2080 | 6.891 |

### Key Findings (Regression)
1. **Model-Data Alignment Matters:** On the additive linear regression synthetic target (`noise=10.0`), `Ridge` achieves `MAE = 8.6533` (`R² = 0.9925`), close to the irreducible Gaussian noise floor, outperforming un-tuned 50-tree `GradientBoostingRegressor` (`MAE = 25.7628`) and `RandomForestRegressor` (`MAE = 29.2819`).
2. **Recommendation:** Always compare linear/regularized models (`LogisticRegression`, `Ridge`) against ensembles (`RandomForest`, `GradientBoosting`) on each target rather than assuming ensembles win universally.
