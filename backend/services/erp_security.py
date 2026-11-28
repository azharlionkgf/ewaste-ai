"""
E-Waste AI — ERP Role-Based Security, Company/Branch Isolation & Audit Service
==============================================================================
Enforces multi-company isolation, branch access restrictions, financial/admin
RBAC guards, and mandatory audit trail logging on all ERP mutations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.all_models import AuditLog, User
from backend.models.erp_org_staff import (
    Employee,
    EmployeeActivityLog,
    EmployeePermission,
    EmployeeRole,
)
from backend.routers.auth import oauth2_scheme
from backend.services.auth_service import decode_access_token


ERP_ROLE_DEFAULT_PERMS: dict[str, set[str]] = {
    "admin": {
        "company:read", "company:write", "employee:read", "employee:write",
        "procurement:read", "procurement:write", "sales:read", "sales:write",
        "batch:read", "batch:write", "processing:read", "processing:write",
        "recovery:read", "recovery:write", "warehouse:read", "warehouse:write",
        "finance:read", "finance:write", "logistics:read", "logistics:write",
        "machine:read", "machine:write", "compliance:read", "compliance:write",
        "ai:read", "ai:write", "reports:read", "admin:access",
    },
    "finance_manager": {
        "company:read", "procurement:read", "procurement:write", "sales:read", "sales:write",
        "warehouse:read", "finance:read", "finance:write", "reports:read",
    },
    "manager": {
        "company:read", "employee:read", "procurement:read", "procurement:write",
        "sales:read", "sales:write", "batch:read", "batch:write",
        "processing:read", "processing:write", "recovery:read", "recovery:write",
        "warehouse:read", "warehouse:write", "logistics:read", "logistics:write",
        "machine:read", "machine:write", "compliance:read", "compliance:write",
        "ai:read", "ai:write", "reports:read",
    },
    "operator": {
        "company:read", "batch:read", "batch:write", "processing:read", "processing:write",
        "recovery:read", "recovery:write", "warehouse:read", "machine:read",
        "logistics:read", "compliance:read", "ai:read", "reports:read",
    },
    "researcher": {
        "company:read", "batch:read", "recovery:read", "compliance:read",
        "ai:read", "ai:write", "reports:read",
    },
}


@dataclass
class ERPSecurityContext:
    user_id: str
    username: str
    user_role: str
    company_id: Optional[str] = None
    branch_id: Optional[str] = None
    employee_id: Optional[str] = None
    is_admin: bool = False
    is_financial_authorized: bool = False
    permissions: set[str] = field(default_factory=set)
    branch_restricted: bool = False


def build_security_context(db: Session, user: User) -> ERPSecurityContext:
    """Resolve User + linked Employee + Role + explicit EmployeePermission rows."""
    role_key = (user.role or "operator").lower()
    perms = set(ERP_ROLE_DEFAULT_PERMS.get(role_key, ERP_ROLE_DEFAULT_PERMS["operator"]))
    is_admin = role_key == "admin"
    is_fin = role_key in {"admin", "finance_manager"}

    emp = (
        db.query(Employee)
        .filter(Employee.user_id == user.id, Employee.is_deleted == False)  # noqa: E712
        .first()
    )
    company_id = emp.company_id if emp else None
    branch_id = emp.branch_id if emp else None
    employee_id = emp.id if emp else None
    branch_restricted = False

    if emp and emp.role_id:
        erole = db.query(EmployeeRole).filter(EmployeeRole.id == emp.role_id).first()
        if erole:
            if erole.is_admin_role:
                is_admin = True
                perms |= ERP_ROLE_DEFAULT_PERMS["admin"]
            if erole.is_financial_restricted:
                # Role marks employee eligible for financial module if granted
                is_fin = True
        role_perms = (
            db.query(EmployeePermission)
            .filter(EmployeePermission.role_id == emp.role_id, EmployeePermission.is_deleted == False)  # noqa: E712
            .all()
        )
        for rp in role_perms:
            if rp.is_granted:
                perms.add(rp.permission_key)
                if rp.branch_restricted:
                    branch_restricted = True
            else:
                perms.discard(rp.permission_key)

    if emp:
        emp_perms = (
            db.query(EmployeePermission)
            .filter(EmployeePermission.employee_id == emp.id, EmployeePermission.is_deleted == False)  # noqa: E712
            .all()
        )
        for ep in emp_perms:
            if ep.is_granted:
                perms.add(ep.permission_key)
                if ep.branch_restricted:
                    branch_restricted = True
            else:
                perms.discard(ep.permission_key)

    if "finance:read" in perms or "finance:write" in perms:
        is_fin = is_fin or role_key in {"admin", "finance_manager"}

    return ERPSecurityContext(
        user_id=user.id,
        username=user.username,
        user_role=role_key,
        company_id=company_id,
        branch_id=branch_id,
        employee_id=employee_id,
        is_admin=is_admin,
        is_financial_authorized=is_fin,
        permissions=perms,
        branch_restricted=branch_restricted and not is_admin,
    )


def get_erp_context(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> ERPSecurityContext:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")
    return build_security_context(db, user)


def require_erp_permission(permission: str, financial: bool = False, admin_only: bool = False):
    """FastAPI dependency enforcing RBAC, financial restriction, and admin restriction."""

    def _checker(ctx: ERPSecurityContext = Depends(get_erp_context)) -> ERPSecurityContext:
        if admin_only and not ctx.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Administrator role required")
        if financial and not (ctx.is_admin or ctx.is_financial_authorized):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Financial permission restricted — authorized finance/admin role required",
            )
        if not ctx.is_admin and permission not in ctx.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permission: {permission}",
            )
        return ctx

    return _checker


def enforce_company_branch_scope(
    ctx: ERPSecurityContext,
    target_company_id: str,
    target_branch_id: Optional[str] = None,
) -> None:
    """Block unauthorized cross-company or branch-restricted data access."""
    if ctx.is_admin and ctx.company_id is None:
        return  # Platform super-admin without company lock
    if ctx.company_id and ctx.company_id != target_company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cross-company data access is prohibited",
        )
    if (
        ctx.branch_restricted
        and ctx.branch_id
        and target_branch_id
        and ctx.branch_id != target_branch_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cross-branch data access restricted for your role",
        )


def record_erp_audit(
    db: Session,
    action: str,
    module: str,
    resource: str,
    resource_id: Optional[str],
    company_id: Optional[str] = None,
    branch_id: Optional[str] = None,
    user_id: Optional[str] = None,
    employee_id: Optional[str] = None,
    details: Optional[dict[str, Any]] = None,
    before_state: Optional[dict[str, Any]] = None,
    after_state: Optional[dict[str, Any]] = None,
) -> None:
    """Persist unified AuditLog and optional EmployeeActivityLog within active transaction."""
    audit = AuditLog(
        user_id=user_id,
        company_id=company_id,
        branch_id=branch_id,
        employee_id=employee_id,
        module=module,
        action=action,
        resource=resource,
        resource_id=str(resource_id) if resource_id is not None else None,
        details=details or {},
        before_state=before_state,
        after_state=after_state,
        status="success",
        created_at=datetime.utcnow(),
    )
    db.add(audit)

    if employee_id and company_id:
        emp_log = EmployeeActivityLog(
            company_id=company_id,
            branch_id=branch_id,
            employee_id=employee_id,
            action=action,
            module=module,
            resource_type=resource,
            resource_id=str(resource_id) if resource_id is not None else None,
            details=details or {},
            occurred_at=datetime.utcnow(),
        )
        db.add(emp_log)
