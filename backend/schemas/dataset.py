"""
E-Waste AI — Pydantic Schemas: Dataset
========================================
Request and response schemas for dataset API endpoints.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class FileTypeEnum(str, Enum):
    csv    = "csv"
    excel  = "excel"
    json   = "json"
    images = "images"
    mixed  = "mixed"


class DatasetStatusEnum(str, Enum):
    uploaded     = "uploaded"
    inspected    = "inspected"
    cleaned      = "cleaned"
    preprocessed = "preprocessed"
    split        = "split"
    archived     = "archived"


# ── Create / Update ──────────────────────────────────────────────────

class DatasetCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    version: str = Field(default="1.0", max_length=50)
    file_type: FileTypeEnum
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    source: Optional[str] = None
    license: Optional[str] = None


class DatasetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[DatasetStatusEnum] = None


# ── Response ─────────────────────────────────────────────────────────

class DatasetStats(BaseModel):
    row_count: Optional[int] = None
    column_count: Optional[int] = None
    image_count: Optional[int] = None
    file_size_mb: Optional[float] = None
    missing_values: Optional[int] = None
    duplicate_rows: Optional[int] = None
    class_distribution: Optional[dict] = None
    column_dtypes: Optional[dict] = None
    null_percentages: Optional[dict] = None


class DatasetResponse(BaseModel):
    id: int
    name: str
    version: str
    file_type: str
    file_path: str
    row_count: Optional[int]
    column_count: Optional[int]
    image_count: Optional[int]
    file_size_mb: Optional[float]
    description: Optional[str]
    tags: Optional[str]
    source: Optional[str]
    license: Optional[str]
    checksum: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DatasetListResponse(BaseModel):
    total: int
    items: List[DatasetResponse]


# ── Cleaning ─────────────────────────────────────────────────────────

class CleaningConfig(BaseModel):
    handle_missing: str = Field(default="mean", description="mean|median|mode|drop|ffill|bfill")
    remove_duplicates: bool = True
    remove_outliers: bool = False
    outlier_method: str = Field(default="iqr", description="iqr|zscore")
    outlier_threshold: float = Field(default=1.5, ge=0.5, le=5.0)
    fix_data_types: bool = True
    normalize_text: bool = True


class CleaningRunResponse(BaseModel):
    id: int
    dataset_id: int
    missing_before: int
    missing_after: int
    duplicates_found: int
    duplicates_removed: int
    outliers_flagged: int
    rows_before: Optional[int]
    rows_after: Optional[int]
    output_file_path: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── Preprocessing ─────────────────────────────────────────────────────

class PreprocessingConfigCreate(BaseModel):
    dataset_id: int
    config_name: Optional[str] = None
    scaler_type: str = Field(default="standard", description="standard|minmax|robust|none")
    encoder_type: str = Field(default="label", description="onehot|label|ordinal|none")
    feature_columns: Optional[List[str]] = None
    target_column: Optional[str] = None
    train_ratio: float = Field(default=0.70, ge=0.5, le=0.9)
    val_ratio: float = Field(default=0.15, ge=0.05, le=0.3)
    test_ratio: float = Field(default=0.15, ge=0.05, le=0.3)

    @field_validator("test_ratio")
    @classmethod
    def ratios_must_sum_to_one(cls, v, info):
        train = info.data.get("train_ratio", 0.70)
        val = info.data.get("val_ratio", 0.15)
        total = round(train + val + v, 10)
        if abs(total - 1.0) > 1e-6:
            raise ValueError(f"train+val+test ratios must sum to 1.0, got {total}")
        return v
