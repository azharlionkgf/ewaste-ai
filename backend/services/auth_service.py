"""
E-Waste AI — Authentication & Security Service (Phase 4 Task 11)
=================================================================
JWT-based authentication, password hashing, role-based authorization.
"""

from __future__ import annotations

import hashlib
import logging
import secrets
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

logger = logging.getLogger(__name__)

# ── Password Hashing ───────────────────────────────────────────────────
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    return _pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return _pwd_context.verify(plain, hashed)


# ── JWT Tokens ─────────────────────────────────────────────────────────

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as exc:
        logger.warning("Token decode failed: %s", exc)
        return None


# ── File Hashing ───────────────────────────────────────────────────────

def hash_file_content(content: bytes) -> str:
    """SHA-256 hash of file content for provenance tracking."""
    return hashlib.sha256(content).hexdigest()


# ── Input Sanitization ─────────────────────────────────────────────────

def sanitize_filename(filename: str) -> str:
    """Remove unsafe characters and path traversal sequences from filenames."""
    # Remove path separators and dots at the start (prevent ../.. traversal)
    basename = filename.replace("\\", "/").split("/")[-1]
    # Remove leading dots
    basename = basename.lstrip(".")
    # Keep only safe characters
    safe = "".join(c for c in basename if c.isalnum() or c in "._- ")
    return safe[:255] or "unnamed_file"


# ── Roles ──────────────────────────────────────────────────────────────

ROLE_PERMISSIONS: dict[str, set[str]] = {
    "admin": {
        "read", "write", "delete", "manage_users", "manage_models",
        "view_reports", "generate_reports", "configure_prices",
    },
    "manager": {
        "read", "write", "manage_models", "view_reports",
        "generate_reports", "configure_prices",
    },
    "operator": {"read", "write", "view_reports"},
    "researcher": {"read", "write", "manage_models", "view_reports", "generate_reports"},
}


def has_permission(role: str, permission: str) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, set())


# ── Rate Limiting (simple in-memory, production use Redis) ─────────────

_rate_store: dict[str, list] = {}


def check_rate_limit(identifier: str, max_requests: int = 100, window_sec: int = 60) -> bool:
    """Return True if within rate limit, False if exceeded."""
    now = datetime.utcnow().timestamp()
    cutoff = now - window_sec
    history = _rate_store.get(identifier, [])
    history = [t for t in history if t > cutoff]
    history.append(now)
    _rate_store[identifier] = history
    return len(history) <= max_requests
