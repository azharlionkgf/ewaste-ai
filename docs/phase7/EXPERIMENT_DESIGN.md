# Experiment Design — Phase 7
## E-Waste AI Platform
**Date:** 2026-11-28 | **Status:** Validated Pipeline Experiments (Synthetic Data Only)

> **CRITICAL TRANSPARENCY NOTICE:** No real e-waste datasets are currently present in `data/`. Therefore, Phase 7 experiments validate end-to-end experimental reproducibility, leak-free splitting, baseline benchmarking, and ablation behavior on deterministic synthetic datasets (`random_state=42`). No real-world domain performance is claimed.

---

## 1. Research Questions

1. **RQ1 (Pipeline Correctness & Leak-Free Generalization):** Do non-trivial classifiers (`LogisticRegression`, `RandomForestClassifier`, `GradientBoostingClassifier`) consistently outperform a majority-class baseline (`DummyClassifier`) on an untouched 10% hold-out test split when preprocessing parameters (`StandardScaler`) are fit strictly on training folds?
2. **RQ2 (Model Complexity Trade-off):** How do linear (`LogisticRegression`, `Ridge`), bagged ensemble (`RandomForest`), and boosted ensemble (`GradientBoosting`) families trade off predictive accuracy/MAE against CPU training and inference latency?
3. **RQ3 (Feature Attribution Consistency):** Can tree-based models consistently identify the 5 informative features embedded inside `make_classification(..., n_features=10, n_informative=5)`?

---

## 2. Independent, Dependent & Controlled Variables

- **Independent Variable:** Estimator family & complexity (Dummy baseline vs Linear vs Random Forest (`n_estimators=50`) vs Gradient Boosting (`n_estimators=50`)).
- **Dependent Variables:**
  - Classification: Validation Accuracy, Untouched Test Accuracy, Weighted Precision, Weighted Recall, Weighted F1, Confusion Matrix, Feature Importances.
  - Regression: Untouched Test MAE, Test \(R^2\), CPU Train Time (s), CPU Test Inference Time (ms).
- **Controlled Variables:**
  - Fixed random seed: `random_state=42` across generation, stratified splitting, and estimator initialization.
  - Identical 80% / 10% / 10% train/val/test partitions (`stratify=y` for classification).
  - Identical `StandardScaler` fit strictly on `X_train` and applied read-only to `X_val` and `X_test`.
  - Fixed hardware/software runtime: CPU-only Python 3.13.7, `scikit-learn 1.8.0`.

---

## 3. Experimental Runs

1. **Experiment E1 — 3-Class Classification Benchmark (`n=500, d=10, d_informative=5`):**
   Models: `DummyClassifier(most_frequent)`, `LogisticRegression(max_iter=500)`, `RandomForestClassifier(n_estimators=50)`, `GradientBoostingClassifier(n_estimators=50)`.
2. **Experiment E2 — Continuous Regression Benchmark (`n=300, d=8, d_informative=5, noise=10.0`):**
   Models: `DummyRegressor(mean)`, `Ridge()`, `RandomForestRegressor(n_estimators=50)`, `GradientBoostingRegressor(n_estimators=50)`.
3. **Experiment E3 — Feature Importance Recovery (`RandomForestClassifier` on E1):**
   Inspect `feature_importances_` across `feature_0..feature_9`.

---

## 4. Reproducibility & Traceability

- Full JSON results archived in `docs/phase7/phase7_measurements.json` and `docs/phase7/baseline_results.json`.
- Experiment tracking ORM (`ResearchExperiment`) verified in `tests/test_phase7_db.py` (`experiment_name`, `model_architecture`, `hyperparameters`, `random_seed`, `metrics`, `library_versions`).
