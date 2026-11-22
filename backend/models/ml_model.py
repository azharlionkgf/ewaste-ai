"""
E-Waste AI — ML Model ORM Models
===================================
SQLAlchemy models for training runs, trained models and evaluations.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base
from backend.models.base import TimestampMixin


class TrainingRun(Base, TimestampMixin):
    """Records every model training job with full reproducibility info."""
    __tablename__ = "training_runs"

    id                   = Column(Integer, primary_key=True, autoincrement=True)
    dataset_id           = Column(Integer, ForeignKey("datasets.id"), nullable=False, index=True)
    preprocessing_id     = Column(Integer, nullable=True, index=True)
    run_name             = Column(String(255), nullable=False)
    model_type           = Column(String(50), nullable=False)   # cnn|random_forest|xgboost|catboost|svm|logistic_regression
    architecture         = Column(String(100), nullable=True)   # mobilenetv3_small|efficientnet_b0|...
    hyperparameters      = Column(Text, nullable=False)         # JSON
    random_seed          = Column(Integer, default=42)
    num_classes          = Column(Integer, nullable=True)
    class_names          = Column(Text, nullable=True)          # JSON array
    epochs_planned       = Column(Integer, nullable=True)
    epochs_completed     = Column(Integer, default=0)
    best_epoch           = Column(Integer, nullable=True)
    final_train_loss     = Column(Float, nullable=True)
    final_val_loss       = Column(Float, nullable=True)
    final_train_acc      = Column(Float, nullable=True)
    final_val_acc        = Column(Float, nullable=True)
    training_duration_s  = Column(Float, nullable=True)
    model_path           = Column(Text, nullable=True)          # saved weights path
    model_size_mb        = Column(Float, nullable=True)
    training_history     = Column(Text, nullable=True)          # JSON per-epoch history
    status               = Column(String(50), default="pending")
    # Status: pending|running|completed|failed|cancelled
    error_message        = Column(Text, nullable=True)
    started_at           = Column(DateTime, nullable=True)
    completed_at         = Column(DateTime, nullable=True)
    mlflow_run_id        = Column(String(255), nullable=True)   # MLflow integration

    dataset    = relationship("Dataset", back_populates="training_runs")
    evaluation = relationship("ModelEvaluation", back_populates="training_run",
                              uselist=False, cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="training_run",
                               cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TrainingRun id={self.id} name='{self.run_name}' type={self.model_type} status={self.status}>"


class ModelEvaluation(Base, TimestampMixin):
    """Comprehensive evaluation metrics for each trained model."""
    __tablename__ = "model_evaluations"

    id                   = Column(Integer, primary_key=True, autoincrement=True)
    training_run_id      = Column(Integer, ForeignKey("training_runs.id"), nullable=False, unique=True, index=True)
    dataset_split        = Column(String(20), default="test")  # val|test
    accuracy             = Column(Float, nullable=True)
    precision_macro      = Column(Float, nullable=True)
    precision_weighted   = Column(Float, nullable=True)
    recall_macro         = Column(Float, nullable=True)
    recall_weighted      = Column(Float, nullable=True)
    f1_macro             = Column(Float, nullable=True)
    f1_weighted          = Column(Float, nullable=True)
    roc_auc              = Column(Float, nullable=True)
    cohen_kappa          = Column(Float, nullable=True)
    confusion_matrix     = Column(Text, nullable=True)   # JSON 2D array
    classification_report = Column(Text, nullable=True)  # JSON full report
    per_class_metrics    = Column(Text, nullable=True)   # JSON per-class breakdown
    inference_time_ms    = Column(Float, nullable=True)  # ms per sample
    evaluated_at         = Column(DateTime, default=datetime.utcnow)

    training_run = relationship("TrainingRun", back_populates="evaluation")

    def __repr__(self):
        return f"<ModelEvaluation id={self.id} run_id={self.training_run_id} accuracy={self.accuracy:.4f}>"


class Prediction(Base, TimestampMixin):
    """Individual prediction records (for audit trail)."""
    __tablename__ = "predictions"

    id                = Column(Integer, primary_key=True, autoincrement=True)
    training_run_id   = Column(Integer, ForeignKey("training_runs.id"), nullable=False, index=True)
    input_path        = Column(Text, nullable=True)       # file path of input
    input_type        = Column(String(50), nullable=True) # image|tabular|video_frame
    predicted_label   = Column(String(255), nullable=True)
    predicted_class_id= Column(Integer, nullable=True)
    confidence_score  = Column(Float, nullable=True)
    top_predictions   = Column(Text, nullable=True)       # JSON [{label, score}...]
    true_label        = Column(String(255), nullable=True) # if ground truth known
    is_correct        = Column(Boolean, nullable=True)
    inference_time_ms = Column(Float, nullable=True)
    batch_item_id     = Column(Integer, nullable=True, index=True)

    training_run = relationship("TrainingRun", back_populates="predictions")

    def __repr__(self):
        return f"<Prediction id={self.id} label='{self.predicted_label}' conf={self.confidence_score:.3f}>"
