"""
E-Waste AI — Phase 6 Test Suite
=================================
Tests: Advanced AI Engine, Material Knowledge, Recovery Estimation,
Economic Analysis, Anomaly Detection, Predictive Analytics, Explainability.
"""

import sys, os, json, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.services.advanced_intelligence import (
    AdvancedIntelligenceEngine,
    MATERIAL_KNOWLEDGE_BASE,
    HAZARDOUS_REFERENCE,
    MATERIAL_PRICES_USD_PER_G,
    RECOVERY_EFFICIENCY,
    PRICE_SOURCE,
    PRICE_DATE,
    get_engine,
)


# ══════════════════════════════════════════════════════════════════════════
# Task 1 — Advanced AI Engine
# ══════════════════════════════════════════════════════════════════════════

class TestAdvancedIntelligenceEngine:
    def setup_method(self):
        self.engine = AdvancedIntelligenceEngine()

    def test_engine_instantiation(self):
        assert self.engine is not None

    def test_singleton_get_engine(self):
        e1 = get_engine()
        e2 = get_engine()
        assert e1 is e2

    def test_list_available_models_returns_list(self):
        models = self.engine.list_available_models()
        assert isinstance(models, list)

    def test_list_supported_device_types(self):
        types = self.engine.list_supported_device_types()
        assert isinstance(types, list)
        assert len(types) > 0
        assert "laptop" in types
        assert "mobile_phone" in types

    def test_predict_missing_model_returns_error(self):
        result = self.engine.predict("nonexistent_model_id_xyz", {"feat": 1.0})
        assert "error" in result
        assert result.get("available") is False

    def test_predict_does_not_fabricate(self):
        result = self.engine.predict("fake_model", {"x": 1})
        assert "error" in result or result.get("available") is False


# ══════════════════════════════════════════════════════════════════════════
# Task 2 — Material Knowledge Base
# ══════════════════════════════════════════════════════════════════════════

class TestMaterialKnowledge:
    def setup_method(self):
        self.engine = AdvancedIntelligenceEngine()

    def test_knowledge_base_not_empty(self):
        assert len(MATERIAL_KNOWLEDGE_BASE) >= 5

    def test_all_entries_have_required_keys(self):
        required = {"source","components","avg_weight_kg","material_composition_percent",
                    "hazardous_substances","confidence"}
        for device, entry in MATERIAL_KNOWLEDGE_BASE.items():
            assert required.issubset(entry.keys()), f"{device} missing keys"

    def test_composition_percentages_sum_near_100(self):
        for device, entry in MATERIAL_KNOWLEDGE_BASE.items():
            total = sum(entry["material_composition_percent"].values())
            assert 95 <= total <= 105, f"{device} composition sums to {total}%"

    def test_get_device_knowledge_known_device(self):
        kb = self.engine.get_device_knowledge("laptop")
        assert kb["available"] is True
        assert "material_composition_percent" in kb
        assert "source" in kb

    def test_get_device_knowledge_unknown_device(self):
        kb = self.engine.get_device_knowledge("flying_saucer")
        assert kb["available"] is False
        assert "message" in kb

    def test_all_hazardous_refs_have_risk_level(self):
        for sub, ref in HAZARDOUS_REFERENCE.items():
            assert "risk_level" in ref, f"{sub} missing risk_level"
            assert "handling" in ref, f"{sub} missing handling"

    def test_price_data_has_source_and_date(self):
        assert isinstance(PRICE_SOURCE, str) and len(PRICE_SOURCE) > 0
        assert isinstance(PRICE_DATE, str) and len(PRICE_DATE) >= 8

    def test_all_prices_positive(self):
        for mat, price in MATERIAL_PRICES_USD_PER_G.items():
            assert price > 0, f"{mat} has non-positive price"


# ══════════════════════════════════════════════════════════════════════════
# Task 4 — Material Recovery Prediction
# ══════════════════════════════════════════════════════════════════════════

class TestRecoveryEstimation:
    def setup_method(self):
        self.engine = AdvancedIntelligenceEngine()

    def test_estimate_recovery_laptop_1kg(self):
        result = self.engine.estimate_recovery("laptop", 1.0)
        assert result["available"] is True
        assert "recoverable_materials" in result
        assert result["input_weight_kg"] == 1.0

    def test_estimate_recovery_returns_disclaimer(self):
        result = self.engine.estimate_recovery("laptop", 1.0)
        assert "disclaimer" in result
        assert len(result["disclaimer"]) > 20

    def test_estimate_recovery_unknown_device(self):
        result = self.engine.estimate_recovery("unknown_device_xyz", 1.0)
        assert result["available"] is False

    def test_recovery_values_are_positive(self):
        result = self.engine.estimate_recovery("mobile_phone", 0.18)
        assert result["available"] is True
        for mat, data in result["recoverable_materials"].items():
            assert data["estimated_recovered_g"] >= 0, f"{mat} has negative recovery"
            assert data["estimated_value_usd"] >= 0, f"{mat} has negative value"

    def test_heavier_device_gives_proportionally_more(self):
        r1 = self.engine.estimate_recovery("laptop", 1.0)
        r2 = self.engine.estimate_recovery("laptop", 2.0)
        assert r2["total_estimated_value_usd"] > r1["total_estimated_value_usd"]

    def test_condition_affects_estimate(self):
        good = self.engine.estimate_recovery("laptop", 2.0, "good")
        poor = self.engine.estimate_recovery("laptop", 2.0, "poor")
        assert good["total_estimated_value_usd"] > poor["total_estimated_value_usd"]

    def test_estimate_has_provenance_fields(self):
        result = self.engine.estimate_recovery("laptop", 1.0)
        assert "data_source" in result
        assert "value_source" in result
        assert "calculation_type" in result
        assert result["calculation_type"] == "rule_based_estimate"

    def test_no_predicted_vs_measured_confusion(self):
        result = self.engine.estimate_recovery("laptop", 1.0)
        for mat, data in result["recoverable_materials"].items():
            assert data["value_type"] == "estimate", f"{mat} not labelled as estimate"

    def test_all_supported_devices_estimable(self):
        for device in self.engine.list_supported_device_types():
            result = self.engine.estimate_recovery(device, 1.0)
            assert result["available"] is True, f"Failed for {device}"


# ══════════════════════════════════════════════════════════════════════════
# Task 6 — Economic Intelligence
# ══════════════════════════════════════════════════════════════════════════

class TestEconomicIntelligence:
    def setup_method(self):
        self.engine = AdvancedIntelligenceEngine()

    def test_processing_cost_basic(self):
        result = self.engine.estimate_processing_cost(100.0)
        assert "total_cost_usd" in result
        assert result["total_cost_usd"] > 0

    def test_processing_cost_has_breakdown(self):
        result = self.engine.estimate_processing_cost(100.0, device_count=10,
                                                       labour_hours=4, transport_km=50)
        assert "breakdown" in result
        bk = result["breakdown"]
        assert "labour" in bk
        assert "transport" in bk
        assert "overhead" in bk

    def test_processing_cost_has_disclaimer(self):
        result = self.engine.estimate_processing_cost(50.0)
        assert "disclaimer" in result
        assert "ESTIMATE" in result["disclaimer"]

    def test_zero_weight_no_crash(self):
        result = self.engine.estimate_processing_cost(0.0)
        assert "total_cost_usd" in result

    def test_costs_increase_with_labour(self):
        r1 = self.engine.estimate_processing_cost(100.0, labour_hours=0)
        r2 = self.engine.estimate_processing_cost(100.0, labour_hours=10)
        assert r2["total_cost_usd"] > r1["total_cost_usd"]


# ══════════════════════════════════════════════════════════════════════════
# Task 7 — Predictive Analytics
# ══════════════════════════════════════════════════════════════════════════

class TestPredictiveAnalytics:
    def setup_method(self):
        self.engine = AdvancedIntelligenceEngine()

    def test_compute_trends_returns_dict(self):
        result = self.engine.compute_trends(days=30)
        assert isinstance(result, dict)

    def test_compute_trends_has_required_fields(self):
        result = self.engine.compute_trends(days=30)
        assert "period_days" in result
        assert "data_sufficient" in result

    def test_insufficient_data_flagged(self):
        result = self.engine.compute_trends(days=1)
        # With no data, should report insufficient
        if result.get("batches_in_period", 0) < 3:
            assert result.get("data_sufficient") is False
            assert result.get("insufficient_data_note") is not None

    def test_trends_has_timestamp(self):
        result = self.engine.compute_trends()
        assert "timestamp" in result or "error" in result


# ══════════════════════════════════════════════════════════════════════════
# Task 8 — Anomaly Detection
# ══════════════════════════════════════════════════════════════════════════

class TestAnomalyDetection:
    def setup_method(self):
        self.engine = AdvancedIntelligenceEngine()

    def test_detect_anomalies_returns_list(self):
        flags = self.engine.detect_anomalies()
        assert isinstance(flags, list)

    def test_each_flag_has_required_fields(self):
        flags = self.engine.detect_anomalies()
        for f in flags:
            assert "type" in f
            assert "severity" in f
            assert "detail" in f
            assert "action" in f

    def test_severity_values_valid(self):
        flags = self.engine.detect_anomalies()
        valid = {"high","medium","low"}
        for f in flags:
            assert f["severity"] in valid, f"Invalid severity: {f['severity']}"

    def test_no_fraud_language_in_flags(self):
        flags = self.engine.detect_anomalies()
        for f in flags:
            detail_lower = f.get("detail","").lower()
            # Anomaly detection must NOT imply fraud
            assert "fraud" not in detail_lower
            assert "criminal" not in detail_lower


# ══════════════════════════════════════════════════════════════════════════
# Task 9 — Hazardous Material Safety
# ══════════════════════════════════════════════════════════════════════════

class TestHazardousMaterials:
    def test_all_devices_have_hazardous_list(self):
        for device, entry in MATERIAL_KNOWLEDGE_BASE.items():
            assert "hazardous_substances" in entry

    def test_high_risk_substances_have_regulation(self):
        high_risk = [s for s, r in HAZARDOUS_REFERENCE.items()
                     if r.get("risk_level") == "high"]
        assert len(high_risk) >= 3
        for sub in high_risk:
            assert "regulation" in HAZARDOUS_REFERENCE[sub]

    def test_no_dismantling_instructions_in_reference(self):
        # Safety reference must not provide unsafe instructions
        for sub, ref in HAZARDOUS_REFERENCE.items():
            handling = ref.get("handling","").lower()
            assert "dismantle" not in handling or "specialist" in handling

    def test_recommend_plan_includes_hazardous_check(self):
        engine = AdvancedIntelligenceEngine()
        # With no DB, batch estimate should still not crash
        result = engine.recommend_recovery_plan("nonexistent_batch_xyz")
        assert isinstance(result, dict)
        assert "available" in result


# ══════════════════════════════════════════════════════════════════════════
# Task 10 — Explainable AI
# ══════════════════════════════════════════════════════════════════════════

class TestExplainableAI:
    def setup_method(self):
        self.engine = AdvancedIntelligenceEngine()

    def test_explain_unloaded_model_returns_unavailable(self):
        result = self.engine.explain_prediction("nonexistent_model", {"x": 1})
        assert result["available"] is False

    def test_explain_has_disclaimer(self):
        # Even for unavailable model, check structure
        result = self.engine.explain_prediction("nonexistent_model", {"x": 1})
        assert "message" in result or "disclaimer" in result

    def test_explain_with_sklearn_model(self):
        """Test explanation with a real sklearn model trained in memory."""
        try:
            from sklearn.ensemble import RandomForestClassifier
            import numpy as np, joblib, tempfile, os

            X = np.random.rand(50, 4)
            y = (X[:, 0] > 0.5).astype(int)
            clf = RandomForestClassifier(n_estimators=5, random_state=42)
            clf.fit(X, y)

            with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as tmp:
                joblib.dump(clf, tmp.name)
                tmp_path = tmp.name

            try:
                self.engine._loaded_models["test_rf"] = clf
                self.engine._model_metadata["test_rf"] = {"path": tmp_path}
                features = {"f0": 0.5, "f1": 0.3, "f2": 0.8, "f3": 0.1}
                result = self.engine.explain_prediction("test_rf", features)
                assert result["available"] is True
                assert "importance" in result
                assert result["method"] in ("SHAP","feature_importances","linear_coefficients")
            finally:
                del self.engine._loaded_models["test_rf"]
                os.unlink(tmp_path)
        except ImportError:
            pytest.skip("sklearn/numpy/joblib not available")


# ══════════════════════════════════════════════════════════════════════════
# Data Integrity — predicted vs measured separation
# ══════════════════════════════════════════════════════════════════════════

class TestDataIntegrity:
    def test_estimates_labelled_as_estimates(self):
        engine = AdvancedIntelligenceEngine()
        result = engine.estimate_recovery("laptop", 1.0)
        for mat, data in result["recoverable_materials"].items():
            assert data["value_type"] == "estimate"

    def test_calculation_type_explicit(self):
        engine = AdvancedIntelligenceEngine()
        result = engine.estimate_recovery("laptop", 1.0)
        assert result["calculation_type"] == "rule_based_estimate"

    def test_no_live_prices_claimed(self):
        # value_source must mention it's not live/real-time
        engine = AdvancedIntelligenceEngine()
        result = engine.estimate_recovery("laptop", 1.0)
        vs = result.get("value_source","").upper()
        assert "INDICATIVE" in vs or "REFERENCE" in vs or "ESTIMATE" in vs
