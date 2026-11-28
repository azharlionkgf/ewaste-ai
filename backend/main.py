"""
E-Waste AI — FastAPI Backend Main Application (Phase 4 Complete)
================================================================
Run with: uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
API Docs: http://localhost:8000/docs
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os

from backend.config import API_VERSION, DEBUG, LOG_LEVEL, LOG_DIR
from backend.database import init_db, check_db_health

# ── Logging ────────────────────────────────────────────────────────────
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / "backend.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


# ── Lifespan ───────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("E-Waste AI Backend v4.0 starting up...")
    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully.")
    except Exception as exc:
        logger.error("Database initialization failed: %s", exc)

    # Check DB health
    if check_db_health():
        logger.info("Database health check: OK")
    else:
        logger.warning("Database health check: FAILED — running without DB")

    yield
    logger.info("E-Waste AI Backend shutting down.")


# ── App ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="E-Waste AI Industrial Intelligence API",
    description=(
        "## E-Waste AI — Combined Industrial Intelligence & Research Platform\n\n"
        "**Phase 4:** Full backend with AI model integration, industrial operations, "
        "material recovery intelligence, economic analysis, and research traceability.\n\n"
        "### Key Features\n"
        "- 🤖 AI Model Integration (actual trained models from Phase 3)\n"
        "- 🏭 Industrial Batch & Inventory Management\n"
        "- ♻️ Material Recovery Intelligence (rule-based estimates)\n"
        "- 💰 Economic Analysis Engine\n"
        "- 🌿 Environmental Impact Reporting\n"
        "- 🔒 JWT Authentication & Role-Based Authorization\n"
        "- 📊 Report Generation\n\n"
        "**GitHub:** https://github.com/azharlionkgf/ewaste-ai"
    ),
    version="4.0.0",
    contact={
        "name": "Adil",
        "url": "https://github.com/azharlionkgf/ewaste-ai",
        "email": "otihaladil8@gmail.com",
    },
    license_info={"name": "MIT"},
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ── CORS ───────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501",
        "https://ewaste-ai-cchoquyhxog2we3qbcyhlt.streamlit.app",
        "*",  # For development — restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Global Exception Handler ───────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled error: %s %s — %s", request.method, request.url, exc)
    # Never expose internal errors in production
    detail = str(exc) if DEBUG else "An internal error occurred."
    return JSONResponse(status_code=500, content={"success": False, "error": detail})


# ── Static Files ───────────────────────────────────────────────────────
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# ── Routers ────────────────────────────────────────────────────────────
from backend.routers.auth import router as auth_router
from backend.routers.batches import router as batch_router
from backend.routers.batches import recovery_router, inventory_router
from backend.routers.ai_inference import router as ai_router
from backend.routers.intelligence import (
    recovery_router as intel_recovery_router,
    economics_router,
    decision_router,
    environmental_router,
    reports_router,
)
from backend.routers.erp_routers import erp_router

app.include_router(auth_router)
app.include_router(batch_router)
app.include_router(recovery_router)
app.include_router(inventory_router)
app.include_router(ai_router)
app.include_router(intel_recovery_router)
app.include_router(economics_router)
app.include_router(decision_router)
app.include_router(environmental_router)
app.include_router(reports_router)
app.include_router(erp_router)

# ── Health ─────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "online",
        "app": "E-Waste AI Industrial Intelligence API",
        "version": "4.0.0",
        "phase": "Phase 4 — Backend Complete",
        "docs": "/docs",
        "github": "https://github.com/azharlionkgf/ewaste-ai",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    db_ok = check_db_health()
    return {
        "status": "healthy" if db_ok else "degraded",
        "database": "connected" if db_ok else "unavailable",
        "version": "4.0.0",
    }


@app.get(f"/api/{API_VERSION}/status", tags=["Health"])
async def api_status():
    """Full API status with available endpoints."""
    return {
        "api_version": API_VERSION,
        "phase": 4,
        "endpoints": {
            "auth": f"/api/{API_VERSION}/auth",
            "batches": f"/api/{API_VERSION}/batches",
            "recovery_records": f"/api/{API_VERSION}/recovery",
            "inventory": f"/api/{API_VERSION}/inventory",
            "ai_inference": f"/api/{API_VERSION}/ai",
            "recovery_intelligence": f"/api/{API_VERSION}/intelligence/recovery",
            "economics": f"/api/{API_VERSION}/intelligence/economics",
            "decisions": f"/api/{API_VERSION}/intelligence/decisions",
            "environmental": f"/api/{API_VERSION}/environmental",
            "reports": f"/api/{API_VERSION}/reports",
            "industrial_erp": f"/api/{API_VERSION}/erp",
        },
    }
