"""
E-Waste AI — Industrial ERP ORM Models: Modules 3 & 4
=====================================================
Module 3: Supplier & E-Waste Procurement (9 tables)
Module 4: Customer & Sales Management (9 tables)
"""

from __future__ import annotations

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.models.erp_mixins import BranchScopedMixin, CompanyScopedMixin, erp_uuid


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 3: SUPPLIER & E-WASTE PROCUREMENT (9 Tables)
# ══════════════════════════════════════════════════════════════════════════════

class Supplier(Base, BranchScopedMixin):
    __tablename__ = "suppliers"

    id                  = Column(String, primary_key=True, default=erp_uuid)
    supplier_code       = Column(String(64), nullable=False)
    name                = Column(String(256), nullable=False)
    supplier_type       = Column(String(64), default="corporate")  # corporate | municipality | aggregator | individual
    registration_number = Column(String(128), nullable=True)
    tax_id              = Column(String(128), nullable=True)
    rating              = Column(Float, default=0.0)
    is_active           = Column(Boolean, default=True, nullable=False, index=True)

    contacts = relationship("SupplierContact", back_populates="supplier", cascade="all, delete-orphan")
    orders   = relationship("ProcurementOrder", back_populates="supplier")

    __table_args__ = (
        UniqueConstraint("company_id", "supplier_code", name="uq_supplier_code_per_company"),
        Index("ix_suppliers_company_name", "company_id", "name"),
    )


class SupplierContact(Base, CompanyScopedMixin):
    __tablename__ = "supplier_contacts"

    id           = Column(String, primary_key=True, default=erp_uuid)
    supplier_id  = Column(String, ForeignKey("suppliers.id"), nullable=False, index=True)
    contact_name = Column(String(256), nullable=False)
    role         = Column(String(128), nullable=True)
    email        = Column(String(256), nullable=True)
    phone        = Column(String(64), nullable=True)
    is_primary   = Column(Boolean, default=False, nullable=False)

    supplier = relationship("Supplier", back_populates="contacts")


class SupplierDocument(Base, CompanyScopedMixin):
    __tablename__ = "supplier_documents"

    id              = Column(String, primary_key=True, default=erp_uuid)
    supplier_id     = Column(String, ForeignKey("suppliers.id"), nullable=False, index=True)
    document_type   = Column(String(64), nullable=False)
    document_number = Column(String(128), nullable=True)
    file_path       = Column(String(512), nullable=True)
    valid_until     = Column(Date, nullable=True)


class SupplierMaterialCategory(Base, CompanyScopedMixin):
    __tablename__ = "supplier_material_categories"

    id              = Column(String, primary_key=True, default=erp_uuid)
    supplier_id     = Column(String, ForeignKey("suppliers.id"), nullable=False, index=True)
    ewaste_category = Column(String(128), nullable=False)
    typical_grade   = Column(String(64), nullable=True)
    is_authorized   = Column(Boolean, default=True, nullable=False)


class ProcurementOrder(Base, BranchScopedMixin):
    __tablename__ = "procurement_orders"

    id                      = Column(String, primary_key=True, default=erp_uuid)
    supplier_id             = Column(String, ForeignKey("suppliers.id"), nullable=False, index=True)
    po_number               = Column(String(64), nullable=False)
    order_date              = Column(Date, nullable=False, index=True)
    expected_delivery_date  = Column(Date, nullable=True)
    ewaste_category         = Column(String(128), nullable=False)
    total_quantity          = Column(Float, default=0.0, nullable=False)
    total_weight_kg         = Column(Float, default=0.0, nullable=False)
    purchase_price_total    = Column(Float, default=0.0, nullable=False)
    transportation_cost     = Column(Float, default=0.0, nullable=False)
    currency                = Column(String(8), default="USD", nullable=False)
    status                  = Column(String(32), default="draft", nullable=False, index=True)
    approved_by_employee_id = Column(String, ForeignKey("employees.id"), nullable=True)
    notes                   = Column(Text, nullable=True)

    supplier = relationship("Supplier", back_populates="orders")
    items    = relationship("ProcurementOrderItem", back_populates="order", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("company_id", "po_number", name="uq_po_number_per_company"),
        CheckConstraint("total_quantity >= 0", name="ck_po_qty_nonneg"),
        CheckConstraint("total_weight_kg >= 0", name="ck_po_weight_nonneg"),
        CheckConstraint("purchase_price_total >= 0", name="ck_po_price_nonneg"),
        CheckConstraint("transportation_cost >= 0", name="ck_po_transport_nonneg"),
    )


class ProcurementOrderItem(Base, CompanyScopedMixin):
    __tablename__ = "procurement_order_items"

    id                   = Column(String, primary_key=True, default=erp_uuid)
    procurement_order_id = Column(String, ForeignKey("procurement_orders.id"), nullable=False, index=True)
    ewaste_category      = Column(String(128), nullable=False)
    item_description     = Column(String(256), nullable=True)
    quantity             = Column(Float, default=0.0, nullable=False)
    weight_kg            = Column(Float, default=0.0, nullable=False)
    unit_price           = Column(Float, default=0.0, nullable=False)
    line_total           = Column(Float, default=0.0, nullable=False)

    order = relationship("ProcurementOrder", back_populates="items")

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="ck_poi_qty_nonneg"),
        CheckConstraint("weight_kg >= 0", name="ck_poi_wt_nonneg"),
    )


class SupplierInvoice(Base, BranchScopedMixin):
    __tablename__ = "supplier_invoices"

    id                   = Column(String, primary_key=True, default=erp_uuid)
    supplier_id          = Column(String, ForeignKey("suppliers.id"), nullable=False, index=True)
    procurement_order_id = Column(String, ForeignKey("procurement_orders.id"), nullable=True, index=True)
    invoice_number       = Column(String(64), nullable=False)
    invoice_date         = Column(Date, nullable=False)
    due_date             = Column(Date, nullable=True)
    subtotal_amount      = Column(Float, default=0.0, nullable=False)
    tax_amount           = Column(Float, default=0.0, nullable=False)
    total_amount         = Column(Float, default=0.0, nullable=False)
    paid_amount          = Column(Float, default=0.0, nullable=False)
    payment_status       = Column(String(32), default="unpaid", nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("company_id", "invoice_number", name="uq_sup_inv_per_company"),
        CheckConstraint("total_amount >= 0", name="ck_sup_inv_total_nonneg"),
        CheckConstraint("paid_amount >= 0", name="ck_sup_inv_paid_nonneg"),
    )


class SupplierPayment(Base, BranchScopedMixin):
    __tablename__ = "supplier_payments"

    id                  = Column(String, primary_key=True, default=erp_uuid)
    supplier_id         = Column(String, ForeignKey("suppliers.id"), nullable=False, index=True)
    supplier_invoice_id = Column(String, ForeignKey("supplier_invoices.id"), nullable=True, index=True)
    payment_reference   = Column(String(64), nullable=False)
    payment_date        = Column(Date, nullable=False)
    amount              = Column(Float, nullable=False)
    payment_method      = Column(String(32), default="bank_transfer", nullable=False)
    status              = Column(String(32), default="completed", nullable=False)

    __table_args__ = (
        CheckConstraint("amount >= 0", name="ck_sup_pay_nonneg"),
    )


class PurchaseReturn(Base, BranchScopedMixin):
    __tablename__ = "purchase_returns"

    id                   = Column(String, primary_key=True, default=erp_uuid)
    supplier_id          = Column(String, ForeignKey("suppliers.id"), nullable=False, index=True)
    procurement_order_id = Column(String, ForeignKey("procurement_orders.id"), nullable=True)
    return_number        = Column(String(64), nullable=False)
    return_date          = Column(Date, nullable=False)
    returned_weight_kg   = Column(Float, default=0.0, nullable=False)
    credit_amount        = Column(Float, default=0.0, nullable=False)
    reason               = Column(Text, nullable=True)
    status               = Column(String(32), default="pending", nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "return_number", name="uq_pr_number_per_company"),
        CheckConstraint("returned_weight_kg >= 0", name="ck_pr_wt_nonneg"),
    )


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 4: CUSTOMER & SALES MANAGEMENT (9 Tables)
# ══════════════════════════════════════════════════════════════════════════════

class Customer(Base, BranchScopedMixin):
    __tablename__ = "customers"

    id                  = Column(String, primary_key=True, default=erp_uuid)
    customer_code       = Column(String(64), nullable=False)
    name                = Column(String(256), nullable=False)
    customer_type       = Column(String(64), default="smelter")  # smelter | refiner | manufacturer | trader
    registration_number = Column(String(128), nullable=True)
    tax_id              = Column(String(128), nullable=True)
    is_active           = Column(Boolean, default=True, nullable=False, index=True)

    contacts     = relationship("CustomerContact", back_populates="customer", cascade="all, delete-orphan")
    sales_orders = relationship("SalesOrder", back_populates="customer")

    __table_args__ = (
        UniqueConstraint("company_id", "customer_code", name="uq_customer_code_per_company"),
        Index("ix_customers_company_name", "company_id", "name"),
    )


class CustomerContact(Base, CompanyScopedMixin):
    __tablename__ = "customer_contacts"

    id           = Column(String, primary_key=True, default=erp_uuid)
    customer_id  = Column(String, ForeignKey("customers.id"), nullable=False, index=True)
    contact_name = Column(String(256), nullable=False)
    role         = Column(String(128), nullable=True)
    email        = Column(String(256), nullable=True)
    phone        = Column(String(64), nullable=True)
    is_primary   = Column(Boolean, default=False, nullable=False)

    customer = relationship("Customer", back_populates="contacts")


class CustomerDocument(Base, CompanyScopedMixin):
    __tablename__ = "customer_documents"

    id              = Column(String, primary_key=True, default=erp_uuid)
    customer_id     = Column(String, ForeignKey("customers.id"), nullable=False, index=True)
    document_type   = Column(String(64), nullable=False)
    document_number = Column(String(128), nullable=True)
    file_path       = Column(String(512), nullable=True)
    valid_until     = Column(Date, nullable=True)


class Quotation(Base, BranchScopedMixin):
    __tablename__ = "quotations"

    id               = Column(String, primary_key=True, default=erp_uuid)
    customer_id      = Column(String, ForeignKey("customers.id"), nullable=False, index=True)
    quote_number     = Column(String(64), nullable=False)
    quote_date       = Column(Date, nullable=False)
    valid_until      = Column(Date, nullable=True)
    material_summary = Column(Text, nullable=True)
    quoted_total     = Column(Float, default=0.0, nullable=False)
    status           = Column(String(32), default="open", nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "quote_number", name="uq_quote_number_per_company"),
    )


class SalesOrder(Base, BranchScopedMixin):
    __tablename__ = "sales_orders"

    id              = Column(String, primary_key=True, default=erp_uuid)
    customer_id     = Column(String, ForeignKey("customers.id"), nullable=False, index=True)
    quotation_id    = Column(String, ForeignKey("quotations.id"), nullable=True)
    so_number       = Column(String(64), nullable=False)
    order_date      = Column(Date, nullable=False, index=True)
    subtotal_amount = Column(Float, default=0.0, nullable=False)
    tax_amount      = Column(Float, default=0.0, nullable=False)
    total_amount    = Column(Float, default=0.0, nullable=False)
    currency        = Column(String(8), default="USD", nullable=False)
    delivery_status = Column(String(32), default="pending", nullable=False, index=True)
    payment_status  = Column(String(32), default="unpaid", nullable=False, index=True)
    notes           = Column(Text, nullable=True)

    customer = relationship("Customer", back_populates="sales_orders")
    items    = relationship("SalesOrderItem", back_populates="order", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("company_id", "so_number", name="uq_so_number_per_company"),
        CheckConstraint("total_amount >= 0", name="ck_so_total_nonneg"),
    )


class SalesOrderItem(Base, CompanyScopedMixin):
    __tablename__ = "sales_order_items"

    id                      = Column(String, primary_key=True, default=erp_uuid)
    sales_order_id          = Column(String, ForeignKey("sales_orders.id"), nullable=False, index=True)
    recovered_material_name = Column(String(128), nullable=False)
    inventory_item_id       = Column(String, ForeignKey("inventory_items.id"), nullable=True, index=True)
    quantity_kg             = Column(Float, nullable=False)
    unit_price              = Column(Float, nullable=False)
    tax_rate_pct            = Column(Float, default=0.0, nullable=False)
    tax_amount              = Column(Float, default=0.0, nullable=False)
    line_total              = Column(Float, nullable=False)

    order = relationship("SalesOrder", back_populates="items")

    __table_args__ = (
        CheckConstraint("quantity_kg >= 0", name="ck_soi_qty_nonneg"),
        CheckConstraint("unit_price >= 0", name="ck_soi_price_nonneg"),
    )


class SalesInvoice(Base, BranchScopedMixin):
    __tablename__ = "sales_invoices"

    id              = Column(String, primary_key=True, default=erp_uuid)
    customer_id     = Column(String, ForeignKey("customers.id"), nullable=False, index=True)
    sales_order_id  = Column(String, ForeignKey("sales_orders.id"), nullable=True, index=True)
    invoice_number  = Column(String(64), nullable=False)
    invoice_date    = Column(Date, nullable=False)
    due_date        = Column(Date, nullable=True)
    subtotal_amount = Column(Float, default=0.0, nullable=False)
    tax_amount      = Column(Float, default=0.0, nullable=False)
    total_amount    = Column(Float, default=0.0, nullable=False)
    paid_amount     = Column(Float, default=0.0, nullable=False)
    payment_status  = Column(String(32), default="unpaid", nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("company_id", "invoice_number", name="uq_sales_inv_per_company"),
        CheckConstraint("total_amount >= 0", name="ck_sales_inv_total_nonneg"),
    )


class SalesPayment(Base, BranchScopedMixin):
    __tablename__ = "sales_payments"

    id                = Column(String, primary_key=True, default=erp_uuid)
    customer_id       = Column(String, ForeignKey("customers.id"), nullable=False, index=True)
    sales_invoice_id  = Column(String, ForeignKey("sales_invoices.id"), nullable=True, index=True)
    payment_reference = Column(String(64), nullable=False)
    payment_date      = Column(Date, nullable=False)
    amount            = Column(Float, nullable=False)
    payment_method    = Column(String(32), default="bank_transfer", nullable=False)
    status            = Column(String(32), default="completed", nullable=False)

    __table_args__ = (
        CheckConstraint("amount >= 0", name="ck_sales_pay_nonneg"),
    )


class SalesReturn(Base, BranchScopedMixin):
    __tablename__ = "sales_returns"

    id                   = Column(String, primary_key=True, default=erp_uuid)
    customer_id          = Column(String, ForeignKey("customers.id"), nullable=False, index=True)
    sales_order_id       = Column(String, ForeignKey("sales_orders.id"), nullable=True)
    return_number        = Column(String(64), nullable=False)
    return_date          = Column(Date, nullable=False)
    returned_quantity_kg = Column(Float, default=0.0, nullable=False)
    refund_amount        = Column(Float, default=0.0, nullable=False)
    reason               = Column(Text, nullable=True)
    status               = Column(String(32), default="pending", nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "return_number", name="uq_sr_number_per_company"),
    )
