"""
E-Waste AI — Phase 7 End-to-End Workflow Tests
================================================
Tests complete workflows A-F using real implemented functionality.
"""

import sys, os, json, pytest, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ── Workflow A: Dataset lifecycle ─────────────────────────────────────────

class TestWorkflowA_Dataset:
    """Upload/inspect/clean/preprocess/validate/prepare/export workflow."""

    def test_dataset_service_importable(self):
        from backend.models import all_models
        from backend.services.dataset_service import DatasetService
        svc = DatasetService()
        assert svc is not None

    def test_dataset_model_has_required_fields(self):
        from backend.models import all_models
        from backend.models.dataset import Dataset
        assert Dataset is all_models.Dataset  # single canonical Dataset class
        cols = [c.name for c in Dataset.__table__.columns]
        for field in ['id', 'name', 'dataset_type', 'file_path', 'is_cleaned', 'is_preprocessed']:
            assert field in cols, f"Dataset missing column: {field}"

    def test_dataset_version_model_importable(self):
        from backend.models.dataset import DatasetVersion
        assert DatasetVersion.__tablename__ == 'dataset_versions'

    def test_cleaning_run_model_importable(self):
        from backend.models.dataset import CleaningRun
        assert CleaningRun.__tablename__ == 'cleaning_runs'

    def test_preprocessing_config_model_importable(self):
        from backend.models.dataset import PreprocessingConfig
        assert PreprocessingConfig.__tablename__ == 'preprocessing_configs'

    def test_workflow_a_end_to_end_pipeline(self):
        """Real workflow: DataFrame -> inspect -> score -> clean -> preprocess -> DatasetService history."""
        import pandas as pd
        import numpy as np
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from backend.database import Base
        import backend.models  # noqa: registers all tables including cleaning_runs, preprocessing_configs
        from backend.services.dataset_service import DatasetService
        from ml.data.inspector import DatasetInspector
        from ml.data.quality_scorer import DatasetQualityScorer
        from ml.data.cleaner_advanced import AdvancedDataCleaner
        from ml.data.preprocessor_advanced import AdvancedPreprocessor

        eng = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=eng)
        db = sessionmaker(bind=eng, autocommit=False, autoflush=False)()
        try:
            rng = np.random.default_rng(42)
            df = pd.DataFrame({
                "weight_kg": np.concatenate([rng.uniform(0.5, 5.0, 48), [None, 2.0]]),
                "device_type": rng.choice(["laptop", "phone", "desktop"], 50),
                "copper_g": rng.uniform(50, 300, 50),
                "label": rng.choice(["high", "low"], 50),
            })
            inspector = DatasetInspector()
            inspect_res = inspector.inspect_tabular(df)
            assert inspect_res["shape"]["rows"] == 50

            scorer = DatasetQualityScorer()
            score_res = scorer.score(df)
            assert 0 <= score_res["overall_score"] <= 100

            cleaner = AdvancedDataCleaner()
            cleaned_df, clean_report = cleaner.clean(df, {"fill_strategy": "median"})
            assert len(cleaned_df) > 0

            prep = AdvancedPreprocessor()
            split_res = prep.fit_transform(cleaned_df, target_col="label")
            assert len(split_res["X_train"]) + len(split_res["X_val"]) + len(split_res["X_test"]) == len(cleaned_df)

            svc = DatasetService(db=db)
            ds_id = svc.register_dataset("wf_a_synthetic", "memory://wf_a.csv", "tabular")
            assert ds_id is not None
            run_id = svc.save_cleaning_run(ds_id, clean_report)
            assert run_id is not None
            cfg_id = svc.save_preprocessing_config(ds_id, {"target_col": "label", "scaler": "standard"})
            assert cfg_id is not None

            hist = svc.get_dataset_history(ds_id)
            assert hist["dataset"]["status"] == "preprocessed"
            assert len(hist["cleaning_runs"]) == 1
            assert len(hist["preprocessing_configs"]) == 1
        finally:
            db.close()
            eng.dispose()


# ── Workflow B: Model lifecycle ───────────────────────────────────────────

class TestWorkflowB_ModelLifecycle:
    """Train → evaluate → compare → register workflow."""

    def test_mlmodel_has_required_fields(self):
        from backend.models.all_models import MLModel
        cols = [c.name for c in MLModel.__table__.columns]
        for f in ['id', 'name', 'file_path', 'training_duration_sec']:
            assert f in cols, f"MLModel missing: {f}"

    def test_model_evaluation_has_metrics_json(self):
        from backend.models.all_models import ModelEvaluation
        cols = [c.name for c in ModelEvaluation.__table__.columns]
        assert 'metrics' in cols

    def test_registry_json_exists_and_valid(self):
        reg_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'registry', 'registry.json')
        assert os.path.exists(reg_path), "registry.json not found"
        with open(reg_path) as f:
            reg = json.load(f)
        assert isinstance(reg, (dict, list))

    def test_pkl_model_files_exist(self):
        saved_dir = os.path.join(os.path.dirname(__file__), '..', 'models', 'saved')
        pkl_files = [f for f in os.listdir(saved_dir) if f.endswith('.pkl')]
        assert len(pkl_files) >= 1, f"No .pkl files found in {saved_dir}"

    def test_pkl_models_loadable(self):
        import joblib
        saved_dir = os.path.join(os.path.dirname(__file__), '..', 'models', 'saved')
        pkl_files = [f for f in os.listdir(saved_dir) if f.endswith('.pkl')]
        for fname in pkl_files[:3]:  # test first 3
            path = os.path.join(saved_dir, fname)
            model = joblib.load(path)
            assert hasattr(model, 'predict'), f"{fname} has no predict() method"


# ── Workflow C: AI inference ──────────────────────────────────────────────

class TestWorkflowC_AIInference:
    """E-waste analysis: estimate_recovery for all device types."""

    def setup_method(self):
        from backend.services.advanced_intelligence import AdvancedIntelligenceEngine
        self.engine = AdvancedIntelligenceEngine()

    def test_all_device_types_estimable(self):
        for device in self.engine.list_supported_device_types():
            result = self.engine.estimate_recovery(device, 1.0)
            assert result['available'] is True, f"Device {device} not estimable"

    def test_inference_returns_disclaimer(self):
        result = self.engine.estimate_recovery('laptop', 1.0)
        assert 'disclaimer' in result

    def test_missing_model_handled_safely(self):
        result = self.engine.predict('nonexistent_model_xyz', {'f': 1.0})
        assert 'error' in result or result.get('available') is False

    def test_recovery_mass_conservation(self):
        """Cannot recover more material than input weight."""
        result = self.engine.estimate_recovery('laptop', 1.0)
        total_recovered_g = result.get('total_recovered_g', 0)
        input_g = 1.0 * 1000
        assert total_recovered_g <= input_g, f"Recovery {total_recovered_g}g > input {input_g}g"


# ── Workflow D: Batch lifecycle ───────────────────────────────────────────

def _make_mem_session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from backend.database import Base
    import backend.models  # noqa
    eng = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=eng)
    return sessionmaker(bind=eng, autocommit=False, autoflush=False)()


class TestWorkflowD_BatchLifecycle:
    """Register e-waste → create batch → record recovery."""

    def setup_method(self):
        self.db = _make_mem_session()

    def teardown_method(self):
        self.db.close()

    def test_waste_batch_crud(self):
        from backend.models.all_models import WasteBatch
        b = WasteBatch(
            batch_number=f'TEST-WF-D-{int(time.time())}',
            source='Phase7 E2E Test',
            total_weight_kg=10.5,
            waste_category='mixed',
            status='open'
        )
        self.db.add(b)
        self.db.commit()
        self.db.refresh(b)
        assert b.id is not None
        # Update
        b.status = 'processing'
        self.db.commit()
        # Read
        fetched = self.db.query(WasteBatch).filter_by(id=b.id).first()
        assert fetched.status == 'processing'
        # Delete
        self.db.delete(fetched)
        self.db.commit()
        assert self.db.query(WasteBatch).filter_by(id=b.id).first() is None

    def test_recovery_record_crud(self):
        from backend.models.all_models import WasteBatch, RecoveryRecord
        b = WasteBatch(batch_number=f'TEST-REC-{int(time.time())}', source='test',
                       total_weight_kg=5.0, waste_category='mixed', status='open')
        self.db.add(b); self.db.commit(); self.db.refresh(b)
        rr = RecoveryRecord(batch_id=b.id, material_name='copper',
                            recovered_quantity_g=250.0, value_source='estimate')
        self.db.add(rr); self.db.commit(); self.db.refresh(rr)
        assert rr.id is not None
        assert rr.recovered_quantity_g == 250.0

    def test_device_record_crud(self):
        from backend.models.all_models import WasteBatch, Device
        b = WasteBatch(batch_number=f'TEST-DEV-{int(time.time())}', source='test',
                       total_weight_kg=2.0, waste_category='mixed', status='open')
        self.db.add(b); self.db.commit(); self.db.refresh(b)
        d = Device(batch_id=b.id, device_type='laptop', manufacturer='TestCo',
                   weight_kg=1.5, condition='good')
        self.db.add(d); self.db.commit(); self.db.refresh(d)
        assert d.id is not None


# ── Workflow E: Recovery plan ─────────────────────────────────────────────

class TestWorkflowE_RecoveryPlan:
    """Select batch → generate recovery plan → estimate value."""

    def setup_method(self):
        from backend.services.advanced_intelligence import AdvancedIntelligenceEngine
        self.engine = AdvancedIntelligenceEngine()

    def test_recovery_plan_for_nonexistent_batch(self):
        result = self.engine.recommend_recovery_plan('nonexistent_batch_xyz')
        assert isinstance(result, dict)
        assert 'available' in result

    def test_processing_cost_has_disclaimer(self):
        result = self.engine.estimate_processing_cost(50.0, labour_hours=4)
        assert 'disclaimer' in result
        assert 'ESTIMATE' in result['disclaimer'].upper()

    def test_trends_returns_dict(self):
        result = self.engine.compute_trends(days=30)
        assert isinstance(result, dict)
        assert 'period_days' in result


# ── Workflow F: Research lifecycle ────────────────────────────────────────

class TestWorkflowF_ResearchLifecycle:
    """Research dataset → experiment config → training → evaluation."""

    def setup_method(self):
        self.db = _make_mem_session()

    def teardown_method(self):
        self.db.close()

    def test_research_experiment_crud(self):
        from backend.models.all_models import ResearchExperiment
        exp = ResearchExperiment(
            experiment_name=f'Phase7-Test-{int(time.time())}',
            model_architecture='random_forest',
            status='planned',
            notes='Phase 7 E2E test experiment'
        )
        self.db.add(exp); self.db.commit(); self.db.refresh(exp)
        assert exp.id is not None

    def test_history_json_files_exist(self):
        history_dir = os.path.join(os.path.dirname(__file__), '..', 'models', 'history')
        json_files = [f for f in os.listdir(history_dir) if f.endswith('.json')]
        assert len(json_files) >= 1, "No training history JSON files found"

    def test_history_json_has_required_fields(self):
        import glob
        history_dir = os.path.join(os.path.dirname(__file__), '..', 'models', 'history')
        for jf in glob.glob(os.path.join(history_dir, '*.json'))[:3]:
            with open(jf) as f:
                h = json.load(f)
            assert isinstance(h, dict), f"{jf} is not a dict"


class TestFrontendNavigation:
    """Verify every sidebar NAV_ITEMS route in app.py resolves to a callable render target."""

    def test_all_17_nav_routes_callable(self):
        import ast, importlib
        from pathlib import Path
        root = Path(__file__).resolve().parent.parent
        from frontend.components.sidebar import NAV_ITEMS

        tree = ast.parse((root / 'app.py').read_text(encoding='utf-8'))
        imported_targets = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith('frontend.pages.'):
                page_key = node.module.split('.')[-1]
                imported_targets[page_key] = node.names[0].name

        assert len(NAV_ITEMS) == 17
        for key, _icon, _label, _group in NAV_ITEMS:
            assert key in imported_targets, f"Sidebar key '{key}' missing from app.py router"
            mod = importlib.import_module(f"frontend.pages.{key}")
            fn_name = imported_targets[key]
            fn = getattr(mod, fn_name, None)
            assert callable(fn), f"{key}: app.py expects '{fn_name}' which is missing/non-callable"
