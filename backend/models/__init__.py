"""
E-Waste AI — SQLAlchemy ORM Model Registry
============================================
Imports all models so SQLAlchemy's metadata knows about every table.
Import this module before calling Base.metadata.create_all().
"""

from backend.models.base import TimestampMixin
from backend.models.dataset import (
    Dataset, DatasetVersion, CleaningRun, PreprocessingConfig
)
from backend.models.ml_model import (
    TrainingRun, ModelEvaluation, Prediction
)
from backend.models.waste_batch import (
    WasteBatch, BatchItem, ItemClassification,
    ItemComponent, MaterialRecovery,
    EconomicValuation, OperationalCost, EwasteCategory
)
from backend.models.research import (
    ResearchExperiment, ExperimentRun, ExperimentMetric,
    BaselineComparison, ResearchReport
)

__all__ = [
    "Dataset", "DatasetVersion", "CleaningRun", "PreprocessingConfig",
    "TrainingRun", "ModelEvaluation", "Prediction",
    "WasteBatch", "BatchItem", "ItemClassification", "ItemComponent",
    "MaterialRecovery", "EconomicValuation", "OperationalCost", "EwasteCategory",
    "ResearchExperiment", "ExperimentRun", "ExperimentMetric",
    "BaselineComparison", "ResearchReport",
]
