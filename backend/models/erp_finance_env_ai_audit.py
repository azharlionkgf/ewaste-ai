"""
E-Waste AI — Industrial ERP ORM Models: Modules 10, 13, 14 & 15
===============================================================
Module 10: Finance & Accounting (13 tables)
Module 13: Environmental & Compliance Records (7 new + reused `environmental_reports`)
Module 14: AI & Automation Database (7 new + reused `ai_predictions`)
Module 15: Reports, Documents & Audit (6 new + reused `generated_reports`, `audit_logs`)
"""

from __future__ import annotations

from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.models.erp_mixins import BranchScopedMixin, CompanyScopedMixin, ERPAuditMixin, erp_now, erp_uuid


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 10: FINANCE & ACCOUNTING (13 Tables)
# ══════════════════════════════════════════════════════════════════════════════

class FinancialPeriod(Base, CompanyScopedMixin):
    __tablename__ = "financial_periods"

    id                = Column(String, primary_key=True, default=erp_uuid)
    financial_year_id = Column(String, ForeignKey("financial_years.id"), nullable=False, index=True)
    period_name       = Column(String(64), nullable=False)
    start_date        = Column(Date, nullable=False)
    end_date          = Column(Date, nullable=False)
    is_closed         = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        CheckConstraint("end_date >= start_date", name="ck_fp_dates_valid"),
    )


class ChartOfAccount(Base, CompanyScopedMixin):
    __tablename__ = "chart_of_accounts"

    id                = Column(String, primary_key=True, default=erp_uuid)
    account_code      = Column(String(32), nullable=False)
    account_name      = Column(String(128), nullable=False)
    account_type      = Column(String(32), nullable=False, index=True)  # asset | liability | equity | revenue | expense
    parent_account_id = Column(String, ForeignKey("chart_of_accounts.id"), nullable=True)
    is_active         = Column(Boolean, default=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "account_code", name="uq_coa_code_per_company"),
    )


class AccountingVoucher(Base, BranchScopedMixin):
    __tablename__ = "accounting_vouchers"

    id                  = Column(String, primary_key=True, default=erp_uuid)
    financial_period_id = Column(String, ForeignKey("financial_periods.id"), nullable=True)
    voucher_number      = Column(String(64), nullable=False)
    voucher_type        = Column(String(32), nullable=False)  # journal | payment | receipt | contra
    voucher_date        = Column(Date, nullable=False, index=True)
    reference_type      = Column(String(64), nullable=True)
    reference_id        = Column(String, nullable=True)
    narration           = Column(Text, nullable=True)
    status              = Column(String(32), default="draft", nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "voucher_number", name="uq_voucher_per_company"),
    )


class JournalEntry(Base, BranchScopedMixin):
    """Double-entry ledger header enforcing total_debit == total_credit before posting."""
    __tablename__ = "journal_entries"

    id                   = Column(String, primary_key=True, default=erp_uuid)
    voucher_id           = Column(String, ForeignKey("accounting_vouchers.id"), nullable=True, index=True)
    financial_period_id  = Column(String, ForeignKey("financial_periods.id"), nullable=True)
    entry_number         = Column(String(64), nullable=False)
    entry_date           = Column(Date, nullable=False, index=True)
    description          = Column(Text, nullable=True)
    total_debit          = Column(Float, default=0.0, nullable=False)
    total_credit         = Column(Float, default=0.0, nullable=False)
    is_balanced          = Column(Boolean, default=True, nullable=False)
    is_posted            = Column(Boolean, default=False, nullable=False, index=True)
    is_audited_statement = Column(Boolean, default=False, nullable=False)  # Operational ERP ledger only; NOT audited FS

    lines = relationship("JournalEntryLine", back_populates="entry", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("company_id", "entry_number", name="uq_je_number_per_company"),
        CheckConstraint("total_debit >= 0", name="ck_je_debit_nonneg"),
        CheckConstraint("total_credit >= 0", name="ck_je_credit_nonneg"),
    )


class JournalEntryLine(Base, CompanyScopedMixin):
    __tablename__ = "journal_entry_lines"

    id               = Column(String, primary_key=True, default=erp_uuid)
    journal_entry_id = Column(String, ForeignKey("journal_entries.id"), nullable=False, index=True)
    account_id       = Column(String, ForeignKey("chart_of_accounts.id"), nullable=False, index=True)
    debit_amount     = Column(Float, default=0.0, nullable=False)
    credit_amount    = Column(Float, default=0.0, nullable=False)
    description      = Column(String(256), nullable=True)

    entry = relationship("JournalEntry", back_populates="lines")

    __table_args__ = (
        CheckConstraint("debit_amount >= 0", name="ck_jel_debit_nonneg"),
        CheckConstraint("credit_amount >= 0", name="ck_jel_credit_nonneg"),
    )


class ExpenseCategory(Base, CompanyScopedMixin):
    __tablename__ = "expense_categories"

    id            = Column(String, primary_key=True, default=erp_uuid)
    category_code = Column(String(64), nullable=False)
    category_name = Column(String(128), nullable=False)  # procurement | labour | electricity | transportation | machine_maintenance | processing | other
    account_id    = Column(String, ForeignKey("chart_of_accounts.id"), nullable=True)

    __table_args__ = (
        UniqueConstraint("company_id", "category_code", name="uq_exp_cat_per_company"),
    )


class Expense(Base, BranchScopedMixin):
    __tablename__ = "expenses"

    id                  = Column(String, primary_key=True, default=erp_uuid)
    expense_category_id = Column(String, ForeignKey("expense_categories.id"), nullable=False, index=True)
    incoming_batch_id   = Column(String, ForeignKey("incoming_batches.id"), nullable=True, index=True)
    journal_entry_id    = Column(String, ForeignKey("journal_entries.id"), nullable=True)
    expense_number      = Column(String(64), nullable=False)
    expense_date        = Column(Date, nullable=False, index=True)
    amount              = Column(Float, nullable=False)
    currency            = Column(String(8), default="USD", nullable=False)
    vendor_name         = Column(String(256), nullable=True)
    description         = Column(Text, nullable=True)
    status              = Column(String(32), default="recorded", nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "expense_number", name="uq_exp_num_per_company"),
        CheckConstraint("amount >= 0", name="ck_exp_amt_nonneg"),
    )


class IncomeRecord(Base, BranchScopedMixin):
    __tablename__ = "income_records"

    id               = Column(String, primary_key=True, default=erp_uuid)
    sales_order_id   = Column(String, ForeignKey("sales_orders.id"), nullable=True, index=True)
    journal_entry_id = Column(String, ForeignKey("journal_entries.id"), nullable=True)
    income_number    = Column(String(64), nullable=False)
    income_date      = Column(Date, nullable=False, index=True)
    source_type      = Column(String(64), default="material_sales", nullable=False)
    amount           = Column(Float, nullable=False)
    currency         = Column(String(8), default="USD", nullable=False)
    description      = Column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("company_id", "income_number", name="uq_inc_num_per_company"),
        CheckConstraint("amount >= 0", name="ck_inc_amt_nonneg"),
    )


class PurchasePayment(Base, BranchScopedMixin):
    __tablename__ = "purchase_payments"

    id                  = Column(String, primary_key=True, default=erp_uuid)
    supplier_id         = Column(String, ForeignKey("suppliers.id"), nullable=False, index=True)
    supplier_invoice_id = Column(String, ForeignKey("supplier_invoices.id"), nullable=True)
    journal_entry_id    = Column(String, ForeignKey("journal_entries.id"), nullable=True)
    payment_number      = Column(String(64), nullable=False)
    payment_date        = Column(Date, nullable=False, index=True)
    amount              = Column(Float, nullable=False)
    payment_mode        = Column(String(32), default="bank_transfer", nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "payment_number", name="uq_pp_num_per_company"),
        CheckConstraint("amount >= 0", name="ck_pp_amt_nonneg"),
    )


class SalesReceipt(Base, BranchScopedMixin):
    __tablename__ = "sales_receipts"

    id               = Column(String, primary_key=True, default=erp_uuid)
    customer_id      = Column(String, ForeignKey("customers.id"), nullable=False, index=True)
    sales_invoice_id = Column(String, ForeignKey("sales_invoices.id"), nullable=True)
    journal_entry_id = Column(String, ForeignKey("journal_entries.id"), nullable=True)
    receipt_number   = Column(String(64), nullable=False)
    receipt_date     = Column(Date, nullable=False, index=True)
    amount           = Column(Float, nullable=False)
    payment_mode     = Column(String(32), default="bank_transfer", nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "receipt_number", name="uq_sr_rcpt_per_company"),
        CheckConstraint("amount >= 0", name="ck_sr_amt_nonneg"),
    )


class TaxRecord(Base, BranchScopedMixin):
    __tablename__ = "tax_records"

    id             = Column(String, primary_key=True, default=erp_uuid)
    tax_type       = Column(String(64), nullable=False)
    tax_rate_pct   = Column(Float, default=0.0, nullable=False)
    taxable_amount = Column(Float, default=0.0, nullable=False)
    tax_amount     = Column(Float, default=0.0, nullable=False)
    reference_type = Column(String(64), nullable=True)
    reference_id   = Column(String, nullable=True)
    filing_period  = Column(String(32), nullable=True)


class BankTransaction(Base, BranchScopedMixin):
    __tablename__ = "bank_transactions"

    id                = Column(String, primary_key=True, default=erp_uuid)
    bank_account_name = Column(String(128), nullable=False)
    txn_date          = Column(Date, nullable=False, index=True)
    txn_type          = Column(String(16), nullable=False)  # debit | credit
    amount            = Column(Float, nullable=False)
    reference_no      = Column(String(64), nullable=True)
    reconciled        = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        CheckConstraint("amount >= 0", name="ck_bt_amt_nonneg"),
    )


class CashTransaction(Base, BranchScopedMixin):
    __tablename__ = "cash_transactions"

    id                     = Column(String, primary_key=True, default=erp_uuid)
    txn_date               = Column(Date, nullable=False, index=True)
    txn_type               = Column(String(16), nullable=False)  # receipt | payment
    amount                 = Column(Float, nullable=False)
    handled_by_employee_id = Column(String, ForeignKey("employees.id"), nullable=True)
    remarks                = Column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint("amount >= 0", name="ck_ct_amt_nonneg"),
    )


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 13: ENVIRONMENTAL & COMPLIANCE RECORDS (7 New + Reused `environmental_reports`)
# ══════════════════════════════════════════════════════════════════════════════

class AuthorizedRecyclerRecord(Base, CompanyScopedMixin):
    __tablename__ = "authorized_recycler_records"

    id                   = Column(String, primary_key=True, default=erp_uuid)
    recycler_name        = Column(String(256), nullable=False)
    authorization_number = Column(String(128), nullable=True)
    jurisdiction         = Column(String(128), nullable=True)
    material_scope       = Column(String(256), nullable=True)
    valid_until          = Column(Date, nullable=True)
    verification_status  = Column(String(32), default="recorded_unverified", nullable=False)
    notes                = Column(Text, nullable=True)


class HazardousWasteMovement(Base, BranchScopedMixin):
    __tablename__ = "hazardous_waste_movements"

    id                         = Column(String, primary_key=True, default=erp_uuid)
    incoming_batch_id          = Column(String, ForeignKey("incoming_batches.id"), nullable=False, index=True)
    hazardous_material_type_id = Column(String, ForeignKey("hazardous_material_types.id"), nullable=False, index=True)
    authorized_recycler_id     = Column(String, ForeignKey("authorized_recycler_records.id"), nullable=True)
    transport_order_id         = Column(String, ForeignKey("transport_orders.id"), nullable=True)
    manifest_number            = Column(String(64), nullable=False)
    movement_date              = Column(Date, nullable=False, index=True)
    quantity_kg                = Column(Float, nullable=False)
    status                     = Column(String(32), default="dispatched", nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "manifest_number", name="uq_hwm_manifest_per_company"),
        CheckConstraint("quantity_kg >= 0", name="ck_hwm_qty_nonneg"),
    )


class EnvironmentalMeasurement(Base, BranchScopedMixin):
    __tablename__ = "environmental_measurements"

    id                = Column(String, primary_key=True, default=erp_uuid)
    incoming_batch_id = Column(String, ForeignKey("incoming_batches.id"), nullable=True, index=True)
    measurement_type  = Column(String(64), nullable=False)
    metric_value      = Column(Float, nullable=False)
    unit              = Column(String(32), nullable=False)
    measured_at       = Column(DateTime, default=erp_now, nullable=False)
    methodology_note  = Column(Text, nullable=True)
    is_certified_lab  = Column(Boolean, default=False, nullable=False)


class WasteDisposalRecord(Base, BranchScopedMixin):
    __tablename__ = "waste_disposal_records"

    id                     = Column(String, primary_key=True, default=erp_uuid)
    incoming_batch_id      = Column(String, ForeignKey("incoming_batches.id"), nullable=True, index=True)
    authorized_recycler_id = Column(String, ForeignKey("authorized_recycler_records.id"), nullable=True)
    disposal_method        = Column(String(128), nullable=False)
    weight_kg              = Column(Float, nullable=False)
    disposal_date          = Column(Date, nullable=False)
    manifest_ref           = Column(String(128), nullable=True)

    __table_args__ = (
        CheckConstraint("weight_kg >= 0", name="ck_wdr_wt_nonneg"),
    )


class ComplianceDocument(Base, BranchScopedMixin):
    """Stores regulatory/compliance documentation records without auto-claiming legal certification."""
    __tablename__ = "compliance_documents"

    id                    = Column(String, primary_key=True, default=erp_uuid)
    document_code         = Column(String(64), nullable=False)
    compliance_category   = Column(String(128), nullable=False)
    jurisdiction_reference = Column(String(256), nullable=True)
    title                 = Column(String(256), nullable=False)
    file_path             = Column(String(512), nullable=True)
    verification_status   = Column(String(32), default="recorded_unverified", nullable=False)
    is_legal_certification = Column(Boolean, default=False, nullable=False)


class ComplianceObservation(Base, BranchScopedMixin):
    __tablename__ = "compliance_observations"

    id                = Column(String, primary_key=True, default=erp_uuid)
    observation_date  = Column(Date, nullable=False, index=True)
    category          = Column(String(128), nullable=False)
    severity          = Column(String(32), default="medium", nullable=False)
    description       = Column(Text, nullable=False)
    corrective_action = Column(Text, nullable=True)
    status            = Column(String(32), default="open", nullable=False)


class EnvironmentalAuditRecord(Base, BranchScopedMixin):
    __tablename__ = "environmental_audit_records"

    id                    = Column(String, primary_key=True, default=erp_uuid)
    audit_date            = Column(Date, nullable=False)
    auditor_name          = Column(String(128), nullable=True)
    scope                 = Column(String(256), nullable=False)
    findings              = Column(Text, nullable=True)
    is_certified_external = Column(Boolean, default=False, nullable=False)


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 14: AI & AUTOMATION DATABASE (7 New + Reused `ai_predictions`)
# ══════════════════════════════════════════════════════════════════════════════

class AIModelRegistry(Base, ERPAuditMixin):
    __tablename__ = "ai_models"

    id                 = Column(String, primary_key=True, default=erp_uuid)
    company_id         = Column(String, ForeignKey("companies.id"), nullable=True, index=True)
    legacy_ml_model_id = Column(String, ForeignKey("ml_models.id"), nullable=True)
    model_code         = Column(String(64), unique=True, nullable=False)
    model_name         = Column(String(256), nullable=False)
    task_type          = Column(String(64), nullable=False)
    framework          = Column(String(64), default="scikit-learn")
    is_active          = Column(Boolean, default=True, nullable=False)


class AIModelVersion(Base, ERPAuditMixin):
    __tablename__ = "ai_model_versions"

    id                  = Column(String, primary_key=True, default=erp_uuid)
    ai_model_id         = Column(String, ForeignKey("ai_models.id"), nullable=False, index=True)
    version_tag         = Column(String(32), nullable=False)
    artifact_path       = Column(String(512), nullable=True)
    training_dataset_ref = Column(String(256), nullable=True)
    metrics_json        = Column(JSON, nullable=True)
    is_production       = Column(Boolean, default=False, nullable=False)


class AIPredictionFeedback(Base, BranchScopedMixin):
    __tablename__ = "ai_prediction_feedback"

    id                     = Column(String, primary_key=True, default=erp_uuid)
    ai_prediction_id       = Column(String, ForeignKey("ai_predictions.id"), nullable=False, index=True)
    reviewer_employee_id   = Column(String, ForeignKey("employees.id"), nullable=True)
    is_accurate            = Column(Boolean, nullable=True)
    corrected_label        = Column(String(128), nullable=True)
    final_measured_outcome = Column(JSON, nullable=True)
    feedback_notes         = Column(Text, nullable=True)
    reviewed_at            = Column(DateTime, default=erp_now, nullable=False)


class RecoveryRecommendation(Base, BranchScopedMixin):
    __tablename__ = "recovery_recommendations"

    id                  = Column(String, primary_key=True, default=erp_uuid)
    incoming_batch_id   = Column(String, ForeignKey("incoming_batches.id"), nullable=False, index=True)
    ai_prediction_id    = Column(String, ForeignKey("ai_predictions.id"), nullable=True)
    recommended_process = Column(String(128), nullable=False)
    priority_materials  = Column(JSON, nullable=True)
    estimated_yield_kg  = Column(Float, nullable=True)
    confidence          = Column(Float, nullable=True)
    acceptance_status   = Column(String(32), default="pending", nullable=False)


class AnomalyRecord(Base, BranchScopedMixin):
    __tablename__ = "anomaly_records"

    id                      = Column(String, primary_key=True, default=erp_uuid)
    anomaly_type            = Column(String(64), nullable=False, index=True)
    severity                = Column(String(32), default="medium", nullable=False)
    entity_type             = Column(String(64), nullable=False)
    entity_id               = Column(String, nullable=True)
    description             = Column(Text, nullable=False)
    resolved                = Column(Boolean, default=False, nullable=False)
    resolved_by_employee_id = Column(String, ForeignKey("employees.id"), nullable=True)


class ForecastingResult(Base, BranchScopedMixin):
    __tablename__ = "forecasting_results"

    id               = Column(String, primary_key=True, default=erp_uuid)
    forecast_metric  = Column(String(128), nullable=False)
    horizon_days     = Column(Integer, default=30, nullable=False)
    predicted_value  = Column(Float, nullable=True)
    uncertainty_note = Column(Text, nullable=True)
    data_sufficient  = Column(Boolean, default=False, nullable=False)
    generated_at     = Column(DateTime, default=erp_now, nullable=False)


class AutomationJob(Base, BranchScopedMixin):
    __tablename__ = "automation_jobs"

    id           = Column(String, primary_key=True, default=erp_uuid)
    job_type     = Column(String(64), nullable=False)
    status       = Column(String(32), default="queued", nullable=False)
    triggered_by = Column(String(128), nullable=True)
    started_at   = Column(DateTime, nullable=True)
    finished_at  = Column(DateTime, nullable=True)
    summary_json = Column(JSON, nullable=True)


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 15: REPORTS, DOCUMENTS & AUDIT (6 New + Reused `generated_reports`, `audit_logs`)
# ══════════════════════════════════════════════════════════════════════════════

class DocumentRegistry(Base, BranchScopedMixin):
    __tablename__ = "document_registry"

    id                      = Column(String, primary_key=True, default=erp_uuid)
    module_name             = Column(String(64), nullable=False, index=True)
    entity_type             = Column(String(64), nullable=False)
    entity_id               = Column(String, nullable=False, index=True)
    title                   = Column(String(256), nullable=False)
    file_path               = Column(String(512), nullable=True)
    mime_type               = Column(String(128), nullable=True)
    checksum_sha256         = Column(String(64), nullable=True)
    uploaded_by_employee_id = Column(String, ForeignKey("employees.id"), nullable=True)


class ReportTemplate(Base, ERPAuditMixin):
    __tablename__ = "report_templates"

    id              = Column(String, primary_key=True, default=erp_uuid)
    company_id      = Column(String, ForeignKey("companies.id"), nullable=True, index=True)
    template_code   = Column(String(64), unique=True, nullable=False)
    template_name   = Column(String(256), nullable=False)
    report_category = Column(String(64), nullable=False)
    schema_json     = Column(JSON, nullable=True)
    is_active       = Column(Boolean, default=True, nullable=False)


class ActivityLog(Base, BranchScopedMixin):
    __tablename__ = "activity_logs"

    id                = Column(String, primary_key=True, default=erp_uuid)
    actor_user_id     = Column(String, ForeignKey("users.id"), nullable=True, index=True)
    actor_employee_id = Column(String, ForeignKey("employees.id"), nullable=True, index=True)
    activity_type     = Column(String(64), nullable=False)
    module_name       = Column(String(64), nullable=False, index=True)
    description       = Column(Text, nullable=False)
    metadata_json     = Column(JSON, nullable=True)
    occurred_at       = Column(DateTime, default=erp_now, nullable=False, index=True)


class NotificationRecord(Base, BranchScopedMixin):
    __tablename__ = "notification_records"

    id                    = Column(String, primary_key=True, default=erp_uuid)
    recipient_employee_id = Column(String, ForeignKey("employees.id"), nullable=True, index=True)
    category              = Column(String(64), nullable=False)
    severity              = Column(String(32), default="info", nullable=False)
    title                 = Column(String(256), nullable=False)
    message               = Column(Text, nullable=False)
    is_read               = Column(Boolean, default=False, nullable=False)


class ApprovalWorkflow(Base, CompanyScopedMixin):
    __tablename__ = "approval_workflows"

    id                   = Column(String, primary_key=True, default=erp_uuid)
    workflow_code        = Column(String(64), nullable=False)
    module_name          = Column(String(64), nullable=False)
    entity_type          = Column(String(64), nullable=False)
    required_role_code   = Column(String(64), nullable=False)
    min_amount_threshold = Column(Float, default=0.0, nullable=False)
    is_active            = Column(Boolean, default=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "workflow_code", name="uq_wf_code_per_company"),
    )


class ApprovalHistory(Base, BranchScopedMixin):
    __tablename__ = "approval_history"

    id                      = Column(String, primary_key=True, default=erp_uuid)
    workflow_id             = Column(String, ForeignKey("approval_workflows.id"), nullable=True)
    entity_type             = Column(String(64), nullable=False, index=True)
    entity_id               = Column(String, nullable=False, index=True)
    decision                = Column(String(32), nullable=False)  # approved | rejected | returned
    approved_by_employee_id = Column(String, ForeignKey("employees.id"), nullable=True)
    decision_at             = Column(DateTime, default=erp_now, nullable=False)
    comments                = Column(Text, nullable=True)
