# Research Methodology — Phase 7
## E-Waste AI Platform
**Date:** 2026-11-28 | **Reproducibility Seed:** `42` | **Runtime:** CPU-only (`scikit-learn 1.8.0`)

---

## 1. Data Acquisition & Scope Statement

As documented in `DATASET_PROVENANCE.md`, no external real e-waste tabular or image datasets currently reside in `data/`. Following scientific integrity rules, the methodology validates the full analytical pipeline on deterministic synthetic benchmarks generated with `sklearn.datasets` (`make_classification`, `make_regression`) at `random_state=42`, while isolating domain estimation exclusively inside citation-tracked rule modules (`UNEP`/`EEA`/`EPA`).

---

## 2. Preprocessing & Data Leakage Prevention Protocol

All Phase 7 experiments adhere strictly to zero-leakage preprocessing:

1. **Hold-out Partitioning First:** Datasets are partitioned **before** any normalization or feature transformation into **80% Train / 10% Validation / 10% Test** using two deterministic `train_test_split(..., random_state=42)` steps (`stratify=y` for classification).
2. **Target Exclusion Verification:** `ml/data/preprocessor_advanced.py` enforces an automated guard raising `ValueError` if `target_col` appears in `feature_cols`.
3. **Transformer Fitting:** `StandardScaler` computes sample mean \(\mu\) and standard deviation \(\sigma\) **exclusively** on `X_train`. The fitted statistics transform `X_val` and `X_test` without re-fitting.
4. **Untouched Test Set Rule:** Hyperparameter selection and comparative diagnostics use validation metrics (`X_val`), while final model comparison tables report single-pass evaluation on the untouched hold-out test split (`X_test`).

---

## 3. Baseline & Model Selection Rationale

Every experimental task evaluates an uninformative baseline prior to parametric and non-parametric estimators:

- **Classification Baseline:** `DummyClassifier(strategy="most_frequent")` establishes empirical chance/majority floor (`0.3400` on balanced 3-class test split).
- **Regression Baseline:** `DummyRegressor(strategy="mean")` establishes variance floor (\(R^2 \approx 0.0\)).
- **Parametric Linear Models:** `LogisticRegression`, `Ridge` evaluate linearly separable or additive signal structure with sub-millisecond inference.
- **Non-Linear Tree Ensembles:** `RandomForest` (bagging) and `GradientBoosting` (additive residual boosting) capture interaction terms and provide feature importance vectors (`feature_importances_`).

---

## 4. Evaluation Metrics & Timing Measurement

- **Classification Metrics:** Accuracy, Weighted Precision, Weighted Recall, Weighted F1-score, and 3×3 Confusion Matrix.
- **Regression Metrics:** Mean Absolute Error (MAE) and Coefficient of Determination (\(R^2\)).
- **Compute Cost Metrics:** High-resolution wall-clock time via `time.perf_counter()` (fit duration in seconds; untouched test-set prediction in milliseconds) and traced Python heap allocation via `tracemalloc`.

---

## 5. Threat to Validity & Limitations

1. **External Validity:** Synthetic Gaussian/clustered manifolds do not replicate real WEEE image lighting, occlusion, alloy impurities, or regional collection bias.
2. **Sample Size Variance:** At `n=500`, the 10% test fold contains `50` samples (`17` / `17` / `16` per class), giving a binomial resolution step of `0.02` (`2%`) accuracy per misclassified sample. Larger real datasets and k-fold cross-validation are recommended prior to industrial deployment.
