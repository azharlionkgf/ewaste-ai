# AI/ML Validation Report — Phase 7
## E-Waste AI Platform
**Date:** 2026-11-28 | **Test Suite:** `tests/test_phase7_ml_api.py` | **Execution Mode:** CPU-only (Python 3.13.7, scikit-learn 1.8.0)

---

## 1. Model Inventory & Artifact Verification

13 `.pkl` model files verified in `models/saved/` (CPU-compatible `scikit-learn` estimators; no `.cuda` attribute or GPU requirement):

| Artifact (`models/saved/`) | Size (bytes) | Origin / Purpose |
|----------------------------|--------------|------------------|
| `synthetic_clf_extra_trees.pkl` | 1,065,432 | Synthetic 3-class classification validation |
| `synthetic_clf_hist_gradient_boosting.pkl` | 209,490 | Synthetic 3-class classification validation |
| `synthetic_clf_logistic_regression.pkl` | 970 | Synthetic 3-class classification validation |
| `synthetic_clf_random_forest.pkl` | 412,746 | Synthetic 3-class classification validation |
| `synthetic_reg_extra_trees.pkl` | 1,400,824 | Synthetic regression validation |
| `synthetic_reg_hist_gradient_boosting.pkl` | 59,852 | Synthetic regression validation |
| `synthetic_reg_random_forest.pkl` | 893,148 | Synthetic regression validation |
| `test_dt_load_synthetic.pkl` | 4,198 | Automated test artifact |
| `test_hgb_synthetic.pkl` | 218,452 | Automated test artifact |
| `test_lr_synthetic.pkl` | 922 | Automated test artifact |
| `test_rf_synthetic.pkl` | 464,138 | Automated test artifact |
| `test_rf_reg_synthetic.pkl` | 1,299,570 | Automated test artifact |
| `diag_test.pkl` | 115,774 | Diagnostic test artifact |

Metadata & training history verified in `models/registry/registry.json` and `models/history/*.json`.

---

## 2. Functional, Edge-Case & Physics Validation

| Validation Check | Scope & Behavior Verified | Status |
|------------------|---------------------------|--------|
| Knowledge base coverage | All 6 device types (`laptop`, `desktop`, `mobile_phone`, `television`, `printer`, `battery_pack`) estimable | ✅ PASS |
| Unknown device handling | `estimate_recovery('unknown_xyz_device', 1.0)` returns `available: False` | ✅ PASS |
| Zero / negative weight input | Zero and negative weight inputs handled safely without unhandled crash | ✅ PASS |
| Missing model handling | `predict()` & `explain_prediction()` with nonexistent model ID return safe unavailable/error response | ✅ PASS |
| Mass conservation invariant | Total `estimated_recovered_g` summed across materials never exceeds 1,000 g input (+5% tolerance) for 1.0 kg input across all 6 devices | ✅ PASS |
| Disclaimer enforcement | Economic cost estimates include explicit `ESTIMATE` disclaimer | ✅ PASS |
| CPU compatibility | Sample `.pkl` files load via `joblib.load()` on CPU without PyTorch/CUDA dependencies | ✅ PASS |
| Fresh-process persistence | Re-importing and initializing `AdvancedIntelligenceEngine` after DB/app restart loads available registry models cleanly | ✅ PASS |

---

## 3. Leakage, Split Integrity & Overfitting Analysis

1. **Preprocessing consistency & leakage check:**
   - `ml/data/preprocessor_advanced.py` explicitly raises `ValueError` if `target_col` appears in `feature_cols` (`test_leakage_prevention` in Phase 2 suite).
   - Phase 7 baseline experiments verified strict `StandardScaler().fit(X_train)` before transforming validation/test splits (`80/10/10` stratified split, `random_state=42`) so zero test-set statistics leak into training.
2. **Overfitting risk observed in existing registry artifact:**
   - In `models/registry/registry.json`, `synthetic_clf_random_forest_20261126_082131` recorded `train_metrics.accuracy = 1.0000` (n=128) versus `val_metrics.accuracy = 0.9062` (n=32), indicating exact-fit variance typical of unconstrained default trees on small (n=200) datasets. Cross-validation and depth regularization should be enforced when real e-waste datasets are introduced.
3. **Drift & Domain Shift Risk (CRITICAL DISCLOSURE):**
   - Zero real industrial or academic e-waste datasets are currently stored in `data/` (only `.gitkeep` placeholders exist).
   - Consequently, **no saved `.pkl` classifier/regressor should be deployed for production e-waste sorting without retraining on real labeled facility data.** Only the citation-backed rule engine (`MATERIAL_KNOWLEDGE_BASE`, UNEP/EEA/EPA composition rates) provides domain estimates today.
4. **CNN Image Inference Availability:**
   - Because `torch` / `torchvision` are commented out in `requirements.txt` and omitted from `requirements-cloud.txt` for CPU/memory constraints, image CNN inference routes return an honest `unavailable` / `model_loaded_no_inference` payload.
