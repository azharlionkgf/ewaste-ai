# Research Dataset Provenance Report — Phase 7
## E-Waste AI Platform
**Date:** 2026-11-28

---

## 1. Repository Dataset Inventory (`data/`)

Recursive inspection of `data/` across all subdirectories (`annotations`, `augmented`, `cleaned`, `exports`, `images`, `processed`, `raw`, `splits`, `uploads`, `videos`) confirms:

- **Real User / Benchmark Datasets On Disk:** **None (0 dataset files)**. Every subdirectory currently contains only `.gitkeep` (0 bytes).
- **Local Test/App Database (`database/ewaste_ai.db`):** Initialized cleanly with 20 schema tables; zero pre-loaded external e-waste benchmark records.

---

## 2. Synthetic & Reference Datasets Used in System Verification

Because no real external e-waste dataset files exist in the repository yet, all ML model artifacts and Phase 3 / Phase 7 validation runs are strictly documented with **SYNTHETIC** provenance:

| Dataset Identifier | Source / Generator | Composition & Size | Features & Target | Limitations / Bias / Missing Values | Status |
|--------------------|--------------------|--------------------|-------------------|-------------------------------------|--------|
| **`synthetic_200x10_3class`** (Phase 3 registry) | `sklearn.datasets.make_classification` (`seed=42`) | 200 records (`128` train / `32` val / `40` test) | 10 continuous synthetic features; 3 abstract classes (`0, 1, 2`) | Purely mathematical isotropic/informative synthetic clusters; no physical e-waste semantics; zero missing values | Synthetic Pipeline Validation Only |
| **`synthetic_reg_150`** (Phase 3 history) | `sklearn.datasets.make_regression` (`seed=42`) | 150 records | Synthetic numeric features; continuous target | No units or domain sensor noise; validation only | Synthetic Pipeline Validation Only |
| **`synthetic_classification_500x10_3class`** (Phase 7) | `sklearn.datasets.make_classification` (`n_samples=500, n_features=10, n_informative=5, n_classes=3, random_state=42`) | 500 records (`400` train / `50` val / `50` test) | 10 standardized float features; 3 balanced classes | Clean, zero missing values, linear/nonlinear synthetic boundary; must NOT be cited as real recycling accuracy | Synthetic Pipeline Validation Only |
| **`synthetic_regression_300x8`** (Phase 7) | `sklearn.datasets.make_regression` (`n_samples=300, n_features=8, n_informative=5, noise=10.0, random_state=42`) | 300 records (`240` train / `30` val / `30` test) | 8 standardized float features; continuous target | Gaussian additive noise (`σ=10.0`); linear dominant trend favors linear/ridge estimators | Synthetic Pipeline Validation Only |

---

## 3. Domain Reference Knowledge Provenance (Rule-Based Layer)

While ML models currently validate on synthetic data, deterministic material composition and hazardous category estimates in `backend/services/recovery_service.py` and `backend/services/advanced_intelligence.py` are derived from documented secondary literature surveys (`UNEP`, `EEA`, `EPA`, `Öko-Institut` cited inside code constants) and `2024-01-15` indicative LME/commodity reference prices (`economic_service.py`).

- **License / Usage Condition Note:** Secondary summary factors stored as internal engineering heuristics for estimation only — **not** certified material assay certificates or live market feeds.

---

## 4. Governance Rules Enforced

1. **Strict Separation:** Synthetic validation results are never presented as empirical e-waste domain accuracy.
2. **Database Separation:** `Dataset.source`, `RecoveryRecord.value_source`, and `AIPrediction.prediction_type` distinguish `actual_model`, `rule_based`, `measured`, and `estimated` origins.
3. **Onboarding Checklist for Real Datasets:** When adding real e-waste CSV or image datasets to `data/raw/` or `data/images/`, record source URL/organization, download date, open license terms, record/image count, class distribution balance, missingness %, and exact version checksum before running experiments.
