"""
Phase 4 API Routers — AI Model Integration & Classification (Tasks 3-4)
"""
from __future__ import annotations
import logging
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from typing import Optional

from backend.database import get_db
from backend.models.all_models import AIPrediction
from backend.schemas.all_schemas import PredictionRequest, PredictionOut
from backend.services.ai_model_service import (
    AIModelEngine, ModelNotAvailableError, ModelInferenceError, get_ai_engine,
)
from backend.services.auth_service import hash_file_content, sanitize_filename
from backend.config import MAX_UPLOAD_BYTES, ALLOWED_IMAGE_TYPES, UPLOAD_DIR

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/ai", tags=["AI Model Integration"])


def _get_engine() -> AIModelEngine:
    return get_ai_engine()


@router.get("/status")
def ai_status(engine: AIModelEngine = Depends(_get_engine)):
    """Check which task types have trained models available."""
    return {
        "models_available": engine.list_available_models(),
        "task_availability": engine.check_availability(),
        "note": "Train models in the AI Training Laboratory to enable predictions.",
    }


@router.get("/models")
def list_models(engine: AIModelEngine = Depends(_get_engine)):
    """List all registered models."""
    return engine.list_available_models()


@router.post("/predict/tabular")
def predict_tabular(
    request: PredictionRequest,
    db: Session = Depends(get_db),
    engine: AIModelEngine = Depends(_get_engine),
):
    """
    Run a tabular prediction using a trained model.
    Returns actual model prediction — never hardcoded values.
    If no model available, returns clear 'unavailable' status.
    """
    try:
        result = engine.predict_tabular(
            request.input_data,
            request.task_type,
            request.model_id,
        )
        # Save prediction to DB
        pred_record = AIPrediction(
            model_id=result.get("model_id"),
            model_name=result.get("model_name"),
            model_version=result.get("model_version"),
            task_type=request.task_type,
            input_type="tabular",
            prediction=result.get("prediction"),
            confidence=result.get("confidence"),
            prediction_type="actual_model",
            dataset_version=request.dataset_version,
        )
        db.add(pred_record)
        db.commit()
        result["prediction_id"] = pred_record.id
        return result

    except ModelNotAvailableError as exc:
        return {
            "task_type": request.task_type,
            "prediction_type": "unavailable",
            "prediction": None,
            "confidence": None,
            "message": str(exc),
            "action_required": "Train a model for this task type in the AI Training Laboratory.",
        }
    except ModelInferenceError as exc:
        raise HTTPException(status_code=500, detail=f"Inference error: {exc}")


@router.post("/predict/batch")
def predict_batch(
    task_type: str,
    records: list[dict],
    model_id: Optional[str] = None,
    engine: AIModelEngine = Depends(_get_engine),
):
    """Run batch predictions on multiple records."""
    if len(records) > 1000:
        raise HTTPException(400, detail="Batch size limit is 1000 records.")
    return engine.predict_batch(records, task_type, model_id)


@router.post("/classify/image")
async def classify_image(
    file: UploadFile = File(...),
    engine: AIModelEngine = Depends(_get_engine),
):
    """
    Upload image for e-waste classification.
    Returns prediction if a CNN model is trained; otherwise unavailable message.
    """
    # Validate file type
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(400, detail=f"File type '{file.content_type}' not allowed. Use JPEG/PNG/WebP.")

    content = await file.read()

    # Validate file size
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(413, detail=f"File too large. Max size: {MAX_UPLOAD_BYTES // 1024 // 1024} MB.")

    file_hash = hash_file_content(content)
    safe_name = sanitize_filename(file.filename or "upload.jpg")

    # Save uploaded file
    save_path = UPLOAD_DIR / safe_name
    save_path.write_bytes(content)

    # Try image classification model
    cnn_model = engine.get_active_model_for_task("ewaste_classification")
    if cnn_model is None:
        return {
            "task_type": "image_classification",
            "prediction_type": "unavailable",
            "prediction": None,
            "message": "No CNN image classification model is trained yet.",
            "action_required": "Train an image classification model in the AI Training Laboratory.",
            "file_hash": file_hash,
            "file_saved": str(save_path),
        }

    # CNN prediction via tabular feature proxy (actual CNN inference requires torch)
    try:
        result = {
            "task_type": "image_classification",
            "prediction_type": "model_loaded_no_inference",
            "model_name": cnn_model.get("name"),
            "file_hash": file_hash,
            "file_saved": str(save_path),
            "message": (
                "CNN model found in registry but image inference requires PyTorch runtime. "
                "Enable torch in environment or use the Streamlit frontend for image classification."
            ),
        }
        return result
    except Exception as exc:
        raise HTTPException(500, detail=f"Image classification error: {exc}")


@router.get("/predictions")
def prediction_history(
    task_type: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """Retrieve prediction history."""
    q = db.query(AIPrediction)
    if task_type:
        q = q.filter(AIPrediction.task_type == task_type)
    preds = q.order_by(AIPrediction.created_at.desc()).limit(limit).all()
    return [
        {
            "id": p.id,
            "task_type": p.task_type,
            "prediction": p.prediction,
            "confidence": p.confidence,
            "prediction_type": p.prediction_type,
            "model_name": p.model_name,
            "created_at": str(p.created_at),
        }
        for p in preds
    ]
