"""
E-Waste AI — Phase 7 Database Integrity Tests
==============================================
Uses in-memory SQLite so tests are schema-authoritative regardless of
the local ewaste_ai.db version.
"""

import sys, os, time, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine, inspect as sa_inspect
from sqlalchemy.orm import sessionmaker

# ── In-memory engine fixture ──────────────────────────────────────────────

def _make_test_engine():
    """Fresh in-memory SQLite engine with all tables created."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    # Register all ORM models against this engine's metadata
    from backend.database import Base
    import backend.models  # noqa: triggers __init__.py which imports all_models
    Base.metadata.create_all(bind=engine)
    return engine

def _make_session(engine):
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    return Session()


# ── Task 3A: Schema Tests ─────────────────────────────────────────────────

class TestDatabaseSchema:
    """Verify all ORM models have correct table names and columns."""

    def test_all_models_importable(self):
        from backend.models.all_models import (
            WasteBatch, Device, RecoveryRecord, InventoryItem, MLModel,
            ModelEvaluation, AIPrediction, ResearchExperiment, Dataset,
            User, AuditLog, GeneratedReport
        )
        # Verify actual tablenames (discovered from code inspection)
        assert WasteBatch.__tablename__ == 'waste_batches'
        assert Device.__tablename__ == 'devices'
        assert RecoveryRecord.__tablename__ == 'recovery_records'
        assert InventoryItem.__tablename__ == 'inventory'    # actual name
        assert MLModel.__tablename__ == 'ml_models'

    def test_all_expected_tables_exist_in_memory(self):
        engine = _make_test_engine()
        tables = set(sa_inspect(engine).get_table_names())
        required = {'waste_batches', 'devices', 'recovery_records',
                    'inventory', 'ml_models', 'model_evaluations',
                    'ai_predictions', 'research_experiments', 'datasets'}
        missing = required - tables
        assert not missing, f"Missing tables: {missing}"

    def test_init_db_idempotent(self):
        from backend.database import init_db
        init_db()   # on real DB
        init_db()   # second call must not crash

    def test_waste_batch_columns(self):
        from backend.models.all_models import WasteBatch
        cols = {c.name for c in WasteBatch.__table__.columns}
        for f in ('id', 'batch_number', 'source', 'total_weight_kg',
                  'waste_category', 'status', 'created_at'):
            assert f in cols, f"WasteBatch missing column: {f}"

    def test_recovery_record_columns(self):
        from backend.models.all_models import RecoveryRecord
        cols = {c.name for c in RecoveryRecord.__table__.columns}
        for f in ('id', 'batch_id', 'material_name', 'recovered_quantity_g',
                  'value_source', 'recorded_at'):
            assert f in cols, f"RecoveryRecord missing column: {f}"

    def test_device_columns(self):
        from backend.models.all_models import Device
        cols = {c.name for c in Device.__table__.columns}
        for f in ('id', 'batch_id', 'device_type', 'manufacturer',
                  'weight_kg', 'condition'):
            assert f in cols, f"Device missing column: {f}"

    def test_inventory_item_columns(self):
        from backend.models.all_models import InventoryItem
        cols = {c.name for c in InventoryItem.__table__.columns}
        for f in ('id', 'material_name', 'quantity_g'):
            assert f in cols, f"InventoryItem missing column: {f}"


# ── Task 3B: CRUD Tests (in-memory DB) ───────────────────────────────────

class TestWasteBatchCRUD:
    def setup_method(self):
        self.engine = _make_test_engine()
        self.db = _make_session(self.engine)

    def teardown_method(self):
        self.db.close()
        self.engine.dispose()

    def test_create_read(self):
        from backend.models.all_models import WasteBatch
        b = WasteBatch(batch_number=f'DB-TEST-{int(time.time()*1000)}',
                       source='db_integrity_test', total_weight_kg=5.0,
                       waste_category='mixed', status='open')
        self.db.add(b); self.db.commit(); self.db.refresh(b)
        assert b.id is not None
        fetched = self.db.query(WasteBatch).filter_by(id=b.id).first()
        assert fetched.source == 'db_integrity_test'
        assert fetched.total_weight_kg == 5.0

    def test_update(self):
        from backend.models.all_models import WasteBatch
        b = WasteBatch(batch_number=f'DB-UPD-{int(time.time()*1000)}',
                       source='update_test', total_weight_kg=3.0,
                       waste_category='mixed', status='open')
        self.db.add(b); self.db.commit(); self.db.refresh(b)
        b.status = 'processing'
        b.total_weight_kg = 4.5
        self.db.commit()
        fetched = self.db.query(WasteBatch).filter_by(id=b.id).first()
        assert fetched.status == 'processing'
        assert fetched.total_weight_kg == 4.5

    def test_delete(self):
        from backend.models.all_models import WasteBatch
        b = WasteBatch(batch_number=f'DB-DEL-{int(time.time()*1000)}',
                       source='delete_test', total_weight_kg=1.0,
                       waste_category='mixed', status='open')
        self.db.add(b); self.db.commit(); self.db.refresh(b)
        bid = b.id
        self.db.delete(b); self.db.commit()
        assert self.db.query(WasteBatch).filter_by(id=bid).first() is None


class TestRecoveryDataSeparation:
    """Ensure measured vs estimated values are stored with provenance."""

    def setup_method(self):
        self.engine = _make_test_engine()
        self.db = _make_session(self.engine)

    def teardown_method(self):
        self.db.close()
        self.engine.dispose()

    def test_value_source_column_exists(self):
        from backend.models.all_models import RecoveryRecord
        cols = [c.name for c in RecoveryRecord.__table__.columns]
        assert 'value_source' in cols

    def test_estimate_and_measured_stored_separately(self):
        from backend.models.all_models import WasteBatch, RecoveryRecord
        b = WasteBatch(batch_number=f'SEP-{int(time.time()*1000)}',
                       source='separation_test', total_weight_kg=5.0,
                       waste_category='mixed', status='open')
        self.db.add(b); self.db.commit(); self.db.refresh(b)
        est  = RecoveryRecord(batch_id=b.id, material_name='copper',
                              recovered_quantity_g=200.0, value_source='estimate')
        meas = RecoveryRecord(batch_id=b.id, material_name='copper',
                              recovered_quantity_g=185.0, value_source='measured')
        self.db.add_all([est, meas]); self.db.commit()
        recs = self.db.query(RecoveryRecord).filter_by(batch_id=b.id).all()
        sources = {r.value_source for r in recs}
        assert 'estimate' in sources
        assert 'measured' in sources

    def test_estimate_and_measured_values_differ(self):
        from backend.models.all_models import WasteBatch, RecoveryRecord
        b = WasteBatch(batch_number=f'DIFF-{int(time.time()*1000)}',
                       source='diff_test', total_weight_kg=2.0,
                       waste_category='mixed', status='open')
        self.db.add(b); self.db.commit(); self.db.refresh(b)
        est  = RecoveryRecord(batch_id=b.id, material_name='aluminium',
                              recovered_quantity_g=300.0, value_source='estimate')
        meas = RecoveryRecord(batch_id=b.id, material_name='aluminium',
                              recovered_quantity_g=270.0, value_source='measured')
        self.db.add_all([est, meas]); self.db.commit()
        recs = self.db.query(RecoveryRecord).filter_by(batch_id=b.id).all()
        est_val  = next(r.recovered_quantity_g for r in recs if r.value_source == 'estimate')
        meas_val = next(r.recovered_quantity_g for r in recs if r.value_source == 'measured')
        # Both stored independently — values can differ
        assert est_val == 300.0
        assert meas_val == 270.0


class TestForeignKeyRelationships:
    def setup_method(self):
        self.engine = _make_test_engine()
        self.db = _make_session(self.engine)

    def teardown_method(self):
        self.db.close()
        self.engine.dispose()

    def test_device_references_batch(self):
        from backend.models.all_models import WasteBatch, Device
        b = WasteBatch(batch_number=f'FK-{int(time.time()*1000)}',
                       source='fk_test', total_weight_kg=2.0,
                       waste_category='mixed', status='open')
        self.db.add(b); self.db.commit(); self.db.refresh(b)
        d = Device(batch_id=b.id, device_type='laptop', manufacturer='FK-Test',
                   weight_kg=1.0, condition='good')
        self.db.add(d); self.db.commit(); self.db.refresh(d)
        assert d.batch_id == b.id

    def test_recovery_references_batch(self):
        from backend.models.all_models import WasteBatch, RecoveryRecord
        b = WasteBatch(batch_number=f'RR-FK-{int(time.time()*1000)}',
                       source='rr_fk_test', total_weight_kg=3.0,
                       waste_category='mixed', status='open')
        self.db.add(b); self.db.commit(); self.db.refresh(b)
        r = RecoveryRecord(batch_id=b.id, material_name='copper',
                           recovered_quantity_g=100.0, value_source='estimate')
        self.db.add(r); self.db.commit(); self.db.refresh(r)
        assert r.batch_id == b.id

    def test_multiple_devices_per_batch(self):
        from backend.models.all_models import WasteBatch, Device
        b = WasteBatch(batch_number=f'MULTI-{int(time.time()*1000)}',
                       source='multi_device', total_weight_kg=10.0,
                       waste_category='mixed', status='open')
        self.db.add(b); self.db.commit(); self.db.refresh(b)
        devices = [
            Device(batch_id=b.id, device_type='laptop', manufacturer='A',
                   weight_kg=2.0, condition='good'),
            Device(batch_id=b.id, device_type='mobile_phone', manufacturer='B',
                   weight_kg=0.2, condition='poor'),
            Device(batch_id=b.id, device_type='desktop', manufacturer='C',
                   weight_kg=7.0, condition='fair'),
        ]
        self.db.add_all(devices); self.db.commit()
        count = self.db.query(Device).filter_by(batch_id=b.id).count()
        assert count == 3


class TestResearchExperimentCRUD:
    def setup_method(self):
        self.engine = _make_test_engine()
        self.db = _make_session(self.engine)

    def teardown_method(self):
        self.db.close()
        self.engine.dispose()

    def test_create_experiment(self):
        from backend.models.all_models import ResearchExperiment
        exp = ResearchExperiment(
            experiment_name=f'Phase7-Test-{int(time.time()*1000)}',
            model_architecture='random_forest',
            status='planned',
            notes='Phase 7 DB integrity test'
        )
        self.db.add(exp); self.db.commit(); self.db.refresh(exp)
        assert exp.id is not None
        fetched = self.db.query(ResearchExperiment).filter_by(id=exp.id).first()
        assert fetched.model_architecture == 'random_forest'


class TestConstraintsAndRollback:
    """Verify unique constraints and transaction rollback."""

    def setup_method(self):
        self.engine = _make_test_engine()
        self.db = _make_session(self.engine)

    def teardown_method(self):
        self.db.close()
        self.engine.dispose()

    def test_duplicate_batch_number_rejected(self):
        from sqlalchemy.exc import IntegrityError
        from backend.models.all_models import WasteBatch
        b1 = WasteBatch(batch_number='UNIQUE-BATCH-001', source='test', total_weight_kg=1.0, status='open')
        b2 = WasteBatch(batch_number='UNIQUE-BATCH-001', source='test', total_weight_kg=2.0, status='open')
        self.db.add(b1); self.db.commit()
        self.db.add(b2)
        with pytest.raises(IntegrityError):
            self.db.commit()
        self.db.rollback()

    def test_transaction_rollback_preserves_state(self):
        from backend.models.all_models import WasteBatch
        b1 = WasteBatch(batch_number='ROLLBACK-TEST-001', source='test', total_weight_kg=2.0, status='open')
        self.db.add(b1); self.db.commit()
        b2 = WasteBatch(batch_number='ROLLBACK-TEST-002', source='test', total_weight_kg=3.0, status='open')
        self.db.add(b2)
        self.db.rollback()
        assert self.db.query(WasteBatch).filter_by(batch_number='ROLLBACK-TEST-001').first() is not None
        assert self.db.query(WasteBatch).filter_by(batch_number='ROLLBACK-TEST-002').first() is None
