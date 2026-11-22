"""
E-Waste AI — Foundation Tests
================================
Smoke tests for Phase 0 — verifies project foundation is correct.
Run: pytest tests/test_foundation.py -v
"""

import sys
import os
import pytest

# Add project root
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


class TestProjectStructure:
    """Verify the project directory structure is correct."""

    REQUIRED_DIRS = [
        "backend", "backend/models", "backend/schemas",
        "backend/routers", "backend/services",
        "ml", "ml/models", "ml/training", "ml/evaluation",
        "ml/inference", "ml/data",
        "intelligence", "frontend", "frontend/components",
        "frontend/pages", "data/uploads", "data/processed",
        "data/images", "data/videos", "data/exports",
        "saved_models", "reports", "tests", "docs", "logs",
    ]

    REQUIRED_FILES = [
        "app.py", "README.md", "TASK_STATUS.md",
        "requirements.txt", ".gitignore", "config.yaml",
        ".env.example", "backend/main.py", "backend/config.py",
        "backend/database.py", "backend/logger.py",
        "frontend/theme.py",
        "frontend/components/sidebar.py",
        "intelligence/device_database.py",
        "intelligence/material_database.py",
        "intelligence/recovery_engine.py",
        "intelligence/economic_engine.py",
        "intelligence/environmental_engine.py",
        "ml/models/model_registry.py",
        "docs/PROJECT_ARCHITECTURE.md",
        "docs/TECHNOLOGY_STACK.md",
        "docs/DATABASE_DESIGN.md",
        "docs/RESEARCH_ARCHITECTURE.md",
        "docs/DEVELOPMENT_ROADMAP.md",
        "scripts/init_db.py",
        "scripts/check_env.py",
    ]

    def test_required_directories_exist(self):
        for d in self.REQUIRED_DIRS:
            assert os.path.isdir(d), f"Missing directory: {d}"

    def test_required_files_exist(self):
        for f in self.REQUIRED_FILES:
            assert os.path.isfile(f), f"Missing file: {f}"

    def test_docs_not_empty(self):
        for doc in ["docs/PROJECT_ARCHITECTURE.md", "docs/TECHNOLOGY_STACK.md",
                    "docs/DATABASE_DESIGN.md", "docs/DEVELOPMENT_ROADMAP.md"]:
            size = os.path.getsize(doc)
            assert size > 500, f"Doc file too small (possibly empty): {doc}"


class TestIntelligenceModule:
    """Verify intelligence module returns correct data structures."""

    def test_device_database_import(self):
        from intelligence.device_database import get_all_labels, get_device_info
        labels = get_all_labels()
        assert isinstance(labels, list)
        assert len(labels) >= 10
        assert "smartphone" in labels

    def test_device_info_structure(self):
        from intelligence.device_database import get_device_info
        info = get_device_info("smartphone")
        assert "avg_weight_kg" in info
        assert "hazard_level" in info

    def test_material_database_import(self):
        from intelligence.material_database import estimate_recovery_weights
        result = estimate_recovery_weights("smartphone", 0.14)
        assert result["is_estimate"] is True
        assert "gold_g" in result

    def test_economic_engine(self):
        from intelligence.economic_engine import calculate_recovery_value
        result = calculate_recovery_value({"gold": 0.004, "copper": 2.1})
        assert result["is_estimate"] is True
        assert result["total_gross_usd"] > 0

    def test_environmental_engine(self):
        from intelligence.environmental_engine import calculate_environmental_impact
        result = calculate_environmental_impact(10.0)
        assert result["is_estimate"] is True
        assert result["co2_saved_kg"] > 0

    def test_recovery_engine(self):
        from intelligence.recovery_engine import generate_recovery_assessment
        result = generate_recovery_assessment("smartphone", 0.14, "broken")
        assert result["is_estimate"] is True
        assert "material_estimates" in result
        assert "economic_estimate" in result
        assert "environmental_benefit" in result
        assert "disclaimer" in result


class TestMLRegistry:
    """Verify ML model registry is populated correctly."""

    def test_cnn_models_available(self):
        from ml.models.model_registry import get_cnn_architectures
        models = get_cnn_architectures()
        assert "mobilenetv3_small" in models
        assert "efficientnet_b0" in models
        assert "resnet18" in models

    def test_tabular_models_available(self):
        from ml.models.model_registry import get_tabular_algorithms
        models = get_tabular_algorithms()
        assert "random_forest" in models
        assert "xgboost" in models
        assert "catboost" in models


class TestConfig:
    """Verify backend configuration loads correctly."""

    def test_settings_import(self):
        from backend.config import settings
        assert settings.APP_NAME == "E-Waste AI"
        assert settings.DEFAULT_SEED == 42
        assert settings.TRAIN_SPLIT + settings.VAL_SPLIT + settings.TEST_SPLIT == pytest.approx(1.0)

    def test_database_url(self):
        from backend.config import settings
        assert "sqlite" in settings.DATABASE_URL.lower()
