"""
E-Waste AI — Complete ORM Models (Phase 4)
==========================================
All database tables for industrial operations, AI/ML, and research.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from backend.database import Base


def _uuid():
    return str(uuid.uuid4())


def _now():
    return datetime.utcnow()


# ══════════════════════════════════════════════════════════════════════════════
# USERS & AUTH
# ══════════════════════════════════════════════════════════════════════════════

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=_uuid)
    username = Column(String(64), unique=True, nullable=False, index=True)
    email = Column(String(256), unique=True, nullable=False, index=True)
    hashed_password = Column(String(256), nullable=False)
    full_name = Column(String(256))
    role = Column(String(32), default="operator")          # admin / manager / operator / researcher
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=_now)
    last_login = Column(DateTime)

    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    action = Column(String(128), nullable=False)
    resource = Column(String(128))
    resource_id = Column(String)
    details = Column(JSON)
    ip_address = Column(String(64))
    created_at = Column(DateTime, default=_now, index=True)

    user = relationship("User", back_populates="audit_logs")


# ══════════════════════════════════════════════════════════════════════════════
# DATASETS
# ══════════════════════════════════════════════════════════════════════════════

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String, primary_key=True, default=_uuid)
    name = Column(String(256), nullable=False)
    version = Column(String(32), default="1.0.0")
    description = Column(Text)
    source = Column(String(256))
    dataset_type = Column(String(64))          # tabular / image / mixed
    file_path = Column(String(512))
    file_size_bytes = Column(Integer)
    row_count = Column(Integer)
    column_count = Column(Integer)
    column_names = Column(JSON)
    target_columns = Column(JSON)
    quality_score = Column(Float)
    checksum = Column(String(128))
    is_cleaned = Column(Boolean, default=False)
    is_preprocessed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=_now, index=True)
    updated_at = Column(DateTime, default=_now, onupdate=_now)

    models = relationship("MLModel", back_populates="dataset")
    experiments = relationship("ResearchExperiment", back_populates="dataset")


# ══════════════════════════════════════════════════════════════════════════════
# ML MODELS
# ══════════════════════════════════════════════════════════════════════════════

class MLModel(Base):
    __tablename__ = "ml_models"

    id = Column(String, primary_key=True, default=_uuid)
    name = Column(String(256), nullable=False)
    model_type = Column(String(64))            # classifier / regressor / cnn
    algorithm = Column(String(128))
    dataset_id = Column(String, ForeignKey("datasets.id"), nullable=True)
    dataset_version = Column(String(32))
    feature_columns = Column(JSON)
    target_column = Column(String(128))
    task_type = Column(String(64))             # classification / regression
    hyperparameters = Column(JSON)
    training_config = Column(JSON)
    random_seed = Column(Integer)
    version = Column(String(32), default="1.0.0")
    status = Column(String(32), default="trained")  # trained / active / archived / failed
    file_path = Column(String(512))
    file_size_bytes = Column(Integer)
    training_duration_sec = Column(Float)
    created_at = Column(DateTime, default=_now, index=True)
    trained_at = Column(DateTime)

    dataset = relationship("Dataset", back_populates="models")
    evaluations = relationship("ModelEvaluation", back_populates="model", cascade="all, delete-orphan")
    predictions = relationship("AIPrediction", back_populates="model")

    __table_args__ = (Index("ix_ml_models_status", "status"),)


class ModelEvaluation(Base):
    __tablename__ = "model_evaluations"

    id = Column(String, primary_key=True, default=_uuid)
    model_id = Column(String, ForeignKey("ml_models.id"), nullable=False)
    split = Column(String(16))                 # train / val / test
    metrics = Column(JSON)                     # accuracy, f1, mae, r2, etc.
    confusion_matrix = Column(JSON)
    class_report = Column(JSON)
    roc_auc = Column(Float)
    pr_auc = Column(Float)
    evaluated_at = Column(DateTime, default=_now)

    model = relationship("MLModel", back_populates="evaluations")


# ══════════════════════════════════════════════════════════════════════════════
# E-WASTE BATCHES & DEVICES
# ══════════════════════════════════════════════════════════════════════════════

class WasteBatch(Base):
    __tablename__ = "waste_batches"

    id = Column(String, primary_key=True, default=_uuid)
    batch_number = Column(String(64), unique=True, nullable=False, index=True)
    source = Column(String(256))               # company / individual / municipality
    received_date = Column(DateTime, default=_now)
    total_weight_kg = Column(Float)
    waste_category = Column(String(128))       # WEEE category
    status = Column(String(32), default="received")
    # received / sorted / dismantled / processed / completed
    location = Column(String(256))
    notes = Column(Text)
    created_at = Column(DateTime, default=_now, index=True)
    updated_at = Column(DateTime, default=_now, onupdate=_now)

    devices = relationship("Device", back_populates="batch", cascade="all, delete-orphan")
    operations = relationship("ProcessingOperation", back_populates="batch", cascade="all, delete-orphan")
    recovery_records = relationship("RecoveryRecord", back_populates="batch", cascade="all, delete-orphan")
    cost_records = relationship("OperationalCost", back_populates="batch", cascade="all, delete-orphan")

    __table_args__ = (Index("ix_waste_batches_status", "status"),)


class Device(Base):
    __tablename__ = "devices"

    id = Column(String, primary_key=True, default=_uuid)
    batch_id = Column(String, ForeignKey("waste_batches.id"), nullable=False)
    device_type = Column(String(128))          # laptop, phone, monitor, etc.
    manufacturer = Column(String(128))
    model_name = Column(String(256))
    year_manufactured = Column(Integer)
    weight_kg = Column(Float)
    condition = Column(String(32))             # working / damaged / non-functional
    image_path = Column(String(512))
    ai_predicted_category = Column(String(128))
    ai_confidence = Column(Float)
    ai_model_id = Column(String, ForeignKey("ml_models.id"), nullable=True)
    created_at = Column(DateTime, default=_now)

    batch = relationship("WasteBatch", back_populates="devices")
    components = relationship("Component", back_populates="device", cascade="all, delete-orphan")


class Component(Base):
    __tablename__ = "components"

    id = Column(String, primary_key=True, default=_uuid)
    device_id = Column(String, ForeignKey("devices.id"), nullable=False)
    component_type = Column(String(128))       # PCB, battery, screen, etc.
    material_type = Column(String(128))
    weight_kg = Column(Float)
    condition = Column(String(32))
    is_hazardous = Column(Boolean, default=False)
    hazard_type = Column(String(128))
    recovery_method = Column(String(128))
    ai_predicted_component = Column(String(128))
    ai_confidence = Column(Float)
    created_at = Column(DateTime, default=_now)

    device = relationship("Device", back_populates="components")
    materials = relationship("Material", back_populates="component", cascade="all, delete-orphan")


class Material(Base):
    __tablename__ = "materials"

    id = Column(String, primary_key=True, default=_uuid)
    component_id = Column(String, ForeignKey("components.id"), nullable=False)
    material_name = Column(String(128))        # gold, copper, lithium, etc.
    estimated_quantity_g = Column(Float)
    actual_quantity_g = Column(Float)
    unit = Column(String(16), default="g")
    purity_percent = Column(Float)
    recovery_rate_percent = Column(Float)
    source = Column(String(32))               # measured / ai_predicted / rule_based / estimated
    created_at = Column(DateTime, default=_now)

    component = relationship("Component", back_populates="materials")


# ══════════════════════════════════════════════════════════════════════════════
# INVENTORY
# ══════════════════════════════════════════════════════════════════════════════

class InventoryItem(Base):
    __tablename__ = "inventory"

    id = Column(String, primary_key=True, default=_uuid)
    material_name = Column(String(128), nullable=False, index=True)
    quantity_g = Column(Float, default=0.0)
    unit = Column(String(16), default="g")
    purity_percent = Column(Float)
    location = Column(String(256))
    batch_id = Column(String, ForeignKey("waste_batches.id"), nullable=True)
    source = Column(String(64))               # recycled / purchased / mixed
    created_at = Column(DateTime, default=_now)
    updated_at = Column(DateTime, default=_now, onupdate=_now)


# ══════════════════════════════════════════════════════════════════════════════
# RECOVERY RECORDS
# ══════════════════════════════════════════════════════════════════════════════

class RecoveryRecord(Base):
    __tablename__ = "recovery_records"

    id = Column(String, primary_key=True, default=_uuid)
    batch_id = Column(String, ForeignKey("waste_batches.id"), nullable=False)
    material_name = Column(String(128))
    recovered_quantity_g = Column(Float)
    recovery_method = Column(String(128))
    recovery_rate_percent = Column(Float)
    estimated_value_usd = Column(Float)
    actual_value_usd = Column(Float)
    value_source = Column(String(64))          # measured / estimated / ai_predicted
    price_per_g_usd = Column(Float)
    price_source = Column(String(128))
    price_timestamp = Column(DateTime)
    notes = Column(Text)
    recorded_at = Column(DateTime, default=_now)

    batch = relationship("WasteBatch", back_populates="recovery_records")


# ══════════════════════════════════════════════════════════════════════════════
# PROCESSING OPERATIONS
# ══════════════════════════════════════════════════════════════════════════════

class ProcessingOperation(Base):
    __tablename__ = "processing_operations"

    id = Column(String, primary_key=True, default=_uuid)
    batch_id = Column(String, ForeignKey("waste_batches.id"), nullable=False)
    operation_type = Column(String(64))        # sorting / dismantling / shredding / smelting
    operator = Column(String(128))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration_minutes = Column(Float)
    input_weight_kg = Column(Float)
    output_weight_kg = Column(Float)
    waste_weight_kg = Column(Float)
    notes = Column(Text)
    status = Column(String(32), default="completed")
    created_at = Column(DateTime, default=_now)

    batch = relationship("WasteBatch", back_populates="operations")


# ══════════════════════════════════════════════════════════════════════════════
# COSTS
# ══════════════════════════════════════════════════════════════════════════════

class OperationalCost(Base):
    __tablename__ = "operational_costs"

    id = Column(String, primary_key=True, default=_uuid)
    batch_id = Column(String, ForeignKey("waste_batches.id"), nullable=True)
    cost_type = Column(String(64))             # labor / energy / transport / disposal / other
    description = Column(String(256))
    amount_usd = Column(Float, nullable=False)
    currency = Column(String(8), default="USD")
    is_estimated = Column(Boolean, default=True)
    estimation_method = Column(String(128))
    recorded_at = Column(DateTime, default=_now)
    recorded_by = Column(String(128))

    batch = relationship("WasteBatch", back_populates="cost_records")


# ══════════════════════════════════════════════════════════════════════════════
# AI PREDICTIONS
# ══════════════════════════════════════════════════════════════════════════════

class AIPrediction(Base):
    __tablename__ = "ai_predictions"

    id = Column(String, primary_key=True, default=_uuid)
    model_id = Column(String, ForeignKey("ml_models.id"), nullable=True)
    model_name = Column(String(128))
    model_version = Column(String(32))
    task_type = Column(String(64))             # classification / regression / recovery / economic
    input_type = Column(String(32))            # image / tabular / batch
    input_reference = Column(String(512))      # file path or batch_id
    input_hash = Column(String(128))
    prediction = Column(JSON)                  # actual prediction output
    confidence = Column(Float)
    prediction_type = Column(String(32))       # actual_model / rule_based / unavailable
    dataset_version = Column(String(32))
    experiment_id = Column(String)
    created_at = Column(DateTime, default=_now, index=True)

    model = relationship("MLModel", back_populates="predictions")

    __table_args__ = (Index("ix_ai_predictions_task_type", "task_type"),)


# ══════════════════════════════════════════════════════════════════════════════
# ENVIRONMENTAL REPORTS
# ══════════════════════════════════════════════════════════════════════════════

class EnvironmentalReport(Base):
    __tablename__ = "environmental_reports"

    id = Column(String, primary_key=True, default=_uuid)
    batch_id = Column(String, ForeignKey("waste_batches.id"), nullable=True)
    report_period_start = Column(DateTime)
    report_period_end = Column(DateTime)
    total_waste_kg = Column(Float)
    total_recovered_kg = Column(Float)
    hazardous_waste_kg = Column(Float)
    recycling_rate_percent = Column(Float)
    co2_avoided_kg_estimate = Column(Float)
    co2_calculation_method = Column(String(256))
    assumptions = Column(JSON)
    is_certified = Column(Boolean, default=False)
    certification_note = Column(Text)
    generated_at = Column(DateTime, default=_now)
    generated_by = Column(String(128))


# ══════════════════════════════════════════════════════════════════════════════
# GENERATED REPORTS
# ══════════════════════════════════════════════════════════════════════════════

class GeneratedReport(Base):
    __tablename__ = "generated_reports"

    id = Column(String, primary_key=True, default=_uuid)
    report_type = Column(String(64), index=True)
    title = Column(String(256))
    description = Column(Text)
    file_path = Column(String(512))
    file_format = Column(String(16))           # pdf / xlsx / json / csv
    file_size_bytes = Column(Integer)
    parameters = Column(JSON)
    data_sources = Column(JSON)
    generated_at = Column(DateTime, default=_now, index=True)
    generated_by = Column(String(128))
    is_available = Column(Boolean, default=True)


# ══════════════════════════════════════════════════════════════════════════════
# RESEARCH EXPERIMENTS
# ══════════════════════════════════════════════════════════════════════════════

class ResearchExperiment(Base):
    __tablename__ = "research_experiments"

    id = Column(String, primary_key=True, default=_uuid)
    experiment_name = Column(String(256), nullable=False)
    objective = Column(Text)
    dataset_id = Column(String, ForeignKey("datasets.id"), nullable=True)
    dataset_version = Column(String(32))
    model_architecture = Column(String(128))
    hyperparameters = Column(JSON)
    random_seed = Column(Integer)
    evaluation_protocol = Column(String(128))
    metrics = Column(JSON)
    duration_sec = Column(Float)
    library_versions = Column(JSON)
    notes = Column(Text)
    status = Column(String(32), default="completed")
    created_at = Column(DateTime, default=_now, index=True)

    dataset = relationship("Dataset", back_populates="experiments")
