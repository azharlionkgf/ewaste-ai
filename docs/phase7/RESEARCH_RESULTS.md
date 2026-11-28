# Research Results — Phase 7
## E-Waste AI Platform
**Date:** 2026-11-28 | **Status:** Reproducible Synthetic Pipeline Validation Complete

---

## 1. Experimental Outcomes Summary

All experiments defined in `EXPERIMENT_DESIGN.md` were executed cleanly on CPU-only Python 3.13.7 (`scikit-learn 1.8.0`, `seed=42`) with results persisted in `docs/phase7/phase7_measurements.json`.

### Answering Research Questions
- **RQ1 (Generalization Above Floor):** Confirmed. All learned estimators significantly exceed majority/mean baselines on untouched hold-out splits: Classification weighted F1 improved from `0.1725` (`DummyClassifier`) to `0.9000` (`RandomForestClassifier`); Regression MAE dropped from `98.6669` (`DummyRegressor`) to `8.6533` (`Ridge`).
- **RQ2 (Architecture & Runtime Trade-off):** Confirmed. Linear models remain fastest (`0.0095–0.0158 s` fit, `< 1 ms` test inference), while tree ensembles deliver superior accuracy (`0.88–0.90`) on non-linear multi-class boundaries at `< 0.6 s` CPU training cost for 500 samples. At 5,000 rows through the full clean/preprocess/train pipeline, total peak heap allocation stayed at `4.34 MB` with `RandomForest` training completing in `2.10 s`.
- **RQ3 (Feature Attribution Recovery):** Confirmed. In Experiment E3 (`RandomForestClassifier` on 5 informative + 5 redundant/noise features), the top 5 features (`feature_1 = 0.1940`, `feature_3 = 0.1401`, `feature_4 = 0.1193`, `feature_6 = 0.1184`, `feature_9 = 0.1155`) collectively explain **68.73%** of total Gini impurity reduction, clearly distinguishing higher-signal dimensions from low-importance features (`feature_0 = 0.0426`, `feature_5 = 0.0415`, `feature_8 = 0.0484`). Note that feature importance reflects statistical predictive association in this synthetic tree ensemble, **not** physical causation.

---

## 2. Historical Phase 3 Synthetic Runs (`models/registry/registry.json`)

For continuity with Phase 3 (200-sample classification dataset `synthetic_200x10_3class`, `seed=42`), stored registry metrics record:
- `synthetic_clf_random_forest`: train acc `1.0000` (`n=128`), val acc `0.9062`, val F1 macro `0.9049`, val ROC-AUC `0.9532` (`n=32`).
- Notice the train (`1.0000`) vs validation (`0.9062`) gap demonstrates small-sample tree overfitting, motivating Phase 7's strict untouched test-set comparison on `n=500`.

---

## 3. Practical Limitations & Next Scientific Steps

1. **No Real Dataset Metrics Yet:** Because `data/` contains only directory placeholders (`.gitkeep`), empirical domain metrics on real WEEE images, PCB assays, or municipal batch logs await ingestion of open benchmark datasets or partner facility records.
2. **Future Research Prerequisites:** Once real labeled data is onboarded, run stratified k-fold cross-validation (`k >= 5`), hyperparameter tuning without touching test folds, and formal confidence interval reporting alongside SHAP feature explanations (`explain_prediction()`).
