"""
E-Waste AI — Application Configuration
=======================================
Environment-based configuration with sensible defaults.
Backwards-compatible: 'settings' object available via backend.config.settings
"""

import os
import secrets
from pathlib import Path

# ── Project Root ───────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).parent.parent

# ── Environment ────────────────────────────────────────────────────────
ENV = os.getenv("EWASTE_ENV", "development")
DEBUG = ENV == "development"

# ── Database ───────────────────────────────────────────────────────────
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{ROOT_DIR}/database/ewaste_ai.db")

# ── Security ───────────────────────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

# ── File Uploads ───────────────────────────────────────────────────────
UPLOAD_DIR = ROOT_DIR / "data" / "uploads"
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50"))
MAX_UPLOAD_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
ALLOWED_DATA_TYPES = {
    "text/csv",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/json",
}

# ── Model Registry ─────────────────────────────────────────────────────
MODEL_REGISTRY_DIR = ROOT_DIR / "models" / "registry"
SAVED_MODELS_DIR = ROOT_DIR / "saved_models"

# ── Reports ────────────────────────────────────────────────────────────
REPORTS_DIR = ROOT_DIR / "reports"

# ── Logging ────────────────────────────────────────────────────────────
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = ROOT_DIR / "logs"

# ── API ────────────────────────────────────────────────────────────────
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# ── Rate Limiting ──────────────────────────────────────────────────────
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))

# ── Ensure directories exist ───────────────────────────────────────────
for d in [UPLOAD_DIR, MODEL_REGISTRY_DIR, SAVED_MODELS_DIR, REPORTS_DIR, LOG_DIR]:
    d.mkdir(parents=True, exist_ok=True)


# ── Backwards-compatible settings object (Phase 1 API) ────────────────
class _Settings:
    """Provides object-style access for older code using 'from backend.config import settings'."""
    # Uppercase (Phase 1 API)
    APP_NAME: str = "E-Waste AI"
    DATABASE_URL: str = DATABASE_URL
    SECRET_KEY: str = SECRET_KEY
    ALGORITHM: str = ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES: int = ACCESS_TOKEN_EXPIRE_MINUTES
    UPLOAD_DIR = UPLOAD_DIR
    LOG_LEVEL: str = LOG_LEVEL
    DEBUG: bool = DEBUG
    ENVIRONMENT: str = ENV
    DEFAULT_SEED: int = 42
    TRAIN_SPLIT: float = 0.8
    VAL_SPLIT: float = 0.1
    TEST_SPLIT: float = 0.1
    # Lowercase (also supported)
    database_url: str = DATABASE_URL
    secret_key: str = SECRET_KEY
    algorithm: str = ALGORITHM
    access_token_expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES
    upload_dir = UPLOAD_DIR
    log_level: str = LOG_LEVEL
    debug: bool = DEBUG
    environment: str = ENV


settings = _Settings()
