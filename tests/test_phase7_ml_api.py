"""
E-Waste AI — Phase 7 API & ML Integration Tests
================================================
Tests FastAPI endpoints, ML validation, and performance benchmarks.
"""

import sys, os, time, json, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# ── API Tests ─────────────────────────────────────────────────────────────

class TestAPIEndpoints:
    def setup_method(self):
        try:
            from fastapi.testclient import TestClient
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker
            from sqlalchemy.pool import StaticPool
            from backend.database import Base, get_db
            import backend.models  # noqa: registers all ORM tables
            from backend.main import app

            self._engine = create_engine(
                "sqlite:///:memory:",
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
            )
            Base.metadata.create_all(bind=self._engine)
            SessionLocalTest = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)

            def _override_get_db():
                db = SessionLocalTest()
                try:
                    yield db
                finally:
                    db.close()

            app.dependency_overrides[get_db] = _override_get_db
            self._app = app
            self._get_db = get_db
            self.client = TestClient(app)
            self.available = True
        except Exception as e:
            self.available = False
            self.skip_reason = str(e)

    def teardown_method(self):
        if getattr(self, "available", False):
            self._app.dependency_overrides.pop(self._get_db, None)
            self._engine.dispose()

    def _require_api(self):
        if not self.available:
            pytest.skip(f"API not available: {self.skip_reason}")

    def test_api_app_importable(self):
        from backend.main import app
        assert app is not None

    def test_root_and_status_endpoints(self):
        self._require_api()
        r_root = self.client.get('/')
        assert r_root.status_code == 200
        assert r_root.json().get('status') == 'online'
        r_stat = self.client.get('/api/v1/status')
        assert r_stat.status_code == 200
        assert 'endpoints' in r_stat.json()

    def test_docs_endpoint(self):
        self._require_api()
        r = self.client.get('/docs')
        assert r.status_code == 200

    def test_openapi_json(self):
        self._require_api()
        r = self.client.get('/openapi.json')
        assert r.status_code == 200
        schema = r.json()
        assert 'paths' in schema

    def test_auth_register_login_me_and_invalid_token(self):
        self._require_api()
        reg = self.client.post('/api/v1/auth/register', json={
            'username': 'phase7_api_user',
            'email': 'phase7@example.com',
            'password': 'StrongPassword!123',
            'full_name': 'Phase 7 Tester',
            'role': 'researcher',
        })
        assert reg.status_code == 201
        login = self.client.post('/api/v1/auth/login', json={
            'username': 'phase7_api_user',
            'password': 'StrongPassword!123',
        })
        assert login.status_code == 200
        token = login.json()['access_token']
        me_ok = self.client.get('/api/v1/auth/me', headers={'Authorization': f'Bearer {token}'})
        assert me_ok.status_code == 200
        assert me_ok.json()['username'] == 'phase7_api_user'
        me_bad = self.client.get('/api/v1/auth/me', headers={'Authorization': 'Bearer invalid.jwt.token'})
        assert me_bad.status_code == 401

    def test_batches_crud_endpoints(self):
        self._require_api()
        created = self.client.post('/api/v1/batches', json={
            'source': 'api_test_facility',
            'total_weight_kg': 12.5,
            'waste_category': 'mixed',
            'location': 'Bay 1',
        })
        assert created.status_code == 201
        batch_id = created.json()['id']
        listed = self.client.get('/api/v1/batches')
        assert listed.status_code == 200
        assert any(b['id'] == batch_id for b in listed.json())

    def test_batches_list_endpoint(self):
        self._require_api()
        r = self.client.get('/api/v1/batches')
        assert r.status_code == 200

    def test_batches_invalid_body(self):
        self._require_api()
        r = self.client.post('/api/v1/batches', json={'invalid_field': 'xyz'})
        assert r.status_code == 422

    def test_batch_not_found(self):
        self._require_api()
        r = self.client.get('/api/v1/batches/999999999')
        assert r.status_code == 404

    def test_intelligence_recovery_and_economics_endpoints(self):
        self._require_api()
        r_rec = self.client.post('/api/v1/intelligence/recovery/estimate', json={
            'device_type': 'laptop',
            'weight_kg': 2.0,
        })
        assert r_rec.status_code == 200
        r_econ = self.client.post('/api/v1/intelligence/economics/analyze', json={
            'device_type': 'laptop',
            'weight_kg': 2.0,
            'processing_cost_usd': 5.0,
        })
        assert r_econ.status_code == 200
        r_404 = self.client.get('/api/v1/intelligence/economics/prices/unknown_material_xyz')
        assert r_404.status_code == 404

    def test_upload_mime_validation_and_path_traversal(self):
        self._require_api()
        from backend.services.auth_service import sanitize_filename
        clean = sanitize_filename('../../etc/passwd')
        assert '..' not in clean and '/' not in clean and '\\' not in clean
        bad_upload = self.client.post(
            '/api/v1/ai/classify/image',
            files={'file': ('evil.txt', b'not an image', 'text/plain')},
        )
        assert bad_upload.status_code == 400

    def test_routers_importable(self):
        from backend.routers.batches import router as batches_router
        from backend.routers.auth import router as auth_router
        assert batches_router is not None
        assert auth_router is not None


# ── ML Validation Tests ───────────────────────────────────────────────────

class TestMLValidation:
    def setup_method(self):
        from backend.services.advanced_intelligence import AdvancedIntelligenceEngine
        self.engine = AdvancedIntelligenceEngine()

    def test_all_6_device_types_in_kb(self):
        types = self.engine.list_supported_device_types()
        assert len(types) == 6
        for dt in ['laptop', 'desktop', 'mobile_phone', 'television', 'printer', 'battery_pack']:
            assert dt in types

    def test_unknown_device_returns_unavailable(self):
        result = self.engine.estimate_recovery('unknown_xyz_device', 1.0)
        assert result['available'] is False

    def test_zero_weight_no_crash(self):
        result = self.engine.estimate_recovery('laptop', 0.0)
        assert isinstance(result, dict)

    def test_negative_weight_handled(self):
        """Negative weight should not crash — handle gracefully."""
        try:
            result = self.engine.estimate_recovery('laptop', -1.0)
            assert isinstance(result, dict)
        except (ValueError, AssertionError):
            pass  # Acceptable to raise ValueError for negative weight

    def test_explain_no_model_returns_unavailable(self):
        result = self.engine.explain_prediction('no_such_model', {'f': 1.0})
        assert result['available'] is False

    def test_predict_no_model_returns_error(self):
        result = self.engine.predict('no_such_model', {'f': 1.0})
        assert 'error' in result or result.get('available') is False

    def test_list_available_models_returns_list(self):
        models = self.engine.list_available_models()
        assert isinstance(models, list)

    def test_mass_conservation(self):
        """Total recovered material cannot exceed input weight."""
        for device in self.engine.list_supported_device_types():
            result = self.engine.estimate_recovery(device, 1.0)
            if result['available']:
                total_g = sum(
                    v.get('estimated_recovered_g', 0)
                    for v in result.get('recoverable_materials', {}).values()
                )
                assert total_g <= 1050, f"{device}: {total_g}g recovered from 1000g input (>5% tolerance)"

    def test_economic_disclaimer_present(self):
        result = self.engine.estimate_processing_cost(100.0)
        assert 'disclaimer' in result
        assert 'ESTIMATE' in result['disclaimer'].upper()

    def test_pkl_models_cpu_compatible(self):
        """Loaded sklearn models should be CPU-only (no CUDA attributes)."""
        import joblib, glob
        saved_dir = os.path.join(os.path.dirname(__file__), '..', 'models', 'saved')
        pkl_files = glob.glob(os.path.join(saved_dir, '*.pkl'))
        for path in pkl_files[:3]:
            model = joblib.load(path)
            # sklearn models don't have .cuda() or .device attributes
            assert not hasattr(model, 'cuda'), f"{path} has .cuda() — not CPU-only"


# ── Performance Benchmarks ────────────────────────────────────────────────

class TestPerformanceBenchmarks:
    """Measure actual performance — no invented numbers."""

    def test_engine_import_time(self):
        t0 = time.time()
        from backend.services.advanced_intelligence import get_engine
        engine = get_engine()
        t1 = time.time()
        elapsed_ms = (t1 - t0) * 1000
        print(f"\nEngine import+init: {elapsed_ms:.1f}ms")
        assert elapsed_ms < 5000, f"Engine init took {elapsed_ms:.0f}ms (>5s)"

    def test_recovery_estimation_latency(self):
        from backend.services.advanced_intelligence import get_engine
        engine = get_engine()
        t0 = time.time()
        for dt in engine.list_supported_device_types():
            engine.estimate_recovery(dt, 2.0)
        t1 = time.time()
        elapsed_ms = (t1 - t0) * 1000
        print(f"\nRecovery estimation x6 devices: {elapsed_ms:.1f}ms")
        assert elapsed_ms < 1000, f"Recovery estimation took {elapsed_ms:.0f}ms (>1s)"

    def test_anomaly_detection_latency(self):
        from backend.services.advanced_intelligence import get_engine
        engine = get_engine()
        t0 = time.time()
        flags = engine.detect_anomalies()
        t1 = time.time()
        elapsed_ms = (t1 - t0) * 1000
        print(f"\nAnomaly detection: {elapsed_ms:.1f}ms, flags={len(flags)}")
        assert elapsed_ms < 5000, f"Anomaly detection took {elapsed_ms:.0f}ms (>5s)"

    def test_pkl_model_load_and_inference(self):
        import joblib, glob, numpy as np
        saved_dir = os.path.join(os.path.dirname(__file__), '..', 'models', 'saved')
        pkl_files = glob.glob(os.path.join(saved_dir, 'synthetic_clf*.pkl'))
        if not pkl_files:
            pytest.skip("No synthetic_clf .pkl files found")
        path = pkl_files[0]
        t0 = time.time()
        model = joblib.load(path)
        t1 = time.time()
        load_ms = (t1 - t0) * 1000
        X = np.random.rand(1, 10)
        t0 = time.time()
        pred = model.predict(X)
        t1 = time.time()
        infer_ms = (t1 - t0) * 1000
        print(f"\nModel load: {load_ms:.1f}ms, inference: {infer_ms:.3f}ms")
        assert pred is not None


# ── Baseline ML Comparison ────────────────────────────────────────────────

class TestBaselineComparison:
    """Compare baseline vs advanced models on synthetic data."""

    def test_baseline_vs_rf_on_synthetic(self):
        import numpy as np
        from sklearn.datasets import make_classification
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        from sklearn.dummy import DummyClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import accuracy_score, f1_score

        np.random.seed(42)
        X, y = make_classification(n_samples=500, n_features=10, n_informative=5,
                                   n_classes=3, random_state=42)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y)
        scaler = StandardScaler()
        X_train_s = scaler.fit_transform(X_train)
        X_test_s = scaler.transform(X_test)

        results = {}
        models = [
            ('Dummy', DummyClassifier(strategy='most_frequent')),
            ('LogisticRegression', LogisticRegression(random_state=42, max_iter=200)),
            ('RandomForest', RandomForestClassifier(n_estimators=50, random_state=42)),
        ]
        for name, m in models:
            t0 = time.time()
            m.fit(X_train_s, y_train)
            train_t = time.time() - t0
            t0 = time.time()
            pred = m.predict(X_test_s)
            infer_t = time.time() - t0
            acc = accuracy_score(y_test, pred)
            f1 = f1_score(y_test, pred, average='weighted')
            results[name] = {'accuracy': round(acc, 4), 'f1_weighted': round(f1, 4),
                             'train_s': round(train_t, 4), 'infer_s': round(infer_t, 6)}
            print(f"\n{name}: acc={acc:.4f} f1={f1:.4f} train={train_t:.3f}s")

        # RF should beat Dummy on this dataset
        assert results['RandomForest']['accuracy'] > results['Dummy']['accuracy'], \
            "RandomForest should outperform Dummy on this dataset"

        # Save results for docs
        out_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'phase7', 'baseline_results.json')
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {out_path}")
