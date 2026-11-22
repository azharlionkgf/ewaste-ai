"""
E-Waste AI — SQLAlchemy Base Model
====================================
Provides a common mixin with created_at / updated_at timestamps
for all database models.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, func
from backend.database import Base


class TimestampMixin:
    """Adds created_at and updated_at columns to any model."""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow, nullable=False)
