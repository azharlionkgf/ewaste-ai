"""
E-Waste AI — Industrial ERP ORM Models: Modules 7, 8 & 9
========================================================
Module 7: Component & Material Management (8 new + reused `components`)
Module 8: Material Recovery Management (8 tables — measured vs estimated kept strict)
Module 9: Warehouse & Inventory Management (10 tables — transactional stock ledger)
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
    String,
    Text,
    UniqueConstraint,
)

from backend.database import Base
from backend.models.erp_mixins import BranchScopedMixin, CompanyScopedMixin, erp_now, erp_uuid


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 7: COMPONENT & MATERIAL MANAGEMENT (8 New + Reused `components`)
# ══════════════════════════════════════════════════════════════════════════════

class DeviceCategory(Base, CompanyScopedMixin):
    __tablename__ = "device_categories"

    id            = Column(String, primary_key=True, default=erp_uuid)
    category_code = Column(String(64), nullable=False)
    category_name = Column(String(128), nullable=False)
    weee_code     = Column(String(32), nullable=True)

    __table_args__ = (
        UniqueConstraint("company_id", "category_code", name="uq_dev_cat_per_company"),
    )


class DeviceModel(Base, CompanyScopedMixin):
    __tablename__ = "device_models"

    id                 = Column(String, primary_key=True, default=erp_uuid)
    device_category_id = Column(String, ForeignKey("device_categories.id"), nullable=False, index=True)
    manufacturer       = Column(String(128), nullable=True)
    model_name         = Column(String(256), nullable=False)
    typical_weight_kg  = Column(Float, default=0.0, nullable=False)


class ComponentCategory(Base, CompanyScopedMixin):
    __tablename__ = "component_categories"

    id                        = Column(String, primary_key=True, default=erp_uuid)
    category_code             = Column(String(64), nullable=False)
    category_name             = Column(String(128), nullable=False)
    is_potentially_hazardous  = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "category_code", name="uq_comp_cat_per_company"),
    )


class MaterialType(Base, CompanyScopedMixin):
    __tablename__ = "material_types"

    id             = Column(String, primary_key=True, default=erp_uuid)
    material_code  = Column(String(64), nullable=False)
    material_name  = Column(String(128), nullable=False)
    material_group = Column(String(64), nullable=False)  # copper | aluminium | iron_steel | plastics | glass | precious_metals | battery_hazardous | other
    is_hazardous   = Column(Boolean, default=False, nullable=False)
    default_unit   = Column(String(16), default="kg", nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "material_code", name="uq_mat_type_per_company"),
    )


class MaterialCompositionSource(Base, CompanyScopedMixin):
    __tablename__ = "material_composition_sources"

    id                  = Column(String, primary_key=True, default=erp_uuid)
    source_name         = Column(String(256), nullable=False)
    source_type         = Column(String(64), nullable=False)  # academic_survey | oem_datasheet | lab_assay | industry_benchmark
    citation_url        = Column(String(512), nullable=True)
    confidence_level    = Column(String(32), default="medium", nullable=False)
    verification_status = Column(String(32), default="unverified", nullable=False)  # verified | unverified | preliminary


class ComponentMaterialMapping(Base, CompanyScopedMixin):
    """Stores component-to-material estimates with source & verification; distinct from measured recovery."""
    __tablename__ = "component_material_mapping"

    id                    = Column(String, primary_key=True, default=erp_uuid)
    component_id          = Column(String, ForeignKey("components.id"), nullable=True, index=True)
    component_category_id = Column(String, ForeignKey("component_categories.id"), nullable=True, index=True)
    material_type_id      = Column(String, ForeignKey("material_types.id"), nullable=False, index=True)
    source_id             = Column(String, ForeignKey("material_composition_sources.id"), nullable=True)
    estimated_pct         = Column(Float, nullable=False)
    verification_status   = Column(String(32), default="unverified", nullable=False)
    confidence_score      = Column(Float, nullable=True)
    is_measured_recovery  = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        CheckConstraint("estimated_pct >= 0 AND estimated_pct <= 100", name="ck_cmm_pct_range"),
        CheckConstraint("NOT is_measured_recovery", name="ck_cmm_never_measured"),
    )


class HazardousMaterialType(Base, CompanyScopedMixin):
    __tablename__ = "hazardous_material_types"

    id                    = Column(String, primary_key=True, default=erp_uuid)
    hazard_code           = Column(String(64), nullable=False)
    substance_name        = Column(String(128), nullable=False)
    cas_number            = Column(String(32), nullable=True)
    risk_level            = Column(String(32), default="high", nullable=False)
    jurisdiction_reference = Column(String(256), nullable=True)
    handling_guidance     = Column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("company_id", "hazard_code", name="uq_haz_code_per_company"),
    )


class HazardousMaterialRecord(Base, BranchScopedMixin):
    __tablename__ = "hazardous_material_records"

    id                         = Column(String, primary_key=True, default=erp_uuid)
    incoming_batch_id          = Column(String, ForeignKey("incoming_batches.id"), nullable=False, index=True)
    hazardous_material_type_id = Column(String, ForeignKey("hazardous_material_types.id"), nullable=False, index=True)
    measured_or_estimated      = Column(String(32), default="estimated", nullable=False)
    quantity_kg                = Column(Float, default=0.0, nullable=False)
    containment_status         = Column(String(64), default="contained", nullable=False)
    recorded_by_employee_id    = Column(String, ForeignKey("employees.id"), nullable=True)

    __table_args__ = (
        CheckConstraint("quantity_kg >= 0", name="ck_hmr_qty_nonneg"),
    )


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 8: MATERIAL RECOVERY MANAGEMENT (8 Tables)
# ══════════════════════════════════════════════════════════════════════════════

class RecoveryJob(Base, BranchScopedMixin):
    __tablename__ = "recovery_jobs"

    id                      = Column(String, primary_key=True, default=erp_uuid)
    incoming_batch_id       = Column(String, ForeignKey("incoming_batches.id"), nullable=False, index=True)
    processing_job_id       = Column(String, ForeignKey("processing_jobs.id"), nullable=True, index=True)
    responsible_employee_id = Column(String, ForeignKey("employees.id"), nullable=True, index=True)
    job_number              = Column(String(64), nullable=False)
    recovery_date           = Column(Date, nullable=False, index=True)
    status                  = Column(String(32), default="completed", nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "job_number", name="uq_rec_job_per_company"),
    )


class RecoveryJobInput(Base, CompanyScopedMixin):
    __tablename__ = "recovery_job_inputs"

    id                   = Column(String, primary_key=True, default=erp_uuid)
    recovery_job_id      = Column(String, ForeignKey("recovery_jobs.id"), nullable=False, index=True)
    material_description = Column(String(256), nullable=False)
    input_quantity_kg    = Column(Float, nullable=False)

    __table_args__ = (
        CheckConstraint("input_quantity_kg >= 0", name="ck_rji_qty_nonneg"),
    )


class RecoveryJobOutput(Base, CompanyScopedMixin):
    """Strictly separates measured, predicted, and estimated recovery quantities."""
    __tablename__ = "recovery_job_outputs"

    id               = Column(String, primary_key=True, default=erp_uuid)
    recovery_job_id  = Column(String, ForeignKey("recovery_jobs.id"), nullable=False, index=True)
    material_type_id = Column(String, ForeignKey("material_types.id"), nullable=False, index=True)
    output_weight_kg = Column(Float, nullable=False)
    measurement_type = Column(String(32), default="measured", nullable=False)  # measured | predicted | estimated
    quality_grade    = Column(String(32), nullable=True)
    destination      = Column(String(256), nullable=True)

    __table_args__ = (
        CheckConstraint("output_weight_kg >= 0", name="ck_rjo_wt_nonneg"),
    )


class RecoveredMaterial(Base, BranchScopedMixin):
    __tablename__ = "recovered_materials"

    id                      = Column(String, primary_key=True, default=erp_uuid)
    incoming_batch_id       = Column(String, ForeignKey("incoming_batches.id"), nullable=False, index=True)
    recovery_job_id         = Column(String, ForeignKey("recovery_jobs.id"), nullable=False, index=True)
    material_type_id        = Column(String, ForeignKey("material_types.id"), nullable=False, index=True)
    measured_weight_kg      = Column(Float, default=0.0, nullable=False)
    predicted_weight_kg     = Column(Float, nullable=True)
    estimated_weight_kg     = Column(Float, nullable=True)
    quality_grade           = Column(String(64), nullable=True)
    recovery_date           = Column(Date, nullable=False, index=True)
    responsible_employee_id = Column(String, ForeignKey("employees.id"), nullable=True)
    final_destination       = Column(String(256), nullable=True)

    __table_args__ = (
        CheckConstraint("measured_weight_kg >= 0", name="ck_rm_meas_nonneg"),
    )


class MaterialQualityRecord(Base, BranchScopedMixin):
    __tablename__ = "material_quality_records"

    id                    = Column(String, primary_key=True, default=erp_uuid)
    recovered_material_id = Column(String, ForeignKey("recovered_materials.id"), nullable=False, index=True)
    assay_method          = Column(String(128), nullable=True)
    purity_pct            = Column(Float, nullable=True)
    moisture_pct          = Column(Float, nullable=True)
    grade                 = Column(String(64), nullable=True)
    certified_lab_ref     = Column(String(128), nullable=True)
    tested_at             = Column(DateTime, default=erp_now, nullable=False)


class MaterialLossRecord(Base, BranchScopedMixin):
    __tablename__ = "material_loss_records"

    id                 = Column(String, primary_key=True, default=erp_uuid)
    recovery_job_id    = Column(String, ForeignKey("recovery_jobs.id"), nullable=False, index=True)
    incoming_batch_id  = Column(String, ForeignKey("incoming_batches.id"), nullable=False, index=True)
    loss_weight_kg     = Column(Float, default=0.0, nullable=False)
    remaining_waste_kg = Column(Float, default=0.0, nullable=False)
    loss_reason        = Column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint("loss_weight_kg >= 0", name="ck_mlr_loss_nonneg"),
        CheckConstraint("remaining_waste_kg >= 0", name="ck_mlr_rem_nonneg"),
    )


class RecoveryMeasurement(Base, BranchScopedMixin):
    __tablename__ = "recovery_measurements"

    id                      = Column(String, primary_key=True, default=erp_uuid)
    recovery_job_id         = Column(String, ForeignKey("recovery_jobs.id"), nullable=False, index=True)
    material_type_id        = Column(String, ForeignKey("material_types.id"), nullable=False, index=True)
    measurement_category    = Column(String(32), nullable=False)  # measured | predicted | estimated
    weight_kg               = Column(Float, nullable=False)
    scale_device_id         = Column(String(64), nullable=True)
    measured_at             = Column(DateTime, default=erp_now, nullable=False)
    measured_by_employee_id = Column(String, ForeignKey("employees.id"), nullable=True)

    __table_args__ = (
        CheckConstraint("weight_kg >= 0", name="ck_rmeas_wt_nonneg"),
    )


class RecoveryMethodRecord(Base, CompanyScopedMixin):
    __tablename__ = "recovery_method_records"

    id              = Column(String, primary_key=True, default=erp_uuid)
    recovery_job_id = Column(String, ForeignKey("recovery_jobs.id"), nullable=False, index=True)
    method_name     = Column(String(128), nullable=False)
    parameters_json = Column(JSON, nullable=True)
    yield_pct       = Column(Float, nullable=True)
    notes           = Column(Text, nullable=True)


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 9: WAREHOUSE & INVENTORY MANAGEMENT (10 Tables)
# ══════════════════════════════════════════════════════════════════════════════

class Warehouse(Base, BranchScopedMixin):
    __tablename__ = "warehouses"

    id             = Column(String, primary_key=True, default=erp_uuid)
    warehouse_code = Column(String(64), nullable=False)
    warehouse_name = Column(String(256), nullable=False)
    warehouse_type = Column(String(64), default="recovered_stock")  # raw_ewaste | recovered_stock | hazmat | dispatch
    capacity_kg    = Column(Float, default=0.0, nullable=False)
    is_active      = Column(Boolean, default=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "warehouse_code", name="uq_wh_code_per_company"),
    )


class WarehouseLocation(Base, CompanyScopedMixin):
    __tablename__ = "warehouse_locations"

    id             = Column(String, primary_key=True, default=erp_uuid)
    warehouse_id   = Column(String, ForeignKey("warehouses.id"), nullable=False, index=True)
    bin_code       = Column(String(64), nullable=False)
    zone           = Column(String(64), nullable=True)
    rack           = Column(String(64), nullable=True)
    is_hazmat_zone = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("warehouse_id", "bin_code", name="uq_bin_code_per_warehouse"),
    )


class ERPInventoryItem(Base, BranchScopedMixin):
    """Master catalog of tracked warehouse stock items (coexists with legacy `inventory` table)."""
    __tablename__ = "inventory_items"

    id               = Column(String, primary_key=True, default=erp_uuid)
    material_type_id = Column(String, ForeignKey("material_types.id"), nullable=True, index=True)
    sku_code         = Column(String(64), nullable=False)
    item_name        = Column(String(256), nullable=False)
    uom              = Column(String(16), default="kg", nullable=False)
    min_stock_kg     = Column(Float, default=0.0, nullable=False)
    is_active        = Column(Boolean, default=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "sku_code", name="uq_sku_per_company"),
        CheckConstraint("min_stock_kg >= 0", name="ck_inv_item_min_nonneg"),
    )


class InventoryStock(Base, BranchScopedMixin):
    __tablename__ = "inventory_stock"

    id                = Column(String, primary_key=True, default=erp_uuid)
    warehouse_id      = Column(String, ForeignKey("warehouses.id"), nullable=False, index=True)
    location_id       = Column(String, ForeignKey("warehouse_locations.id"), nullable=True)
    inventory_item_id = Column(String, ForeignKey("inventory_items.id"), nullable=False, index=True)
    incoming_batch_id = Column(String, ForeignKey("incoming_batches.id"), nullable=True, index=True)
    opening_stock_kg  = Column(Float, default=0.0, nullable=False)
    received_stock_kg = Column(Float, default=0.0, nullable=False)
    issued_stock_kg   = Column(Float, default=0.0, nullable=False)
    sold_stock_kg     = Column(Float, default=0.0, nullable=False)
    closing_stock_kg  = Column(Float, default=0.0, nullable=False)
    reserved_stock_kg = Column(Float, default=0.0, nullable=False)

    __table_args__ = (
        CheckConstraint("closing_stock_kg >= 0", name="ck_stock_closing_nonneg"),
        CheckConstraint("reserved_stock_kg >= 0", name="ck_stock_res_nonneg"),
        Index("ix_stock_wh_item_batch", "warehouse_id", "inventory_item_id", "incoming_batch_id"),
    )


class InventoryTransaction(Base, BranchScopedMixin):
    __tablename__ = "inventory_transactions"

    id                       = Column(String, primary_key=True, default=erp_uuid)
    warehouse_id             = Column(String, ForeignKey("warehouses.id"), nullable=False, index=True)
    inventory_item_id        = Column(String, ForeignKey("inventory_items.id"), nullable=False, index=True)
    incoming_batch_id        = Column(String, ForeignKey("incoming_batches.id"), nullable=True, index=True)
    txn_type                 = Column(String(32), nullable=False, index=True)  # OPENING | RECEIVE | ISSUE | SALE | TRANSFER_IN | TRANSFER_OUT | ADJUST
    quantity_kg              = Column(Float, nullable=False)
    balance_after_kg         = Column(Float, nullable=False)
    reference_type           = Column(String(64), nullable=True)
    reference_id             = Column(String, nullable=True)
    performed_by_employee_id = Column(String, ForeignKey("employees.id"), nullable=True)
    txn_at                   = Column(DateTime, default=erp_now, nullable=False, index=True)

    __table_args__ = (
        CheckConstraint("balance_after_kg >= 0", name="ck_itxn_bal_nonneg"),
    )


class StockMovement(Base, BranchScopedMixin):
    __tablename__ = "stock_movements"

    id                = Column(String, primary_key=True, default=erp_uuid)
    inventory_item_id = Column(String, ForeignKey("inventory_items.id"), nullable=False, index=True)
    from_warehouse_id = Column(String, ForeignKey("warehouses.id"), nullable=True)
    to_warehouse_id   = Column(String, ForeignKey("warehouses.id"), nullable=True)
    incoming_batch_id = Column(String, ForeignKey("incoming_batches.id"), nullable=True)
    quantity_kg       = Column(Float, nullable=False)
    movement_date     = Column(DateTime, default=erp_now, nullable=False)
    reference_no      = Column(String(64), nullable=True)

    __table_args__ = (
        CheckConstraint("quantity_kg > 0", name="ck_sm_qty_pos"),
    )


class StockAdjustment(Base, BranchScopedMixin):
    __tablename__ = "stock_adjustments"

    id                      = Column(String, primary_key=True, default=erp_uuid)
    warehouse_id            = Column(String, ForeignKey("warehouses.id"), nullable=False, index=True)
    inventory_item_id       = Column(String, ForeignKey("inventory_items.id"), nullable=False, index=True)
    adjustment_kg           = Column(Float, nullable=False)
    reason                  = Column(Text, nullable=False)
    approved_by_employee_id = Column(String, ForeignKey("employees.id"), nullable=True)
    adjusted_at             = Column(DateTime, default=erp_now, nullable=False)


class StockReservation(Base, BranchScopedMixin):
    __tablename__ = "stock_reservations"

    id                = Column(String, primary_key=True, default=erp_uuid)
    warehouse_id      = Column(String, ForeignKey("warehouses.id"), nullable=False, index=True)
    inventory_item_id = Column(String, ForeignKey("inventory_items.id"), nullable=False, index=True)
    sales_order_id    = Column(String, ForeignKey("sales_orders.id"), nullable=True, index=True)
    reserved_kg       = Column(Float, nullable=False)
    status            = Column(String(32), default="active", nullable=False)
    expires_at        = Column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint("reserved_kg >= 0", name="ck_sres_nonneg"),
    )


class MaterialTransfer(Base, CompanyScopedMixin):
    __tablename__ = "material_transfers"

    id                = Column(String, primary_key=True, default=erp_uuid)
    from_branch_id    = Column(String, ForeignKey("company_branches.id"), nullable=False, index=True)
    to_branch_id      = Column(String, ForeignKey("company_branches.id"), nullable=False, index=True)
    from_warehouse_id = Column(String, ForeignKey("warehouses.id"), nullable=False)
    to_warehouse_id   = Column(String, ForeignKey("warehouses.id"), nullable=False)
    inventory_item_id = Column(String, ForeignKey("inventory_items.id"), nullable=False)
    incoming_batch_id = Column(String, ForeignKey("incoming_batches.id"), nullable=True)
    transfer_number   = Column(String(64), nullable=False)
    quantity_kg       = Column(Float, nullable=False)
    status            = Column(String(32), default="completed", nullable=False)
    transferred_at    = Column(DateTime, default=erp_now, nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "transfer_number", name="uq_transfer_num_per_company"),
        CheckConstraint("quantity_kg > 0", name="ck_mt_qty_pos"),
    )


class StockAuditRecord(Base, BranchScopedMixin):
    __tablename__ = "stock_audit_records"

    id                    = Column(String, primary_key=True, default=erp_uuid)
    warehouse_id          = Column(String, ForeignKey("warehouses.id"), nullable=False, index=True)
    inventory_item_id     = Column(String, ForeignKey("inventory_items.id"), nullable=False, index=True)
    system_stock_kg       = Column(Float, nullable=False)
    physical_count_kg     = Column(Float, nullable=False)
    variance_kg           = Column(Float, nullable=False)
    audited_by_employee_id = Column(String, ForeignKey("employees.id"), nullable=True)
    audited_at            = Column(DateTime, default=erp_now, nullable=False)
    notes                 = Column(Text, nullable=True)
