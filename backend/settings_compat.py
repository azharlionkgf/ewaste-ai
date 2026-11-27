"""
Backwards-compatible 'settings' object for Phase 1 tests.
Phase 4 config uses module-level constants; this provides the old API.
"""
from backend.config import (
    DATABASE_URL, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES,
    UPLOAD_DIR, LOG_LEVEL, DEBUG, ENV,
)


class _Settings:
    database_url: str = DATABASE_URL
    secret_key: str = SECRET_KEY
    algorithm: str = ALGORITHM
    access_token_expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES
    upload_dir = UPLOAD_DIR
    log_level: str = LOG_LEVEL
    debug: bool = DEBUG
    environment: str = ENV


settings = _Settings()
