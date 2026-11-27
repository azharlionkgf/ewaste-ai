"""
E-Waste AI — Pydantic Schemas (Phase 4)
========================================
Request/Response models for all API endpoints.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


# ══════════════════════════════════════════════════════════════════════════════
# BASE
# ══════════════════════════════════════════════════════════════════════════════

class SuccessResponse(BaseModel):
    success: bool = True
    message: str = "OK"
    data: Any = None


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None


# ══════════════════════════════════════════════════════════════════════════════
# AUTH / USERS
# ══════════════════════════════════════════════════════════════════════════════

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None
    role: str = "operator"

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        allowed = {"admin", "manager", "operator", "researcher"}
        if v not in allowed:
            raise ValueError(f"Role must be one of {allowed}")
        return v


class UserOut(BaseModel):
    id: str
    username: str
    email: str
    full_name: Optional[str]
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class LoginRequest(BaseModel):
    username: str
    password: str


# ══════════════════════════════════════════════════════════════════════════════
# WASTE BATCHES
# ══════════════════════════════════════════════════════════════════════════════

class WasteBatchCreate(BaseModel):
    source: str = Field(..., min_length=2, max_length=256)
    total_weight_kg: float = Field(..., gt=0)
    waste_category: Optional[str] = None
    location: Optional[str] = None
    received_date: Optional[datetime] = None
    notes: Optional[str] = None


class WasteBatchOut(BaseModel):
    id: str
    batch_number: str
    source: str
    received_date: Optional[datetime]
    total_weight_kg: Optional[float]
    waste_category: Optional[str]
    status: str
    location: Optional[str]
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class BatchStatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        allowed = {"received", "sorted", "dismantled", "processed", "completed"}
        if v not in allowed:
            raise ValueError(f"Status must be one of {allowed}")
        return v


# ══════════════════════════════════════════════════════════════════════════════
# DEVICES
# ══════════════════════════════════════════════════════════════════════════════

class DeviceCreate(BaseModel):
    batch_id: str
    device_type: Optional[str] = None
    manufacturer: Optional[str] = None
    model_name: Optional[str] = None
    year_manufactured: Optional[int] = None
    weight_kg: Optional[float] = None
    condition: Optional[str] = "unknown"


class DeviceOut(BaseModel):
    id: str
    batch_id: str
    device_type: Optional[str]
    manufacturer: Optional[str]
    model_name: Optional[str]
    weight_kg: Optional[float]
    condition: Optional[str]
    ai_predicted_category: Optional[str]
    ai_confidence: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True


# ══════════════════════════════════════════════════════════════════════════════
# AI PREDICTIONS
# ══════════════════════════════════════════════════════════════════════════════

class PredictionRequest(BaseModel):
    task_type: str
    input_data: dict
    model_id: Optional[str] = None
    dataset_version: Optional[str] = None


class PredictionOut(BaseModel):
    id: str
    task_type: str
    prediction: Any
    confidence: Optional[float]
    prediction_type: str
    model_name: Optional[str]
    model_version: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ClassificationResult(BaseModel):
    predicted_class: str
    confidence: float
    all_classes: Optional[dict] = None
    model_used: str
    prediction_type: str           # actual_model / rule_based / unavailable
    disclaimer: str = "AI predictions are estimates. Verify before operational use."


class RegressionResult(BaseModel):
    predicted_value: float
    unit: str
    uncertainty_note: str = "Prediction uncertainty not quantified for this model."
    model_used: str
    prediction_type: str
    disclaimer: str = "Financial estimates are for guidance only."


# ══════════════════════════════════════════════════════════════════════════════
# RECOVERY INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════

class RecoveryEstimateRequest(BaseModel):
    device_type: Optional[str] = None
    weight_kg: Optional[float] = None
    components: Optional[list] = None
    batch_id: Optional[str] = None


class MaterialEstimate(BaseModel):
    material_name: str
    estimated_quantity_g: float
    recovery_rate_percent: float
    recoverable_quantity_g: float
    source: str                    # rule_based / ai_predicted / measured
    confidence: Optional[str] = None


class RecoveryEstimateOut(BaseModel):
    device_type: Optional[str]
    weight_kg: Optional[float]
    materials: list[MaterialEstimate]
    total_recoverable_g: float
    recommendations: list[str]
    disclaimer: str = (
        "Material estimates are based on published composition data and rule-based models. "
        "Actual yields depend on device-specific composition and processing quality."
    )


# ══════════════════════════════════════════════════════════════════════════════
# ECONOMIC INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════

class EconomicAnalysisRequest(BaseModel):
    batch_id: Optional[str] = None
    materials: Optional[list] = None
    weight_kg: Optional[float] = None
    device_type: Optional[str] = None
    processing_cost_usd: Optional[float] = None


class EconomicAnalysisOut(BaseModel):
    gross_recovery_value_usd: float
    estimated_processing_cost_usd: float
    net_value_usd: float
    material_breakdown: list[dict]
    price_sources: list[str]
    assumptions: list[str]
    disclaimer: str = (
        "Financial estimates use indicative market prices and standard processing costs. "
        "Actual values depend on current market conditions and processing efficiency."
    )


# ══════════════════════════════════════════════════════════════════════════════
# INVENTORY
# ══════════════════════════════════════════════════════════════════════════════

class InventoryItemCreate(BaseModel):
    material_name: str
    quantity_g: float = Field(..., ge=0)
    unit: str = "g"
    purity_percent: Optional[float] = None
    location: Optional[str] = None
    batch_id: Optional[str] = None
    source: str = "recycled"


class InventoryItemOut(BaseModel):
    id: str
    material_name: str
    quantity_g: float
    unit: str
    purity_percent: Optional[float]
    location: Optional[str]
    source: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ══════════════════════════════════════════════════════════════════════════════
# RECOVERY RECORDS
# ══════════════════════════════════════════════════════════════════════════════

class RecoveryRecordCreate(BaseModel):
    batch_id: str
    material_name: str
    recovered_quantity_g: float = Field(..., ge=0)
    recovery_method: Optional[str] = None
    recovery_rate_percent: Optional[float] = None
    estimated_value_usd: Optional[float] = None
    price_per_g_usd: Optional[float] = None
    price_source: Optional[str] = None
    notes: Optional[str] = None


class RecoveryRecordOut(BaseModel):
    id: str
    batch_id: str
    material_name: str
    recovered_quantity_g: float
    recovery_method: Optional[str]
    recovery_rate_percent: Optional[float]
    estimated_value_usd: Optional[float]
    price_source: Optional[str]
    recorded_at: datetime

    class Config:
        from_attributes = True


# ══════════════════════════════════════════════════════════════════════════════
# OPERATIONAL COSTS
# ══════════════════════════════════════════════════════════════════════════════

class OperationalCostCreate(BaseModel):
    batch_id: Optional[str] = None
    cost_type: str
    description: Optional[str] = None
    amount_usd: float = Field(..., gt=0)
    is_estimated: bool = True
    estimation_method: Optional[str] = None


class OperationalCostOut(BaseModel):
    id: str
    batch_id: Optional[str]
    cost_type: str
    description: Optional[str]
    amount_usd: float
    is_estimated: bool
    recorded_at: datetime

    class Config:
        from_attributes = True


# ══════════════════════════════════════════════════════════════════════════════
# RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════

class RecommendationOut(BaseModel):
    batch_id: Optional[str]
    device_type: Optional[str]
    recommendations: list[dict]
    hazard_flags: list[str]
    reasoning: list[str]
    disclaimer: str = (
        "These are AI-generated operational recommendations. "
        "They do not constitute certified safety or legal compliance guidance. "
        "Hazardous materials must be handled by qualified professionals."
    )


# ══════════════════════════════════════════════════════════════════════════════
# ENVIRONMENTAL REPORTS
# ══════════════════════════════════════════════════════════════════════════════

class EnvironmentalReportCreate(BaseModel):
    batch_id: Optional[str] = None
    report_period_start: Optional[datetime] = None
    report_period_end: Optional[datetime] = None
    total_waste_kg: Optional[float] = None
    total_recovered_kg: Optional[float] = None
    hazardous_waste_kg: Optional[float] = None


class EnvironmentalReportOut(BaseModel):
    id: str
    batch_id: Optional[str]
    total_waste_kg: Optional[float]
    total_recovered_kg: Optional[float]
    recycling_rate_percent: Optional[float]
    co2_avoided_kg_estimate: Optional[float]
    assumptions: Optional[dict]
    is_certified: bool
    certification_note: Optional[str]
    generated_at: datetime

    class Config:
        from_attributes = True


# ══════════════════════════════════════════════════════════════════════════════
# REPORTS
# ══════════════════════════════════════════════════════════════════════════════

class ReportRequest(BaseModel):
    report_type: str
    parameters: Optional[dict] = None
    file_format: str = "json"

    @field_validator("file_format")
    @classmethod
    def validate_format(cls, v):
        allowed = {"json", "csv", "xlsx", "pdf"}
        if v not in allowed:
            raise ValueError(f"Format must be one of {allowed}")
        return v


class ReportOut(BaseModel):
    id: str
    report_type: str
    title: str
    file_format: str
    file_size_bytes: Optional[int]
    generated_at: datetime
    is_available: bool
    download_url: Optional[str]

    class Config:
        from_attributes = True
