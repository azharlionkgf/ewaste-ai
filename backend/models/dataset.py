"""
E-Waste AI — Dataset ORM Models
=================================
SQLAlchemy models for dataset versioning, cleaning runs, and preprocessing configs.
Re-exports canonical Dataset from all_models to avoid duplicate Base registry entries.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.models.base import TimestampMixin
from backend.models.all_models import Dataset  # canonical Dataset ORM model (UUID PK)


class DatasetVersion(Base, TimestampMixin):
    """Tracks dataset versions for reproducibility."""
    __tablename__ = "dataset_versions"
    __table_args__ = {"extend_existing": True}

    id            = Column(Integer, primary_key=True, autoincrement=True)
    dataset_id    = Column(String, ForeignKey("datasets.id"), nullable=False, index=True)
    version       = Column(String(50), nullable=False)
    file_path     = Column(Text, nullable=False)
    checksum      = Column(String(64), nullable=True)
    change_notes  = Column(Text, nullable=True)
    row_count     = Column(Integer, nullable=True)
    is_current    = Column(Boolean, default=True, nullable=False)

    dataset = relationship(Dataset)

    def __repr__(self):
        return f"<DatasetVersion dataset_id={self.dataset_id} v={self.version}>"


class CleaningRun(Base, TimestampMixin):
    """Records of automated data cleaning operations."""
    __tablename__ = "cleaning_runs"
    __table_args__ = {"extend_existing": True}

    id                   = Column(Integer, primary_key=True, autoincrement=True)
    dataset_id           = Column(String, ForeignKey("datasets.id"), nullable=False, index=True)
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

    dataset = relationship(Dataset)

    def __repr__(self):
        return f"<CleaningRun id={self.id} dataset_id={self.dataset_id} status={self.status}>"


class PreprocessingConfig(Base, TimestampMixin):
    """Saved preprocessing configurations for reproducibility."""
    __tablename__ = "preprocessing_configs"
    __table_args__ = {"extend_existing": True}

    id               = Column(Integer, primary_key=True, autoincrement=True)
    dataset_id       = Column(String, ForeignKey("datasets.id"), nullable=False, index=True)
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

    dataset = relationship(Dataset)

    def __repr__(self):
        return f"<PreprocessingConfig id={self.id} dataset_id={self.dataset_id}>"
