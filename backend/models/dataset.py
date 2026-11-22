"""
E-Waste AI — Dataset ORM Models
=================================
SQLAlchemy models for dataset management and versioning.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base
from backend.models.base import TimestampMixin


class Dataset(Base, TimestampMixin):
    """Master dataset registry."""
    __tablename__ = "datasets"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    name          = Column(String(255), nullable=False, index=True)
    version       = Column(String(50), nullable=False, default="1.0")
    file_type     = Column(String(50), nullable=False)   # csv|excel|json|images|mixed
    file_path     = Column(Text, nullable=False)
    row_count     = Column(Integer, nullable=True)
    column_count  = Column(Integer, nullable=True)
    image_count   = Column(Integer, nullable=True)
    file_size_mb  = Column(Float, nullable=True)
    description   = Column(Text, nullable=True)
    tags          = Column(Text, nullable=True)           # JSON array string
    source        = Column(String(500), nullable=True)    # Where dataset came from
    license       = Column(String(255), nullable=True)
    checksum      = Column(String(64), nullable=True)     # SHA-256
    status        = Column(String(50), default="uploaded", nullable=False)
    # Status values: uploaded|inspected|cleaned|preprocessed|split|archived

    # Relationships
    cleaning_runs       = relationship("CleaningRun", back_populates="dataset", cascade="all, delete-orphan")
    preprocessing_configs = relationship("PreprocessingConfig", back_populates="dataset", cascade="all, delete-orphan")
    training_runs       = relationship("TrainingRun", back_populates="dataset", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Dataset id={self.id} name='{self.name}' v{self.version} type={self.file_type}>"


class DatasetVersion(Base, TimestampMixin):
    """Tracks dataset versions for reproducibility."""
    __tablename__ = "dataset_versions"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    dataset_id    = Column(Integer, ForeignKey("datasets.id"), nullable=False, index=True)
    version       = Column(String(50), nullable=False)
    file_path     = Column(Text, nullable=False)
    checksum      = Column(String(64), nullable=True)
    change_notes  = Column(Text, nullable=True)
    row_count     = Column(Integer, nullable=True)
    is_current    = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<DatasetVersion dataset_id={self.dataset_id} v={self.version}>"


class CleaningRun(Base, TimestampMixin):
    """Records of automated data cleaning operations."""
    __tablename__ = "cleaning_runs"

    id                   = Column(Integer, primary_key=True, autoincrement=True)
    dataset_id           = Column(Integer, ForeignKey("datasets.id"), nullable=False, index=True)
    missing_before       = Column(Integer, default=0)
    missing_after        = Column(Integer, default=0)
    duplicates_found     = Column(Integer, default=0)
    duplicates_removed   = Column(Integer, default=0)
    outliers_flagged     = Column(Integer, default=0)
    outliers_removed     = Column(Integer, default=0)
    type_errors_fixed    = Column(Integer, default=0)
    rows_before          = Column(Integer, nullable=True)
    rows_after           = Column(Integer, nullable=True)
    cleaning_config      = Column(Text, nullable=True)   # JSON config used
    output_file_path     = Column(Text, nullable=True)
    cleaning_report      = Column(Text, nullable=True)   # JSON summary
    status               = Column(String(50), default="pending")
    error_message        = Column(Text, nullable=True)

    dataset = relationship("Dataset", back_populates="cleaning_runs")

    def __repr__(self):
        return f"<CleaningRun id={self.id} dataset_id={self.dataset_id} status={self.status}>"


class PreprocessingConfig(Base, TimestampMixin):
    """Saved preprocessing configurations for reproducibility."""
    __tablename__ = "preprocessing_configs"

    id               = Column(Integer, primary_key=True, autoincrement=True)
    dataset_id       = Column(Integer, ForeignKey("datasets.id"), nullable=False, index=True)
    config_name      = Column(String(255), nullable=True)
    scaler_type      = Column(String(50), nullable=True)   # standard|minmax|robust|none
    encoder_type     = Column(String(50), nullable=True)   # onehot|label|ordinal|none
    feature_columns  = Column(Text, nullable=True)         # JSON array
    target_column    = Column(String(255), nullable=True)
    train_ratio      = Column(Float, default=0.70)
    val_ratio        = Column(Float, default=0.15)
    test_ratio       = Column(Float, default=0.15)
    augmentation_cfg = Column(Text, nullable=True)         # JSON
    output_dir       = Column(Text, nullable=True)
    config_hash      = Column(String(64), nullable=True)
    is_active        = Column(Boolean, default=True)

    dataset = relationship("Dataset", back_populates="preprocessing_configs")

    def __repr__(self):
        return f"<PreprocessingConfig id={self.id} dataset_id={self.dataset_id}>"
