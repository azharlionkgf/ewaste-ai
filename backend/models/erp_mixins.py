"""
E-Waste AI — Industrial ERP ORM Mixins & Common Helpers
========================================================
Shared UUID primary keys, audit timestamps, soft-delete columns, and
multi-company / multi-branch ownership foreign keys.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import declared_attr


def erp_uuid() -> str:
    return str(uuid.uuid4())


def erp_now() -> datetime:
    return datetime.utcnow()


class ERPAuditMixin:
    """Standard created/updated timestamps, actor references, and soft deletion."""

    created_at = Column(DateTime, default=erp_now, nullable=False, index=True)
    updated_at = Column(DateTime, default=erp_now, onupdate=erp_now, nullable=False)
    created_by = Column(String(128), nullable=True)
    updated_by = Column(String(128), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    deleted_at = Column(DateTime, nullable=True)


class CompanyScopedMixin(ERPAuditMixin):
    """Multi-company ownership enforcement."""

    @declared_attr
    def company_id(cls):
        return Column(String, ForeignKey("companies.id"), nullable=False, index=True)


class BranchScopedMixin(CompanyScopedMixin):
    """Multi-company and multi-branch ownership enforcement."""

    @declared_attr
    def branch_id(cls):
        return Column(String, ForeignKey("company_branches.id"), nullable=True, index=True)
