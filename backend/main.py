"""
E-Waste AI — FastAPI Backend Main Application
=============================================
Run with: uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
API Docs: http://localhost:8000/docs
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    logger.info("E-Waste AI Backend starting up...")
    # TODO Phase 1: Initialize database
    # from backend.database import init_db
    # await init_db()
    yield
    logger.info("E-Waste AI Backend shutting down...")


app = FastAPI(
    title="E-Waste AI API",
    description=(
        "Combined Industrial Intelligence & Research Platform for Electronic Waste.\n\n"
        "Provides endpoints for dataset management, ML training, e-waste classification, "
        "material recovery estimation, economic valuation, and report generation."
    ),
    version="2.0.0",
    contact={
        "name": "Adil",
        "url": "https://github.com/azharlionkgf/ewaste-ai",
        "email": "otihaladil8@gmail.com",
    },
    license_info={"name": "MIT"},
    lifespan=lifespan,
)

# ── CORS ───────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static Files ────────────────────────────────────────────────────────
import os
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# ── Routers (added as phases complete) ─────────────────────────────────
# Phase 1:
# from backend.routers import datasets
# app.include_router(datasets.router, prefix="/api/datasets", tags=["Datasets"])

# Phase 2:
# from backend.routers import cleaning, preprocessing
# app.include_router(cleaning.router, prefix="/api/cleaning", tags=["Cleaning"])
# app.include_router(preprocessing.router, prefix="/api/preprocessing", tags=["Preprocessing"])

# Phase 4:
# from backend.routers import training
# app.include_router(training.router, prefix="/api/training", tags=["Training"])

# Phase 5:
# from backend.routers import evaluation
# app.include_router(evaluation.router, prefix="/api/evaluation", tags=["Evaluation"])

# Phase 6:
# from backend.routers import inference, video, recovery, reports
# app.include_router(inference.router, prefix="/api/inference", tags=["Inference"])
# app.include_router(video.router, prefix="/api/video", tags=["Video"])
# app.include_router(recovery.router, prefix="/api/recovery", tags=["Recovery"])
# app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])


# ── Health Check ────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "online",
        "app": "E-Waste AI API",
        "version": "2.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
