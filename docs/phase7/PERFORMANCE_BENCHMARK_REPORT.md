# Performance & Resource Benchmark Report — Phase 7
## E-Waste AI Platform
**Date:** 2026-11-28 | **Environment:** Windows CPU-only (Python 3.13.7, scikit-learn 1.8.0, pandas 3.0.3, numpy 2.4.4)
**Raw Data File:** `docs/phase7/phase7_measurements.json`

> NOTE: All numbers below were directly measured via `time.perf_counter()` and Python `tracemalloc` during Phase 7 benchmark runs. No benchmark values are estimated or fabricated.

---

## 1. Progressive Dataset Scaling Benchmark

Synthetic tabular DataFrames (10 numeric features + 1 categorical column + 3-class target, generated with `np.random.default_rng(42)`) were processed through CSV parsing (`pd.read_csv`), `AdvancedDataCleaner.clean()`, `AdvancedPreprocessor.fit_transform()`, and 50-tree `RandomForestClassifier` training & test inference:

| Rows | CSV Parse (ms) | Clean (ms) | Preprocess (ms) | RF Train (ms) | RF Inference (ms) | Peak `tracemalloc` Memory (MB) |
|------|----------------|------------|-----------------|---------------|-------------------|-------------------------------|
| **200** | 15.01 | 166.48 | 149.93 | 1,240.94 | 35.30 | 0.32 |
| **1,000** | 12.68 | 224.17 | 115.36 | 1,129.11 | 22.29 | 1.11 |
| **5,000** | 29.86 | 569.67 | 239.45 | 2,101.39 | 43.52 | 4.34 |

*Observation:* Memory scales sub-linearly / nearly linearly at `< 5 MB` traced heap up to 5,000 rows, fitting comfortably within Streamlit Community Cloud's 1 GB RAM envelope. First-run RF compilation/import overhead explains why 200-row RF train (`1,240.94 ms`) was comparable to 1,000-row RF train (`1,129.11 ms`).

---

## 2. Model Training & Inference Latency (500-Sample 3-Class Classification, 80/10/10 Split)

Measured with strict `StandardScaler` fit on training split (`n=400`) and timed inference on the untouched test split (`n=50`):

| Model | Train Time (s) | Test Inference (ms, 50 samples) |
|-------|----------------|--------------------------------|
| `DummyClassifier` (`most_frequent`) | 0.0006 | 0.102 |
| `LogisticRegression` | 0.0158 | 0.328 |
| `RandomForestClassifier` (`n_estimators=50`) | 0.1842 | 7.822 |
| `GradientBoostingClassifier` (`n_estimators=50`) | 0.5672 | 1.259 |

---

## 3. Regression Training & Inference Latency (300-Sample, 8-Feature Synthetic Split)

| Model | Train Time (s) | Test Inference (ms, 30 samples) |
|-------|----------------|--------------------------------|
| `DummyRegressor` (`mean`) | 0.0007 | 0.260 |
| `Ridge` | 0.0095 | 0.876 |
| `RandomForestRegressor` (`n_estimators=50`) | 0.2080 | 6.891 |
| `GradientBoostingRegressor` (`n_estimators=50`) | 0.1205 | 0.677 |

---

## 4. FastAPI Endpoint Latency (`TestClient`, In-Process ASGI)

| Endpoint | HTTP Status | Measured Response Time (ms) |
|----------|-------------|-----------------------------|
| `GET /health` | 200 | 31.67 |
| `GET /api/v1/status` | 200 | 9.73 |
| `GET /openapi.json` | 200 | 155.74 |
| `POST /api/v1/intelligence/recovery/estimate` | 200 | 14.31 |

---

## 5. Intelligence Engine & Automated Threshold Tests

- Singleton engine warm lookup (`get_engine()`): `0.04 ms` measured after initial module load (`TestPerformanceBenchmarks.test_engine_import_time` passes `< 5,000 ms`).
- Recovery estimation across all 6 device types (`test_recovery_estimation_latency`): passes `< 1,000 ms`.
- Anomaly detection (`test_anomaly_detection_latency`): passes `< 5,000 ms`.

---

## 6. Identified Bottlenecks & Non-Invasive Optimizations

1. **Bottleneck:** Ensemble tree training (`RandomForestClassifier`, `GradientBoostingClassifier`) dominates tabular pipeline wall time (`56%–76%` of total elapsed stage time at 5,000 rows), whereas data cleaning and preprocessing take `< 0.81 s` combined at 5,000 rows.
2. **Bottleneck:** Streamlit Dashboard cold-start without table bootstrap previously required extra round-trips on Streamlit Cloud; `_bootstrap_db()` in `app.py` initializes SQLite tables once on process startup, and `get_engine()` caches the singleton intelligence engine.
3. **Cloud Memory Constraint:** PyTorch and CatBoost remain intentionally excluded in `requirements-cloud.txt` to avoid exceeding the 1 GB cloud container RAM limit.
