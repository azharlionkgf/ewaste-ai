"""
E-Waste AI — Phase 4 Test Suite
================================
Tests for: DB, auth, batch management, AI engine, recovery, economics,
           decision support, environmental, reporting, research traceability.
Run: pytest tests/test_phase4_backend.py -v
"""

from __future__ import annotations

import json
import os
import sys
import types
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# ── Project root ──────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

# ── Lightweight DB for tests ───────────────────────────────────────────
os.environ["DATABASE_URL"] = "sqlite:///./database/test_phase4.db"
os.environ["SECRET_KEY"] = "test-secret-key-phase4-ewaste-ai"


# ══════════════════════════════════════════════════════════════════════
# TASK 1-2: Database & Models
# ══════════════════════════════════════════════════════════════════════

class TestDatabaseSetup:
    def test_import_database_module(self):
        from backend.database import Base, SessionLocal, engine, init_db, get_db
        assert Base is not None
        assert SessionLocal is not None

    def test_init_db_creates_tables(self):
        from backend.database import init_db, engine
        init_db()
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        expected = [
            "users", "audit_logs", "datasets", "ml_models", "model_evaluations",
            "waste_batches", "devices", "components", "materials", "inventory",
            "recovery_records", "processing_operations", "operational_costs",
            "ai_predictions", "environmental_reports", "generated_reports",
            "research_experiments",
        ]
        for table in expected:
            assert table in tables, f"Table '{table}' not created"

    def test_db_health_check(self):
        from backend.database import check_db_health
        assert check_db_health() is True

    def test_db_session_context_manager(self):
        from backend.database import db_session
        with db_session() as session:
            assert session is not None


class TestOrmModels:
    def test_user_model_import(self):
        from backend.models.all_models import User
        assert User.__tablename__ == "users"

    def test_waste_batch_model_import(self):
        from backend.models.all_models import WasteBatch
        assert WasteBatch.__tablename__ == "waste_batches"

    def test_ml_model_import(self):
        from backend.models.all_models import MLModel
        assert MLModel.__tablename__ == "ml_models"

    def test_ai_prediction_import(self):
        from backend.models.all_models import AIPrediction
        assert AIPrediction.__tablename__ == "ai_predictions"

    def test_all_models_imported_in_package(self):
        import backend.models as m
        assert hasattr(m, "User")
        assert hasattr(m, "WasteBatch")
        assert hasattr(m, "RecoveryRecord")
        assert hasattr(m, "InventoryItem")


# ══════════════════════════════════════════════════════════════════════
# TASK 11: Auth & Security
# ══════════════════════════════════════════════════════════════════════

class TestAuthService:
    def test_hash_and_verify_password(self):
        from backend.services.auth_service import hash_password, verify_password
        hashed = hash_password("MySecurePass123!")
        assert verify_password("MySecurePass123!", hashed) is True
        assert verify_password("WrongPassword", hashed) is False

    def test_create_and_decode_token(self):
        from backend.services.auth_service import create_access_token, decode_access_token
        token = create_access_token({"sub": "user-123", "role": "operator"})
        payload = decode_access_token(token)
        assert payload is not None
        assert payload["sub"] == "user-123"
        assert payload["role"] == "operator"

    def test_invalid_token_returns_none(self):
        from backend.services.auth_service import decode_access_token
        result = decode_access_token("not.a.real.token")
        assert result is None

    def test_hash_file_content(self):
        from backend.services.auth_service import hash_file_content
        content = b"test file content"
        h = hash_file_content(content)
        assert len(h) == 64  # SHA-256 hex length

    def test_sanitize_filename(self):
        from backend.services.auth_service import sanitize_filename
        # Path traversal is stripped — only the base filename is kept
        result = sanitize_filename("../../../etc/passwd")
        assert "passwd" in result
        assert ".." not in result
        assert "/" not in result
        assert sanitize_filename("my file.jpg") == "my file.jpg"

    def test_role_permissions(self):
        from backend.services.auth_service import has_permission
        assert has_permission("admin", "delete") is True
        assert has_permission("operator", "delete") is False
        assert has_permission("researcher", "manage_models") is True
        assert has_permission("operator", "read") is True

    def test_rate_limiting(self):
        from backend.services.auth_service import check_rate_limit
        # Should pass for first requests
        for _ in range(5):
            assert check_rate_limit("test-user-rl", max_requests=10, window_sec=60) is True

    def test_schemas_import(self):
        from backend.schemas.all_schemas import UserCreate, WasteBatchCreate, PredictionRequest
        assert UserCreate is not None
        assert WasteBatchCreate is not None


# ══════════════════════════════════════════════════════════════════════
# TASK 7: Batch Management
# ══════════════════════════════════════════════════════════════════════

class TestBatchManagement:
    @pytest.fixture
    def db(self):
        from backend.database import SessionLocal, init_db
        init_db()
        session = SessionLocal()
        yield session
        session.close()

    def test_create_batch(self, db):
        from backend.services.batch_service import BatchManagementService
        svc = BatchManagementService()
        batch = svc.create_batch(db, source="Test Company", weight_kg=50.0, location="Warehouse A")
        assert batch.id is not None
        assert batch.batch_number.startswith("EWASTE-")
        assert batch.source == "Test Company"
        assert batch.total_weight_kg == 50.0
        assert batch.status == "received"

    def test_get_batch(self, db):
        from backend.services.batch_service import BatchManagementService
        svc = BatchManagementService()
        batch = svc.create_batch(db, source="Retrieval Test", weight_kg=10.0)
        retrieved = svc.get_batch(db, batch.id)
        assert retrieved is not None
        assert retrieved.id == batch.id

    def test_update_batch_status(self, db):
        from backend.services.batch_service import BatchManagementService
        svc = BatchManagementService()
        batch = svc.create_batch(db, source="Status Test", weight_kg=5.0)
        updated = svc.update_status(db, batch.id, "sorted")
        assert updated.status == "sorted"

    def test_list_batches(self, db):
        from backend.services.batch_service import BatchManagementService
        svc = BatchManagementService()
        svc.create_batch(db, source="List Test A", weight_kg=1.0)
        svc.create_batch(db, source="List Test B", weight_kg=2.0)
        batches = svc.list_batches(db, limit=100)
        assert len(batches) >= 2

    def test_add_device_to_batch(self, db):
        from backend.services.batch_service import BatchManagementService
        svc = BatchManagementService()
        batch = svc.create_batch(db, source="Device Test", weight_kg=20.0)
        device = svc.add_device(db, batch.id, device_type="laptop", weight_kg=1.5, condition="damaged")
        assert device.id is not None
        assert device.device_type == "laptop"
        assert device.batch_id == batch.id

    def test_batch_history(self, db):
        from backend.services.batch_service import BatchManagementService
        svc = BatchManagementService()
        batch = svc.create_batch(db, source="History Test", weight_kg=30.0)
        history = svc.get_batch_history(db, batch.id)
        assert "batch" in history
        assert history["batch"]["source"] == "History Test"

    def test_batch_not_found(self, db):
        from backend.services.batch_service import BatchManagementService
        svc = BatchManagementService()
        result = svc.get_batch(db, "nonexistent-id")
        assert result is None


# ══════════════════════════════════════════════════════════════════════
# TASK 7: Inventory Management
# ══════════════════════════════════════════════════════════════════════

class TestInventoryManagement:
    @pytest.fixture
    def db(self):
        from backend.database import SessionLocal, init_db
        init_db()
        session = SessionLocal()
        yield session
        session.close()

    def test_add_inventory_item(self, db):
        from backend.services.batch_service import InventoryService
        svc = InventoryService()
        item = svc.add_item(db, material_name="copper", quantity_g=500.0, source="recycled")
        assert item.id is not None
        assert item.material_name == "copper"
        assert item.quantity_g == 500.0

    def test_get_inventory(self, db):
        from backend.services.batch_service import InventoryService
        svc = InventoryService()
        svc.add_item(db, material_name="gold_test", quantity_g=1.5)
        items = svc.get_inventory(db, material_name="gold_test")
        assert len(items) >= 1

    def test_inventory_summary(self, db):
        from backend.services.batch_service import InventoryService
        svc = InventoryService()
        summary = svc.get_summary(db)
        assert isinstance(summary, list)


# ══════════════════════════════════════════════════════════════════════
# TASK 3: AI Model Engine
# ══════════════════════════════════════════════════════════════════════

class TestAIModelEngine:
    def test_engine_instantiates(self):
        from backend.services.ai_model_service import AIModelEngine
        engine = AIModelEngine()
        assert engine is not None

    def test_list_available_models_empty_registry(self):
        from backend.services.ai_model_service import AIModelEngine
        engine = AIModelEngine()
        models = engine.list_available_models()
        assert isinstance(models, list)

    def test_check_availability_returns_dict(self):
        from backend.services.ai_model_service import AIModelEngine
        engine = AIModelEngine()
        availability = engine.check_availability()
        assert "ewaste_classification" in availability
        assert "device_identification" in availability
        assert "recovery_quantity" in availability

    def test_model_not_available_raises(self):
        from backend.services.ai_model_service import AIModelEngine, ModelNotAvailableError
        engine = AIModelEngine()
        with pytest.raises(ModelNotAvailableError):
            engine.predict_tabular({"feature1": 1.0}, "nonexistent_task_type")

    def test_singleton_pattern(self):
        from backend.services.ai_model_service import get_ai_engine
        engine1 = get_ai_engine()
        engine2 = get_ai_engine()
        assert engine1 is engine2

    def test_predict_with_mock_model(self):
        """Test prediction with an actual mock sklearn model."""
        import pickle
        import tempfile
        import numpy as np
        from sklearn.linear_model import LogisticRegression
        from sklearn.datasets import make_classification
        from backend.services.ai_model_service import AIModelEngine

        # Train a tiny real model
        X, y = make_classification(n_samples=100, n_features=4, n_informative=2, random_state=42)
        model = LogisticRegression()
        model.fit(X, y)

        with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as f:
            pickle.dump(model, f)
            model_path = f.name

        engine = AIModelEngine()
        engine._registry_data["test-mock-model"] = {
            "name": "Test Mock Model",
            "algorithm": "LogisticRegression",
            "task_type": "mock_classification",
            "version": "1.0.0",
            "status": "active",
            "file_path": model_path,
            "feature_columns": ["f1", "f2", "f3", "f4"],
        }

        result = engine.predict_tabular(
            {"f1": 0.5, "f2": -0.3, "f3": 1.2, "f4": 0.1},
            "mock_classification",
        )
        assert result["prediction_type"] == "actual_model"
        assert result["prediction"] in [0, 1]
        assert 0.0 <= result["confidence"] <= 1.0
        assert result["model_name"] == "Test Mock Model"

        # Cleanup
        import os
        os.unlink(model_path)


# ══════════════════════════════════════════════════════════════════════
# TASK 5: Recovery Intelligence
# ══════════════════════════════════════════════════════════════════════

class TestRecoveryIntelligence:
    @pytest.fixture
    def svc(self):
        from backend.services.recovery_service import RecoveryIntelligenceService
        return RecoveryIntelligenceService()

    def test_laptop_recovery_estimate(self, svc):
        result = svc.estimate_recovery("laptop", 1.5)
        assert result["device_type"] == "laptop"
        assert result["weight_kg"] == 1.5
        assert len(result["materials"]) > 0
        assert result["total_recoverable_g"] > 0

    def test_smartphone_recovery_estimate(self, svc):
        result = svc.estimate_recovery("smartphone", 0.2)
        materials = {m["material_name"] for m in result["materials"]}
        assert "gold" in materials
        assert "lithium" in materials

    def test_all_sources_labeled_rule_based(self, svc):
        result = svc.estimate_recovery("laptop", 1.0)
        for m in result["materials"]:
            assert m["source"] == "rule_based"

    def test_disclaimer_present(self, svc):
        result = svc.estimate_recovery("monitor", 5.0)
        assert "disclaimer" in result
        assert len(result["disclaimer"]) > 0

    def test_no_weight_returns_empty(self, svc):
        result = svc.estimate_recovery("laptop", None)
        assert result["total_recoverable_g"] == 0.0

    def test_unknown_device_uses_generic(self, svc):
        result = svc.estimate_recovery("unknown_device_xyz", 1.0)
        assert result["device_type"] == "generic"
        assert len(result["materials"]) > 0

    def test_hazardous_materials_flagged(self, svc):
        result = svc.estimate_recovery("laptop", 1.0)
        assert len(result["hazardous_materials"]) > 0

    def test_recommendations_present(self, svc):
        result = svc.estimate_recovery("smartphone", 0.2)
        assert len(result["recommendations"]) > 0


# ══════════════════════════════════════════════════════════════════════
# TASK 6: Economic Intelligence
# ══════════════════════════════════════════════════════════════════════

class TestEconomicIntelligence:
    @pytest.fixture
    def svc(self):
        from backend.services.economic_service import EconomicIntelligenceService
        return EconomicIntelligenceService()

    def test_economic_analysis_basic(self, svc):
        materials = [
            {"material_name": "gold", "recoverable_quantity_g": 0.3},
            {"material_name": "copper", "recoverable_quantity_g": 90.0},
        ]
        result = svc.analyze_batch_economics(materials, weight_kg=1.5)
        assert result["gross_recovery_value_usd"] > 0
        assert result["estimated_processing_cost_usd"] > 0
        assert "disclaimer" in result

    def test_net_value_calculation(self, svc):
        materials = [{"material_name": "gold", "recoverable_quantity_g": 1.0}]
        result = svc.analyze_batch_economics(materials, weight_kg=1.0)
        expected_net = result["gross_recovery_value_usd"] - result["estimated_processing_cost_usd"]
        assert abs(result["net_value_usd"] - expected_net) < 0.01

    def test_price_reference(self, svc):
        price = svc.get_price_reference("gold")
        assert price is not None
        assert price["price_per_g_usd"] > 0
        assert "source" in price

    def test_unknown_material_no_price(self, svc):
        price = svc.get_price_reference("unobtanium")
        assert price is None

    def test_disclaimer_present(self, svc):
        result = svc.analyze_batch_economics([], weight_kg=1.0)
        assert "disclaimer" in result
        assert "ESTIMATES" in result["disclaimer"] or "estimates" in result["disclaimer"].lower()

    def test_all_prices_dict(self, svc):
        prices = svc.all_prices()
        assert "prices_usd_per_g" in prices
        assert "gold" in prices["prices_usd_per_g"]


# ══════════════════════════════════════════════════════════════════════
# TASK 8: Decision Support
# ══════════════════════════════════════════════════════════════════════

class TestDecisionSupport:
    @pytest.fixture
    def svc(self):
        from backend.services.decision_service import DecisionSupportService
        return DecisionSupportService()

    def test_laptop_recommendations(self, svc):
        result = svc.get_recommendations("laptop")
        assert len(result["recommendations"]) > 0
        assert "battery" in str(result["recommendations"]).lower()

    def test_hazard_flags_included(self, svc):
        result = svc.get_recommendations("laptop")
        assert len(result["hazard_flags"]) > 0

    def test_disclaimer_always_present(self, svc):
        result = svc.get_recommendations("unknown")
        assert "DISCLAIMER" in result["disclaimer"]

    def test_reasoning_list_not_empty(self, svc):
        result = svc.get_recommendations("smartphone")
        assert len(result["reasoning"]) > 0

    def test_device_type_normalization(self, svc):
        result1 = svc.get_recommendations("laptop")
        result2 = svc.get_recommendations("notebook")
        assert result1["device_type"] == result2["device_type"] == "laptop"


# ══════════════════════════════════════════════════════════════════════
# TASK 9: Environmental Reporting
# ══════════════════════════════════════════════════════════════════════

class TestEnvironmentalReporting:
    @pytest.fixture
    def db(self):
        from backend.database import SessionLocal, init_db
        init_db()
        session = SessionLocal()
        yield session
        session.close()

    def test_period_summary_runs(self, db):
        from backend.services.environmental_service import EnvironmentalReportingService
        svc = EnvironmentalReportingService()
        summary = svc.get_period_summary(db)
        assert "total_waste_kg" in summary
        assert "recycling_rate_percent" in summary

    def test_batch_env_report_missing_batch(self, db):
        from backend.services.environmental_service import EnvironmentalReportingService
        svc = EnvironmentalReportingService()
        result = svc.generate_batch_environmental_report(db, "nonexistent-id")
        assert "error" in result

    def test_batch_env_report_complete(self, db):
        from backend.services.batch_service import BatchManagementService
        from backend.services.environmental_service import EnvironmentalReportingService
        batch_svc = BatchManagementService()
        env_svc = EnvironmentalReportingService()
        batch = batch_svc.create_batch(db, source="Env Report Test", weight_kg=100.0)
        result = env_svc.generate_batch_environmental_report(db, batch.id)
        assert result["total_waste_kg"] == 100.0
        assert result["is_certified"] is False
        assert "certification_note" in result


# ══════════════════════════════════════════════════════════════════════
# TASK 10: Report Generation
# ══════════════════════════════════════════════════════════════════════

class TestReportGeneration:
    @pytest.fixture
    def svc(self):
        from backend.services.report_service import ReportGenerationService
        return ReportGenerationService()

    def test_batch_report_json(self, svc):
        result = svc.generate_batch_report({"batch_number": "TEST-001", "source": "Test"})
        assert result.get("success") is True
        assert result.get("file_format") == "json"
        assert result.get("file_size_bytes", 0) > 0

    def test_recovery_report_json(self, svc):
        result = svc.generate_recovery_report(
            {"device_type": "laptop", "total_recoverable_g": 150.0, "disclaimer": "Test"}
        )
        assert result.get("success") is True

    def test_financial_report_json(self, svc):
        result = svc.generate_financial_report(
            {"net_value_usd": 25.0, "disclaimer": "Test", "price_data_date": "2024-01-01"}
        )
        assert result.get("success") is True

    def test_environmental_report_json(self, svc):
        result = svc.generate_environmental_report({"recycling_rate_percent": 60.0})
        assert result.get("success") is True

    def test_inventory_report_json(self, svc):
        items = [{"material": "gold", "total_quantity_g": 2.5}]
        result = svc.generate_inventory_report(items)
        assert result.get("success") is True

    def test_ai_prediction_report_json(self, svc):
        preds = [{"id": "1", "task": "classification", "prediction": "laptop", "confidence": 0.9}]
        result = svc.generate_ai_report(preds)
        assert result.get("success") is True

    def test_research_report_json(self, svc):
        experiments = [{"name": "exp1", "metrics": {"accuracy": 0.85}}]
        result = svc.generate_research_report(experiments)
        assert result.get("success") is True

    def test_report_csv_format(self, svc):
        result = svc.generate_inventory_report(
            [{"material": "copper", "total_quantity_g": 500.0}],
            format="csv"
        )
        assert result.get("success") is True


# ══════════════════════════════════════════════════════════════════════
# TASK 14: Research Traceability
# ══════════════════════════════════════════════════════════════════════

class TestResearchTraceability:
    @pytest.fixture
    def db(self):
        from backend.database import SessionLocal, init_db
        init_db()
        session = SessionLocal()
        yield session
        session.close()

    def test_research_experiment_creation(self, db):
        from backend.models.all_models import ResearchExperiment
        exp = ResearchExperiment(
            experiment_name="Phase4 Traceability Test",
            objective="Verify research traceability in Phase 4 backend",
            model_architecture="LogisticRegression",
            hyperparameters={"C": 1.0, "max_iter": 1000},
            random_seed=42,
            evaluation_protocol="80/10/10 split",
            metrics={"val_accuracy": 0.875, "val_f1": 0.874},
            duration_sec=0.02,
            library_versions={"scikit-learn": "1.8.0", "python": "3.13.7"},
            status="completed",
        )
        db.add(exp)
        db.commit()
        db.refresh(exp)
        assert exp.id is not None
        assert exp.random_seed == 42
        assert exp.metrics["val_accuracy"] == 0.875

    def test_prediction_provenance_recorded(self, db):
        from backend.models.all_models import AIPrediction
        pred = AIPrediction(
            model_name="TestModel",
            model_version="1.0.0",
            task_type="ewaste_classification",
            input_type="tabular",
            prediction={"class": "laptop"},
            confidence=0.92,
            prediction_type="actual_model",
            dataset_version="1.0.0",
        )
        db.add(pred)
        db.commit()
        db.refresh(pred)
        assert pred.id is not None
        assert pred.dataset_version == "1.0.0"
        assert pred.prediction_type == "actual_model"


# ══════════════════════════════════════════════════════════════════════
# TASK 12: Config & Application
# ══════════════════════════════════════════════════════════════════════

class TestConfiguration:
    def test_config_imports(self):
        from backend.config import (
            DATABASE_URL, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES,
            UPLOAD_DIR, MODEL_REGISTRY_DIR, REPORTS_DIR, API_VERSION,
        )
        assert DATABASE_URL is not None
        assert SECRET_KEY is not None
        assert ALGORITHM == "HS256"
        assert ACCESS_TOKEN_EXPIRE_MINUTES > 0
        assert API_VERSION == "v1"

    def test_directories_created(self):
        from backend.config import UPLOAD_DIR, MODEL_REGISTRY_DIR, REPORTS_DIR, LOG_DIR
        assert UPLOAD_DIR.exists()
        assert MODEL_REGISTRY_DIR.exists()
        assert REPORTS_DIR.exists()
        assert LOG_DIR.exists()

    def test_max_upload_size_configured(self):
        from backend.config import MAX_UPLOAD_BYTES, MAX_UPLOAD_SIZE_MB
        assert MAX_UPLOAD_BYTES == MAX_UPLOAD_SIZE_MB * 1024 * 1024
        assert MAX_UPLOAD_BYTES > 0


class TestFastAPIApp:
    def test_app_imports_without_error(self):
        from backend.main import app
        assert app.title is not None
        assert "4.0.0" in app.version

    def test_fastapi_routes_registered(self):
        from backend.main import app
        routes = [r.path for r in app.routes]
        assert "/" in routes
        assert "/health" in routes
        assert any("api/v1" in r for r in routes)
