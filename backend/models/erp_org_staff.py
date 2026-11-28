"""
E-Waste AI — Industrial ERP ORM Models: Modules 1 & 2
=====================================================
Module 1: Company Management (10 tables)
Module 2: Employee & Staff Management (9 tables)
"""

from __future__ import annotations

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.models.erp_mixins import (
    BranchScopedMixin,
    CompanyScopedMixin,
    ERPAuditMixin,
    erp_now,
    erp_uuid,
)


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 1: COMPANY MANAGEMENT (10 Tables)
# ══════════════════════════════════════════════════════════════════════════════

class Company(Base, ERPAuditMixin):
    __tablename__ = "companies"

    id                  = Column(String, primary_key=True, default=erp_uuid)
    company_code        = Column(String(64), unique=True, nullable=False, index=True)
    legal_name          = Column(String(256), nullable=False)
    trade_name          = Column(String(256), nullable=True)
    registration_number = Column(String(128), nullable=True)
    tax_id              = Column(String(128), nullable=True)
    industry_type       = Column(String(128), default="e_waste_recycling")
    base_currency       = Column(String(8), default="USD", nullable=False)
    is_active           = Column(Boolean, default=True, nullable=False, index=True)

    branches        = relationship("CompanyBranch", back_populates="company", cascade="all, delete-orphan")
    financial_years = relationship("FinancialYear", back_populates="company", cascade="all, delete-orphan")


class CompanyBranch(Base, CompanyScopedMixin):
    __tablename__ = "company_branches"

    id             = Column(String, primary_key=True, default=erp_uuid)
    branch_code    = Column(String(64), nullable=False)
    branch_name    = Column(String(256), nullable=False)
    branch_type    = Column(String(64), default="recycling_plant")  # hq | recycling_plant | collection_center | warehouse
    is_head_office = Column(Boolean, default=False, nullable=False)
    is_active      = Column(Boolean, default=True, nullable=False, index=True)

    company     = relationship("Company", back_populates="branches")
    departments = relationship("Department", back_populates="branch", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("company_id", "branch_code", name="uq_branch_code_per_company"),
        Index("ix_branches_company_active", "company_id", "is_active"),
    )


class Department(Base, BranchScopedMixin):
    __tablename__ = "departments"

    id          = Column(String, primary_key=True, default=erp_uuid)
    dept_code   = Column(String(64), nullable=False)
    dept_name   = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    is_active   = Column(Boolean, default=True, nullable=False)

    branch = relationship("CompanyBranch", back_populates="departments")

    __table_args__ = (
        UniqueConstraint("company_id", "branch_id", "dept_code", name="uq_dept_code_per_branch"),
    )


class BusinessUnit(Base, BranchScopedMixin):
    __tablename__ = "business_units"

    id        = Column(String, primary_key=True, default=erp_uuid)
    unit_code = Column(String(64), nullable=False)
    unit_name = Column(String(256), nullable=False)
    unit_type = Column(String(64), default="operations")
    is_active = Column(Boolean, default=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "unit_code", name="uq_bu_code_per_company"),
    )


class CompanyAddress(Base, BranchScopedMixin):
    __tablename__ = "company_addresses"

    id           = Column(String, primary_key=True, default=erp_uuid)
    address_type = Column(String(64), default="registered")  # registered | plant | warehouse | billing
    line1        = Column(String(256), nullable=False)
    line2        = Column(String(256), nullable=True)
    city         = Column(String(128), nullable=False)
    state        = Column(String(128), nullable=True)
    postal_code  = Column(String(32), nullable=True)
    country      = Column(String(128), nullable=False)
    is_primary   = Column(Boolean, default=False, nullable=False)


class CompanyContact(Base, BranchScopedMixin):
    __tablename__ = "company_contacts"

    id           = Column(String, primary_key=True, default=erp_uuid)
    contact_name = Column(String(256), nullable=False)
    designation  = Column(String(128), nullable=True)
    email        = Column(String(256), nullable=True)
    phone        = Column(String(64), nullable=True)
    is_primary   = Column(Boolean, default=False, nullable=False)


class CompanyDocument(Base, BranchScopedMixin):
    __tablename__ = "company_documents"

    id              = Column(String, primary_key=True, default=erp_uuid)
    document_type   = Column(String(64), nullable=False)
    title           = Column(String(256), nullable=False)
    file_path       = Column(String(512), nullable=True)
    checksum_sha256 = Column(String(64), nullable=True)
    issued_date     = Column(Date, nullable=True)
    expiry_date     = Column(Date, nullable=True)


class CompanyLicense(Base, BranchScopedMixin):
    __tablename__ = "company_licenses"

    id                  = Column(String, primary_key=True, default=erp_uuid)
    license_number      = Column(String(128), nullable=False)
    license_type        = Column(String(128), nullable=False)
    issuing_authority   = Column(String(256), nullable=True)
    jurisdiction        = Column(String(128), nullable=True)
    valid_from          = Column(Date, nullable=True)
    valid_until         = Column(Date, nullable=True)
    verification_status = Column(String(32), default="recorded_unverified", nullable=False)
    notes               = Column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("company_id", "license_number", name="uq_company_license_number"),
    )


class CompanySetting(Base, BranchScopedMixin):
    __tablename__ = "company_settings"

    id            = Column(String, primary_key=True, default=erp_uuid)
    setting_key   = Column(String(128), nullable=False)
    setting_value = Column(JSON, nullable=True)
    scope         = Column(String(32), default="company")

    __table_args__ = (
        UniqueConstraint("company_id", "setting_key", name="uq_company_setting_key"),
    )


class FinancialYear(Base, CompanyScopedMixin):
    __tablename__ = "financial_years"

    id         = Column(String, primary_key=True, default=erp_uuid)
    year_code  = Column(String(32), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date   = Column(Date, nullable=False)
    is_closed  = Column(Boolean, default=False, nullable=False)
    is_current = Column(Boolean, default=True, nullable=False)

    company = relationship("Company", back_populates="financial_years")

    __table_args__ = (
        UniqueConstraint("company_id", "year_code", name="uq_fy_code_per_company"),
        CheckConstraint("end_date >= start_date", name="ck_fy_dates_valid"),
    )


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 2: EMPLOYEE & STAFF MANAGEMENT (9 Tables)
# ══════════════════════════════════════════════════════════════════════════════

class EmployeeDesignation(Base, CompanyScopedMixin):
    __tablename__ = "employee_designations"

    id          = Column(String, primary_key=True, default=erp_uuid)
    title       = Column(String(128), nullable=False)
    grade_level = Column(String(32), nullable=True)
    description = Column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("company_id", "title", name="uq_designation_per_company"),
    )


class EmployeeRole(Base, CompanyScopedMixin):
    __tablename__ = "employee_roles"

    id                      = Column(String, primary_key=True, default=erp_uuid)
    role_code               = Column(String(64), nullable=False)
    role_name               = Column(String(128), nullable=False)
    description             = Column(Text, nullable=True)
    is_financial_restricted = Column(Boolean, default=False, nullable=False)
    is_admin_role           = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "role_code", name="uq_role_code_per_company"),
    )


class EmployeeShift(Base, BranchScopedMixin):
    __tablename__ = "employee_shifts"

    id         = Column(String, primary_key=True, default=erp_uuid)
    shift_name = Column(String(64), nullable=False)
    start_time = Column(String(16), nullable=False)  # HH:MM
    end_time   = Column(String(16), nullable=False)  # HH:MM


class Employee(Base, BranchScopedMixin):
    __tablename__ = "employees"

    id                    = Column(String, primary_key=True, default=erp_uuid)
    user_id               = Column(String, ForeignKey("users.id"), nullable=True, index=True)
    employee_code         = Column(String(64), nullable=False)
    full_name             = Column(String(256), nullable=False)
    email                 = Column(String(256), nullable=True)
    phone                 = Column(String(64), nullable=True)
    department_id         = Column(String, ForeignKey("departments.id"), nullable=True, index=True)
    designation_id        = Column(String, ForeignKey("employee_designations.id"), nullable=True)
    role_id               = Column(String, ForeignKey("employee_roles.id"), nullable=True, index=True)
    shift_id              = Column(String, ForeignKey("employee_shifts.id"), nullable=True)
    joining_date          = Column(Date, nullable=False)
    is_active             = Column(Boolean, default=True, nullable=False, index=True)
    authorized_operations = Column(JSON, nullable=True)

    role        = relationship("EmployeeRole")
    department  = relationship("Department")
    designation = relationship("EmployeeDesignation")

    __table_args__ = (
        UniqueConstraint("company_id", "employee_code", name="uq_employee_code_per_company"),
        Index("ix_employees_company_branch", "company_id", "branch_id"),
    )


class EmployeeDepartment(Base, BranchScopedMixin):
    """Tracks employee department assignments and transfers across time."""
    __tablename__ = "employee_departments"

    id             = Column(String, primary_key=True, default=erp_uuid)
    employee_id    = Column(String, ForeignKey("employees.id"), nullable=False, index=True)
    department_id  = Column(String, ForeignKey("departments.id"), nullable=False, index=True)
    effective_from = Column(Date, nullable=False)
    effective_to   = Column(Date, nullable=True)
    is_primary     = Column(Boolean, default=True, nullable=False)


class EmployeeAttendance(Base, BranchScopedMixin):
    __tablename__ = "employee_attendance"

    id              = Column(String, primary_key=True, default=erp_uuid)
    employee_id     = Column(String, ForeignKey("employees.id"), nullable=False, index=True)
    shift_id        = Column(String, ForeignKey("employee_shifts.id"), nullable=True)
    attendance_date = Column(Date, nullable=False, index=True)
    check_in        = Column(DateTime, nullable=True)
    check_out       = Column(DateTime, nullable=True)
    status          = Column(String(32), default="present", nullable=False)  # present | absent | leave | half_day


class EmployeeTrainingRecord(Base, BranchScopedMixin):
    __tablename__ = "employee_training_records"

    id              = Column(String, primary_key=True, default=erp_uuid)
    employee_id     = Column(String, ForeignKey("employees.id"), nullable=False, index=True)
    training_topic  = Column(String(256), nullable=False)
    safety_category = Column(String(64), default="general")  # hazmat | machine_safety | compliance | general
    completed_date  = Column(Date, nullable=True)
    valid_until     = Column(Date, nullable=True)
    trainer_name    = Column(String(128), nullable=True)
    status          = Column(String(32), default="completed", nullable=False)


class EmployeePermission(Base, CompanyScopedMixin):
    __tablename__ = "employee_permissions"

    id                = Column(String, primary_key=True, default=erp_uuid)
    role_id           = Column(String, ForeignKey("employee_roles.id"), nullable=True, index=True)
    employee_id       = Column(String, ForeignKey("employees.id"), nullable=True, index=True)
    permission_key    = Column(String(128), nullable=False, index=True)
    resource_scope    = Column(String(64), default="branch")  # company | branch | own
    branch_restricted = Column(Boolean, default=True, nullable=False)
    is_granted        = Column(Boolean, default=True, nullable=False)


class EmployeeActivityLog(Base, BranchScopedMixin):
    __tablename__ = "employee_activity_logs"

    id            = Column(String, primary_key=True, default=erp_uuid)
    employee_id   = Column(String, ForeignKey("employees.id"), nullable=False, index=True)
    action        = Column(String(128), nullable=False)
    module        = Column(String(64), nullable=False, index=True)
    resource_type = Column(String(64), nullable=True)
    resource_id   = Column(String, nullable=True)
    details       = Column(JSON, nullable=True)
    occurred_at   = Column(DateTime, default=erp_now, nullable=False, index=True)
