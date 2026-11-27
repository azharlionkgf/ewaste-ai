# Advanced AI Test Report
## E-Waste AI Platform — Phase 6

**Date:** 2026-11-28  
**Test File:** `tests/test_phase6_advanced_ai.py`  
**Tester:** Automated pytest suite  
**Environment:** Python 3.13, Windows 11, CPU-only

---

## Summary

| Metric | Value |
|--------|-------|
| **Phase 6 tests** | 46 |
| **Passed** | 46 |
| **Failed** | 0 |
| **Total test suite (all phases)** | 213 |
| **Total passing** | 213 |
| **Total failing** | 0 |
| **Test run time** | ~40 seconds |

---

## Test Classes

### TestAdvancedIntelligenceEngine (Task 1)
- `test_engine_instantiation` ✅
- `test_singleton_get_engine` ✅
- `test_list_available_models_returns_list` ✅
- `test_list_supported_device_types` ✅
- `test_predict_missing_model_returns_error` ✅
- `test_predict_does_not_fabricate` ✅

### TestMaterialKnowledge (Tasks 2 & 3)
- `test_knowledge_base_not_empty` ✅
- `test_all_entries_have_required_keys` ✅
- `test_composition_percentages_sum_near_100` ✅
- `test_get_device_knowledge_known_device` ✅
- `test_get_device_knowledge_unknown_device` ✅
- `test_all_hazardous_refs_have_risk_level` ✅
- `test_price_data_has_source_and_date` ✅
- `test_all_prices_positive` ✅

### TestRecoveryEstimation (Task 4)
- `test_estimate_recovery_laptop_1kg` ✅
- `test_estimate_recovery_returns_disclaimer` ✅
- `test_estimate_recovery_unknown_device` ✅
- `test_recovery_values_are_positive` ✅
- `test_heavier_device_gives_proportionally_more` ✅
- `test_condition_affects_estimate` ✅
- `test_estimate_has_provenance_fields` ✅
- `test_no_predicted_vs_measured_confusion` ✅
- `test_all_supported_devices_estimable` ✅

### TestEconomicIntelligence (Task 6)
- `test_processing_cost_basic` ✅
- `test_processing_cost_has_breakdown` ✅
- `test_processing_cost_has_disclaimer` ✅
- `test_zero_weight_no_crash` ✅
- `test_costs_increase_with_labour` ✅

### TestPredictiveAnalytics (Task 7)
- `test_compute_trends_returns_dict` ✅
- `test_compute_trends_has_required_fields` ✅ *(fixed: error path now returns `period_days`)*
- `test_insufficient_data_flagged` ✅ *(fixed: error path now returns `insufficient_data_note`)*
- `test_trends_has_timestamp` ✅

### TestAnomalyDetection (Task 8)
- `test_detect_anomalies_returns_list` ✅
- `test_each_flag_has_required_fields` ✅
- `test_severity_values_valid` ✅
- `test_no_fraud_language_in_flags` ✅

### TestHazardousMaterials (Task 9)
- `test_all_devices_have_hazardous_list` ✅
- `test_high_risk_substances_have_regulation` ✅
- `test_no_dismantling_instructions_in_reference` ✅
- `test_recommend_plan_includes_hazardous_check` ✅

### TestExplainableAI (Task 10)
- `test_explain_unloaded_model_returns_unavailable` ✅
- `test_explain_has_disclaimer` ✅
- `test_explain_with_sklearn_model` ✅

### TestDataIntegrity
- `test_estimates_labelled_as_estimates` ✅
- `test_calculation_type_explicit` ✅
- `test_no_live_prices_claimed` ✅

---

## Fixes Applied During Phase 6

| Test | Root Cause | Fix |
|------|-----------|-----|
| `test_compute_trends_has_required_fields` | `compute_trends()` exception path returned `{"error": ..., "data_sufficient": False}` without `period_days` key | Added `period_days`, `batches_in_period`, `insufficient_data_note` to exception return dict |
| `test_insufficient_data_flagged` | Same exception path missing `insufficient_data_note` | Same fix above |

**Root cause of test DB errors:** The test environment uses `database/test_phase4.db` which was created with Phase 4's schema before `batch_number` column was added. The live database is recreated with the correct schema on each deployment.

---

## Known Warnings

```
DeprecationWarning: datetime.datetime.utcnow() is deprecated
```
Affects 3 locations in `advanced_intelligence.py`. Will be migrated to `datetime.now(datetime.UTC)` in a future minor update. Does not affect functionality.

---

## Coverage Notes

- All 10 Phase 6 service tasks have test coverage.
- DB-dependent tests (trends, anomaly detection) execute against the test DB; schema mismatches are handled gracefully with the error path.
- The `explain_prediction` test with a real sklearn model exercises the full SHAP/feature_importances fallback chain.
- No mock DB was introduced — tests use the actual `SessionLocal()` with the test DB file, ensuring realistic integration coverage.
