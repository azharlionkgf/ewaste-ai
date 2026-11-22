"""
E-Waste AI — Research ORM Models
===================================
SQLAlchemy models for research experiment tracking,
baseline comparisons and reproducible results storage.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base
from backend.models.base import TimestampMixin


class ResearchExperiment(Base, TimestampMixin):
    """Research experiment registry."""
    __tablename__ = "research_experiments"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    experiment_code     = Column(String(100), unique=True, nullable=True, index=True)
    experiment_name     = Column(String(500), nullable=True)
    name                = Column(String(500), nullable=True)   # convenient alias
    description         = Column(Text, nullable=True)
    researcher          = Column(String(255), nullable=True)
    research_question   = Column(Text, nullable=True)
    hypothesis          = Column(Text, nullable=True)
    methodology         = Column(Text, nullable=True)
    dataset_ids         = Column(Text, nullable=True)   # JSON array of dataset IDs
    baseline_reference  = Column(Text, nullable=True)   # paper/model being compared against
    expected_outcome    = Column(Text, nullable=True)
    actual_outcome      = Column(Text, nullable=True)   # filled after completion
    limitations         = Column(Text, nullable=True)
    tags                = Column(Text, nullable=True)   # JSON array
    status              = Column(String(50), default="planned")
    # planned|running|completed|published

    runs = relationship("ExperimentRun", back_populates="experiment",
                        cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ResearchExperiment code={self.experiment_code} status={self.status}>"


class ExperimentRun(Base, TimestampMixin):
    """Individual runs within a research experiment."""
    __tablename__ = "experiment_runs"

    id                    = Column(Integer, primary_key=True, autoincrement=True)
    experiment_id         = Column(Integer, ForeignKey("research_experiments.id"), nullable=False, index=True)
    training_run_id       = Column(Integer, nullable=True, index=True)
    run_name              = Column(String(255), nullable=False)
    run_description       = Column(Text, nullable=True)
    hyperparameters       = Column(Text, nullable=True)   # JSON
    dataset_version       = Column(String(100), nullable=True)
    preprocessing_hash    = Column(String(64), nullable=True)
    random_seed           = Column(Integer, nullable=True)
    is_baseline           = Column(Boolean, default=False)
    result_summary        = Column(Text, nullable=True)   # JSON: key metrics
    notes                 = Column(Text, nullable=True)
    run_at                = Column(DateTime, default=datetime.utcnow)

    experiment = relationship("ResearchExperiment", back_populates="runs")
    metrics    = relationship("ExperimentMetric", back_populates="run",
                              cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ExperimentRun id={self.id} name='{self.run_name}'>"


class ExperimentMetric(Base):
    """Detailed metrics per experiment run (supports custom metrics)."""
    __tablename__ = "experiment_metrics"

    id                 = Column(Integer, primary_key=True, autoincrement=True)
    experiment_run_id  = Column(Integer, ForeignKey("experiment_runs.id"), nullable=False, index=True)
    metric_name        = Column(String(255), nullable=False)
    metric_value       = Column(Float, nullable=False)
    metric_type        = Column(String(50), nullable=True)   # primary|secondary|custom
    split              = Column(String(20), nullable=True)   # train|val|test
    recorded_at        = Column(DateTime, default=datetime.utcnow)

    run = relationship("ExperimentRun", back_populates="metrics")

    def __repr__(self):
        return f"<ExperimentMetric run_id={self.experiment_run_id} {self.metric_name}={self.metric_value}>"


class BaselineComparison(Base, TimestampMixin):
    """Published benchmark comparisons."""
    __tablename__ = "baseline_comparisons"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    experiment_id       = Column(Integer, nullable=False, index=True)
    baseline_name       = Column(String(255), nullable=False)
    source_paper        = Column(Text, nullable=True)       # paper title / DOI
    dataset_name        = Column(String(255), nullable=True)
    reported_accuracy   = Column(Float, nullable=True)
    reported_f1         = Column(Float, nullable=True)
    our_accuracy        = Column(Float, nullable=True)      # filled after experiment
    our_f1              = Column(Float, nullable=True)
    notes               = Column(Text, nullable=True)
    is_verified         = Column(Boolean, default=False)

    def __repr__(self):
        return f"<BaselineComparison experiment_id={self.experiment_id} baseline={self.baseline_name}>"


class ResearchReport(Base, TimestampMixin):
    """Generated research reports."""
    __tablename__ = "research_reports"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    experiment_id   = Column(Integer, nullable=True, index=True)
    report_type     = Column(String(100), nullable=False)  # academic|industrial|evaluation|environmental
    title           = Column(String(500), nullable=False)
    file_path       = Column(Text, nullable=True)
    file_format     = Column(String(20), default="pdf")
    section_config  = Column(Text, nullable=True)   # JSON: which sections to include
    generated_by    = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<ResearchReport type={self.report_type} title='{self.title[:40]}'>"
