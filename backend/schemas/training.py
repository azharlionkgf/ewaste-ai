"""
E-Waste AI — Pydantic Schemas: ML Training & Evaluation
=========================================================
Request and response schemas for training and evaluation APIs.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ModelTypeEnum(str, Enum):
    cnn                 = "cnn"
    random_forest       = "random_forest"
    xgboost             = "xgboost"
    catboost            = "catboost"
    svm                 = "svm"
    logistic_regression = "logistic_regression"


class CNNArchEnum(str, Enum):
    mobilenetv3_small = "mobilenetv3_small"
    mobilenetv3_large = "mobilenetv3_large"
    efficientnet_b0   = "efficientnet_b0"
    resnet18          = "resnet18"
    resnet34          = "resnet34"


class TrainingStatusEnum(str, Enum):
    pending   = "pending"
    running   = "running"
    completed = "completed"
    failed    = "failed"
    cancelled = "cancelled"


# ── Training Request ──────────────────────────────────────────────────

class CNNHyperparams(BaseModel):
    optimizer:    str   = Field(default="adam", description="adam|sgd|adamw")
    lr:           float = Field(default=0.001, ge=1e-6, le=0.1)
    batch_size:   int   = Field(default=16, ge=1, le=256)
    epochs:       int   = Field(default=30, ge=1, le=200)
    weight_decay: float = Field(default=1e-4, ge=0.0)
    scheduler:    str   = Field(default="cosine", description="cosine|step|none")
    pretrained:   bool  = True
    freeze_layers:int   = Field(default=0, ge=0, description="Number of backbone layers to freeze")
    dropout:      float = Field(default=0.2, ge=0.0, le=0.8)


class TabularHyperparams(BaseModel):
    n_estimators:   Optional[int]   = Field(default=100, ge=10)
    max_depth:      Optional[int]   = Field(default=None, ge=1)
    learning_rate:  Optional[float] = Field(default=0.1, ge=1e-5)
    subsample:      Optional[float] = Field(default=0.8, ge=0.1, le=1.0)
    min_child_weight: Optional[int] = Field(default=1, ge=1)
    C:              Optional[float] = Field(default=1.0, ge=1e-5, description="SVM regularization")
    kernel:         Optional[str]   = Field(default="rbf", description="SVM kernel: rbf|linear|poly")
    max_iter:       Optional[int]   = Field(default=1000)


class TrainingRequest(BaseModel):
    dataset_id:        int
    preprocessing_id:  Optional[int]  = None
    run_name:          str            = Field(..., min_length=2, max_length=255)
    model_type:        ModelTypeEnum
    architecture:      Optional[CNNArchEnum] = None
    cnn_hyperparams:   Optional[CNNHyperparams]     = None
    tabular_hyperparams: Optional[TabularHyperparams] = None
    random_seed:       int = Field(default=42, ge=0)
    target_column:     Optional[str] = None
    feature_columns:   Optional[List[str]] = None


# ── Training Response ─────────────────────────────────────────────────

class TrainingProgressEvent(BaseModel):
    """WebSocket progress event schema."""
    event:       str = "training_progress"
    epoch:       int
    total_epochs:int
    train_loss:  float
    val_loss:    float
    train_acc:   float
    val_acc:     float
    eta_seconds: int
    status:      str


class TrainingRunResponse(BaseModel):
    id:                 int
    dataset_id:         int
    run_name:           str
    model_type:         str
    architecture:       Optional[str]
    hyperparameters:    str
    random_seed:        int
    num_classes:        Optional[int]
    epochs_completed:   int
    final_train_acc:    Optional[float]
    final_val_acc:      Optional[float]
    training_duration_s:Optional[float]
    model_path:         Optional[str]
    status:             str
    started_at:         Optional[datetime]
    completed_at:       Optional[datetime]
    created_at:         datetime

    class Config:
        from_attributes = True


# ── Evaluation Response ───────────────────────────────────────────────

class EvaluationResponse(BaseModel):
    id:                  int
    training_run_id:     int
    dataset_split:       str
    accuracy:            Optional[float]
    precision_macro:     Optional[float]
    precision_weighted:  Optional[float]
    recall_macro:        Optional[float]
    recall_weighted:     Optional[float]
    f1_macro:            Optional[float]
    f1_weighted:         Optional[float]
    roc_auc:             Optional[float]
    cohen_kappa:         Optional[float]
    inference_time_ms:   Optional[float]
    confusion_matrix:    Optional[str]   # JSON
    classification_report: Optional[str] # JSON
    evaluated_at:        datetime

    class Config:
        from_attributes = True


# ── Inference ─────────────────────────────────────────────────────────

class InferenceRequest(BaseModel):
    training_run_id: int
    return_top_k:    int = Field(default=5, ge=1, le=20)


class InferenceResponse(BaseModel):
    predicted_label:   str
    confidence_score:  float
    top_predictions:   List[Dict[str, Any]]
    inference_time_ms: float
    is_estimate:       bool = True
    model_used:        str
