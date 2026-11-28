"""
E-Waste AI — Industrial ERP ORM Models: Modules 5, 6, 11 & 12
=============================================================
Module 5: Incoming E-Waste Registration (8 tables)
Module 6: Sorting, Dismantling & Processing (11 tables, sharing `machines`)
Module 12: Machine & Production Management (8 additional + shared `machines`)
Module 11: Transport & Logistics (8 tables)
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
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.models.erp_mixins import BranchScopedMixin, CompanyScopedMixin, erp_now, erp_uuid


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 5: INCOMING E-WASTE REGISTRATION (8 Tables)
# ══════════════════════════════════════════════════════════════════════════════

class IncomingMaterial(Base, BranchScopedMixin):
    __tablename__ = "incoming_materials"

    id                  = Column(String, primary_key=True, default=erp_uuid)
    material_code       = Column(String(64), nullable=False)
    material_name       = Column(String(256), nullable=False)
    ewaste_category     = Column(String(128), nullable=False)
    device_type         = Column(String(128), nullable=True)
    default_hazard_flag = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "material_code", name="uq_inc_mat_code_per_company"),
    )


class IncomingBatch(Base, BranchScopedMixin):
    __tablename__ = "incoming_batches"

    id                      = Column(String, primary_key=True, default=erp_uuid)
    warehouse_id            = Column(String, ForeignKey("warehouses.id"), nullable=True, index=True)
    supplier_id             = Column(String, ForeignKey("suppliers.id"), nullable=True, index=True)
    procurement_order_id    = Column(String, ForeignKey("procurement_orders.id"), nullable=True, index=True)
    responsible_employee_id = Column(String, ForeignKey("employees.id"), nullable=True, index=True)
    legacy_batch_id         = Column(String, ForeignKey("waste_batches.id"), nullable=True)
    batch_number            = Column(String(64), nullable=False, index=True)
    barcode_qr_code         = Column(String(128), nullable=True, index=True)
    receiving_date          = Column(Date, nullable=False, index=True)
    ewaste_category         = Column(String(128), nullable=False)
    device_type             = Column(String(128), nullable=True)
    gross_weight_kg         = Column(Float, nullable=False)
    tare_weight_kg          = Column(Float, default=0.0, nullable=False)
    net_weight_kg           = Column(Float, nullable=False)
    inspection_status       = Column(String(32), default="pending", nullable=False, index=True)
    purchase_value          = Column(Float, default=0.0, nullable=False)
    batch_status            = Column(String(32), default="received", nullable=False, index=True)
    notes                   = Column(Text, nullable=True)

    items           = relationship("BatchItem", back_populates="batch", cascade="all, delete-orphan")
    status_history  = relationship("BatchStatusHistory", back_populates="batch", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("company_id", "batch_number", name="uq_incoming_batch_per_company"),
        CheckConstraint("gross_weight_kg >= 0", name="ck_inc_gross_nonneg"),
        CheckConstraint("tare_weight_kg >= 0", name="ck_inc_tare_nonneg"),
        CheckConstraint("net_weight_kg >= 0", name="ck_inc_net_nonneg"),
        CheckConstraint("purchase_value >= 0", name="ck_inc_val_nonneg"),
        Index("ix_inc_batch_company_branch_status", "company_id", "branch_id", "batch_status"),
    )


class BatchItem(Base, BranchScopedMixin):
    __tablename__ = "batch_items"

    id                   = Column(String, primary_key=True, default=erp_uuid)
    incoming_batch_id    = Column(String, ForeignKey("incoming_batches.id"), nullable=False, index=True)
    incoming_material_id = Column(String, ForeignKey("incoming_materials.id"), nullable=True)
    item_code            = Column(String(64), nullable=False)
    device_type          = Column(String(128), nullable=True)
    quantity             = Column(Integer, default=1, nullable=False)
    gross_weight_kg      = Column(Float, default=0.0, nullable=False)
    net_weight_kg        = Column(Float, default=0.0, nullable=False)
    condition            = Column(String(32), default="unknown")

    batch = relationship("IncomingBatch", back_populates="items")

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="ck_bi_qty_nonneg"),
        CheckConstraint("net_weight_kg >= 0", name="ck_bi_wt_nonneg"),
    )


class WeighbridgeRecord(Base, BranchScopedMixin):
    __tablename__ = "weighbridge_records"

    id                   = Column(String, primary_key=True, default=erp_uuid)
    incoming_batch_id    = Column(String, ForeignKey("incoming_batches.id"), nullable=False, index=True)
    ticket_number        = Column(String(64), nullable=False)
    vehicle_number       = Column(String(64), nullable=True)
    gross_weight_kg      = Column(Float, nullable=False)
    tare_weight_kg       = Column(Float, default=0.0, nullable=False)
    net_weight_kg        = Column(Float, nullable=False)
    weighed_at           = Column(DateTime, default=erp_now, nullable=False)
    operator_employee_id = Column(String, ForeignKey("employees.id"), nullable=True)

    __table_args__ = (
        UniqueConstraint("company_id", "ticket_number", name="uq_wb_ticket_per_company"),
        CheckConstraint("gross_weight_kg >= tare_weight_kg", name="ck_wb_gross_ge_tare"),
        CheckConstraint("net_weight_kg >= 0", name="ck_wb_net_nonneg"),
    )


class MaterialReceivingRecord(Base, BranchScopedMixin):
    __tablename__ = "material_receiving_records"

    id                      = Column(String, primary_key=True, default=erp_uuid)
    warehouse_id            = Column(String, ForeignKey("warehouses.id"), nullable=True, index=True)
    incoming_batch_id       = Column(String, ForeignKey("incoming_batches.id"), nullable=False, index=True)
    gate_pass_number        = Column(String(64), nullable=False)
    received_at             = Column(DateTime, default=erp_now, nullable=False)
    received_by_employee_id = Column(String, ForeignKey("employees.id"), nullable=True)
    remarks                 = Column(Text, nullable=True)


class IncomingInspection(Base, BranchScopedMixin):
    __tablename__ = "incoming_inspections"

    id                    = Column(String, primary_key=True, default=erp_uuid)
    incoming_batch_id     = Column(String, ForeignKey("incoming_batches.id"), nullable=False, index=True)
    inspector_employee_id = Column(String, ForeignKey("employees.id"), nullable=True)
    inspection_date       = Column(DateTime, default=erp_now, nullable=False)
    contamination_detected = Column(Boolean, default=False, nullable=False)
    hazardous_present     = Column(Boolean, default=False, nullable=False)
    moisture_pct          = Column(Float, nullable=True)
    inspection_status     = Column(String(32), default="passed", nullable=False)
    findings              = Column(Text, nullable=True)


class BatchDocument(Base, BranchScopedMixin):
    __tablename__ = "batch_documents"

    id                = Column(String, primary_key=True, default=erp_uuid)
    incoming_batch_id = Column(String, ForeignKey("incoming_batches.id"), nullable=False, index=True)
    document_type     = Column(String(64), nullable=False)
    title             = Column(String(256), nullable=False)
    file_path         = Column(String(512), nullable=True)
    checksum_sha256   = Column(String(64), nullable=True)


class BatchStatusHistory(Base, BranchScopedMixin):
    __tablename__ = "batch_status_history"

    id                     = Column(String, primary_key=True, default=erp_uuid)
    incoming_batch_id      = Column(String, ForeignKey("incoming_batches.id"), nullable=False, index=True)
    previous_status        = Column(String(32), nullable=True)
    new_status             = Column(String(32), nullable=False)
    changed_by_employee_id = Column(String, ForeignKey("employees.id"), nullable=True)
    changed_at             = Column(DateTime, default=erp_now, nullable=False, index=True)
    reason                 = Column(Text, nullable=True)

    batch = relationship("IncomingBatch", back_populates="status_history")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 12 & MODULE 6: PRODUCTION LINES, WORKSTATIONS, MACHINES & PROCESSING
# ══════════════════════════════════════════════════════════════════════════════

class ProductionLine(Base, BranchScopedMixin):
    __tablename__ = "production_lines"

    id            = Column(String, primary_key=True, default=erp_uuid)
    line_code     = Column(String(64), nullable=False)
    line_name     = Column(String(256), nullable=False)
    process_focus = Column(String(128), nullable=True)
    is_active     = Column(Boolean, default=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "line_code", name="uq_line_code_per_company"),
    )


class Workstation(Base, BranchScopedMixin):
    __tablename__ = "workstations"

    id                 = Column(String, primary_key=True, default=erp_uuid)
    production_line_id = Column(String, ForeignKey("production_lines.id"), nullable=True)
    station_code       = Column(String(64), nullable=False)
    station_name       = Column(String(256), nullable=False)
    station_type       = Column(String(64), default="sorting", nullable=False)  # sorting | dismantling | inspection
    is_active          = Column(Boolean, default=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "station_code", name="uq_station_code_per_company"),
    )


class MachineCategory(Base, CompanyScopedMixin):
    __tablename__ = "machine_categories"

    id            = Column(String, primary_key=True, default=erp_uuid)
    category_code = Column(String(64), nullable=False)
    category_name = Column(String(128), nullable=False)
    description   = Column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("company_id", "category_code", name="uq_mcat_code_per_company"),
    )


class Machine(Base, BranchScopedMixin):
    """Unified machine master table shared across Modules 6 and 12."""
    __tablename__ = "machines"

    id                    = Column(String, primary_key=True, default=erp_uuid)
    production_line_id    = Column(String, ForeignKey("production_lines.id"), nullable=True, index=True)
    workstation_id        = Column(String, ForeignKey("workstations.id"), nullable=True)
    machine_category_id   = Column(String, ForeignKey("machine_categories.id"), nullable=True, index=True)
    machine_code          = Column(String(64), nullable=False)
    machine_name          = Column(String(256), nullable=False)
    manufacturer          = Column(String(128), nullable=True)
    model_no              = Column(String(128), nullable=True)
    serial_no             = Column(String(128), nullable=True)
    rated_capacity_kg_hr  = Column(Float, default=0.0, nullable=False)
    status                = Column(String(32), default="operational", nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("company_id", "machine_code", name="uq_machine_code_per_company"),
        CheckConstraint("rated_capacity_kg_hr >= 0", name="ck_machine_cap_nonneg"),
    )


class MachineCapacity(Base, CompanyScopedMixin):
    __tablename__ = "machine_capacity"

    id                   = Column(String, primary_key=True, default=erp_uuid)
    machine_id           = Column(String, ForeignKey("machines.id"), nullable=False, index=True)
    material_category    = Column(String(128), nullable=False)
    throughput_kg_per_hr = Column(Float, nullable=False)
    power_rating_kw      = Column(Float, default=0.0, nullable=False)
    effective_from       = Column(Date, nullable=False)

    __table_args__ = (
        CheckConstraint("throughput_kg_per_hr >= 0", name="ck_mc_tp_nonneg"),
    )


class SortingOperation(Base, BranchScopedMixin):
    __tablename__ = "sorting_operations"

    id                   = Column(String, primary_key=True, default=erp_uuid)
    incoming_batch_id    = Column(String, ForeignKey("incoming_batches.id"), nullable=False, index=True)
    workstation_id       = Column(String, ForeignKey("workstations.id"), nullable=True)
    operator_employee_id = Column(String, ForeignKey("employees.id"), nullable=True, index=True)
    start_time           = Column(DateTime, nullable=False)
    end_time             = Column(DateTime, nullable=True)
    input_weight_kg      = Column(Float, nullable=False)
    output_weight_kg     = Column(Float, default=0.0, nullable=False)
    rejected_quantity_kg = Column(Float, default=0.0, nullable=False)
    status               = Column(String(32), default="completed", nullable=False)
    notes                = Column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint("input_weight_kg >= 0", name="ck_sort_in_nonneg"),
        CheckConstraint("output_weight_kg >= 0", name="ck_sort_out_nonneg"),
        CheckConstraint("rejected_quantity_kg >= 0", name="ck_sort_rej_nonneg"),
    )


class DismantlingOperation(Base, BranchScopedMixin):
    """Authorized operational dismantling log (stores no unsafe manual procedures)."""
    __tablename__ = "dismantling_operations"

    id                     = Column(String, primary_key=True, default=erp_uuid)
    incoming_batch_id      = Column(String, ForeignKey("incoming_batches.id"), nullable=False, index=True)
    workstation_id         = Column(String, ForeignKey("workstations.id"), nullable=True)
    operator_employee_id   = Column(String, ForeignKey("employees.id"), nullable=True, index=True)
    authorization_verified = Column(Boolean, default=True, nullable=False)
    start_time             = Column(DateTime, nullable=False)
    end_time               = Column(DateTime, nullable=True)
    input_weight_kg        = Column(Float, nullable=False)
    output_weight_kg       = Column(Float, default=0.0, nullable=False)
    rejected_quantity_kg   = Column(Float, default=0.0, nullable=False)
    status                 = Column(String(32), default="completed", nullable=False)
    notes                  = Column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint("input_weight_kg >= 0", name="ck_dism_in_nonneg"),
        CheckConstraint("output_weight_kg >= 0", name="ck_dism_out_nonneg"),
    )


class ProcessingJob(Base, BranchScopedMixin):
    __tablename__ = "processing_jobs"

    id                   = Column(String, primary_key=True, default=erp_uuid)
    incoming_batch_id    = Column(String, ForeignKey("incoming_batches.id"), nullable=False, index=True)
    production_line_id   = Column(String, ForeignKey("production_lines.id"), nullable=True)
    machine_id           = Column(String, ForeignKey("machines.id"), nullable=True, index=True)
    operator_employee_id = Column(String, ForeignKey("employees.id"), nullable=True, index=True)
    job_number           = Column(String(64), nullable=False)
    process_type         = Column(String(64), nullable=False)  # shredding | magnetic | eddy_current | separation
    start_time           = Column(DateTime, nullable=False)
    end_time             = Column(DateTime, nullable=True)
    input_weight_kg      = Column(Float, nullable=False)
    output_weight_kg     = Column(Float, default=0.0, nullable=False)
    rejected_quantity_kg = Column(Float, default=0.0, nullable=False)
    status               = Column(String(32), default="in_progress", nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("company_id", "job_number", name="uq_proc_job_number_per_company"),
        CheckConstraint("input_weight_kg >= 0", name="ck_pj_in_nonneg"),
        CheckConstraint("output_weight_kg >= 0", name="ck_pj_out_nonneg"),
        CheckConstraint("rejected_quantity_kg >= 0", name="ck_pj_rej_nonneg"),
    )


class ProcessingJobItem(Base, CompanyScopedMixin):
    __tablename__ = "processing_job_items"

    id                   = Column(String, primary_key=True, default=erp_uuid)
    processing_job_id    = Column(String, ForeignKey("processing_jobs.id"), nullable=False, index=True)
    batch_item_id        = Column(String, ForeignKey("batch_items.id"), nullable=True)
    input_weight_kg      = Column(Float, nullable=False)
    output_weight_kg     = Column(Float, default=0.0, nullable=False)
    rejected_quantity_kg = Column(Float, default=0.0, nullable=False)


class MachineUsageLog(Base, BranchScopedMixin):
    __tablename__ = "machine_usage_logs"

    id                   = Column(String, primary_key=True, default=erp_uuid)
    machine_id           = Column(String, ForeignKey("machines.id"), nullable=False, index=True)
    processing_job_id    = Column(String, ForeignKey("processing_jobs.id"), nullable=True, index=True)
    operator_employee_id = Column(String, ForeignKey("employees.id"), nullable=True)
    start_time           = Column(DateTime, nullable=False)
    end_time             = Column(DateTime, nullable=True)
    hours_used           = Column(Float, default=0.0, nullable=False)
    throughput_kg        = Column(Float, default=0.0, nullable=False)


class MachineMaintenance(Base, BranchScopedMixin):
    __tablename__ = "machine_maintenance"

    id               = Column(String, primary_key=True, default=erp_uuid)
    machine_id       = Column(String, ForeignKey("machines.id"), nullable=False, index=True)
    maintenance_type = Column(String(64), nullable=False)
    performed_at     = Column(DateTime, nullable=False)
    performed_by     = Column(String(128), nullable=True)
    cost_amount      = Column(Float, default=0.0, nullable=False)
    summary          = Column(Text, nullable=True)


class OperatorAssignment(Base, BranchScopedMixin):
    __tablename__ = "operator_assignments"

    id                = Column(String, primary_key=True, default=erp_uuid)
    employee_id       = Column(String, ForeignKey("employees.id"), nullable=False, index=True)
    workstation_id    = Column(String, ForeignKey("workstations.id"), nullable=True)
    machine_id        = Column(String, ForeignKey("machines.id"), nullable=True)
    processing_job_id = Column(String, ForeignKey("processing_jobs.id"), nullable=True)
    assigned_from     = Column(DateTime, default=erp_now, nullable=False)
    assigned_to       = Column(DateTime, nullable=True)


class ProcessingWasteRecord(Base, BranchScopedMixin):
    __tablename__ = "processing_waste_records"

    id                = Column(String, primary_key=True, default=erp_uuid)
    incoming_batch_id = Column(String, ForeignKey("incoming_batches.id"), nullable=False, index=True)
    processing_job_id = Column(String, ForeignKey("processing_jobs.id"), nullable=True)
    waste_type        = Column(String(128), nullable=False)
    weight_kg         = Column(Float, nullable=False)
    disposal_route    = Column(String(128), nullable=True)
    recorded_at       = Column(DateTime, default=erp_now, nullable=False)

    __table_args__ = (
        CheckConstraint("weight_kg >= 0", name="ck_pwr_wt_nonneg"),
    )


class QualityInspection(Base, BranchScopedMixin):
    __tablename__ = "quality_inspections"

    id                    = Column(String, primary_key=True, default=erp_uuid)
    incoming_batch_id     = Column(String, ForeignKey("incoming_batches.id"), nullable=True, index=True)
    processing_job_id     = Column(String, ForeignKey("processing_jobs.id"), nullable=True, index=True)
    inspector_employee_id = Column(String, ForeignKey("employees.id"), nullable=True)
    inspection_date       = Column(DateTime, default=erp_now, nullable=False)
    purity_pct            = Column(Float, nullable=True)
    contamination_pct     = Column(Float, nullable=True)
    result                = Column(String(32), default="pass", nullable=False)
    notes                 = Column(Text, nullable=True)


class MachineOperatingLog(Base, BranchScopedMixin):
    __tablename__ = "machine_operating_logs"

    id              = Column(String, primary_key=True, default=erp_uuid)
    machine_id      = Column(String, ForeignKey("machines.id"), nullable=False, index=True)
    shift_id        = Column(String, ForeignKey("employee_shifts.id"), nullable=True)
    log_date        = Column(Date, nullable=False, index=True)
    operating_hours = Column(Float, default=0.0, nullable=False)
    idle_hours      = Column(Float, default=0.0, nullable=False)
    output_kg       = Column(Float, default=0.0, nullable=False)


class MachineDowntime(Base, BranchScopedMixin):
    __tablename__ = "machine_downtime"

    id             = Column(String, primary_key=True, default=erp_uuid)
    machine_id     = Column(String, ForeignKey("machines.id"), nullable=False, index=True)
    start_time     = Column(DateTime, nullable=False)
    end_time       = Column(DateTime, nullable=True)
    downtime_hours = Column(Float, default=0.0, nullable=False)
    reason         = Column(String(256), nullable=False)
    severity       = Column(String(32), default="medium", nullable=False)


class MaintenanceSchedule(Base, BranchScopedMixin):
    __tablename__ = "maintenance_schedules"

    id             = Column(String, primary_key=True, default=erp_uuid)
    machine_id     = Column(String, ForeignKey("machines.id"), nullable=False, index=True)
    schedule_name  = Column(String(128), nullable=False)
    frequency_days = Column(Integer, default=30, nullable=False)
    next_due_date  = Column(Date, nullable=False)
    is_active      = Column(Boolean, default=True, nullable=False)


class MaintenanceRecord(Base, BranchScopedMixin):
    __tablename__ = "maintenance_records"

    id               = Column(String, primary_key=True, default=erp_uuid)
    machine_id       = Column(String, ForeignKey("machines.id"), nullable=False, index=True)
    schedule_id      = Column(String, ForeignKey("maintenance_schedules.id"), nullable=True)
    maintenance_date = Column(Date, nullable=False)
    technician       = Column(String(128), nullable=True)
    cost_amount      = Column(Float, default=0.0, nullable=False)
    findings         = Column(Text, nullable=True)
    status           = Column(String(32), default="completed", nullable=False)


class EnergyConsumptionRecord(Base, BranchScopedMixin):
    __tablename__ = "energy_consumption_records"

    id                = Column(String, primary_key=True, default=erp_uuid)
    machine_id        = Column(String, ForeignKey("machines.id"), nullable=True, index=True)
    processing_job_id = Column(String, ForeignKey("processing_jobs.id"), nullable=True)
    recorded_date     = Column(Date, nullable=False, index=True)
    kwh_consumed      = Column(Float, nullable=False)
    energy_cost       = Column(Float, default=0.0, nullable=False)
    meter_reference   = Column(String(64), nullable=True)

    __table_args__ = (
        CheckConstraint("kwh_consumed >= 0", name="ck_energy_kwh_nonneg"),
    )


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 11: TRANSPORT & LOGISTICS (8 Tables)
# ══════════════════════════════════════════════════════════════════════════════

class Transporter(Base, CompanyScopedMixin):
    __tablename__ = "transporters"

    id               = Column(String, primary_key=True, default=erp_uuid)
    transporter_code = Column(String(64), nullable=False)
    name             = Column(String(256), nullable=False)
    license_number   = Column(String(128), nullable=True)
    contact_phone    = Column(String(64), nullable=True)
    is_active        = Column(Boolean, default=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "transporter_code", name="uq_transporter_code_per_company"),
    )


class Vehicle(Base, BranchScopedMixin):
    __tablename__ = "vehicles"

    id                  = Column(String, primary_key=True, default=erp_uuid)
    transporter_id      = Column(String, ForeignKey("transporters.id"), nullable=True, index=True)
    registration_number = Column(String(64), nullable=False)
    vehicle_type        = Column(String(64), default="truck", nullable=False)
    max_payload_kg      = Column(Float, default=0.0, nullable=False)
    is_hazmat_approved  = Column(Boolean, default=False, nullable=False)
    is_active           = Column(Boolean, default=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("company_id", "registration_number", name="uq_vehicle_reg_per_company"),
    )


class Driver(Base, CompanyScopedMixin):
    __tablename__ = "drivers"

    id             = Column(String, primary_key=True, default=erp_uuid)
    transporter_id = Column(String, ForeignKey("transporters.id"), nullable=True)
    employee_id    = Column(String, ForeignKey("employees.id"), nullable=True)
    full_name      = Column(String(256), nullable=False)
    license_number = Column(String(128), nullable=False)
    phone          = Column(String(64), nullable=True)
    is_active      = Column(Boolean, default=True, nullable=False)


class TransportOrder(Base, BranchScopedMixin):
    __tablename__ = "transport_orders"

    id                   = Column(String, primary_key=True, default=erp_uuid)
    order_number         = Column(String(64), nullable=False)
    trip_purpose         = Column(String(64), nullable=False)  # supplier_pickup | incoming_transport | inter_branch_transfer | customer_delivery
    transporter_id       = Column(String, ForeignKey("transporters.id"), nullable=True)
    vehicle_id           = Column(String, ForeignKey("vehicles.id"), nullable=True)
    driver_id            = Column(String, ForeignKey("drivers.id"), nullable=True)
    incoming_batch_id    = Column(String, ForeignKey("incoming_batches.id"), nullable=True, index=True)
    sales_order_id       = Column(String, ForeignKey("sales_orders.id"), nullable=True, index=True)
    origin_location      = Column(String(256), nullable=False)
    destination_location = Column(String(256), nullable=False)
    scheduled_date       = Column(Date, nullable=False)
    status               = Column(String(32), default="scheduled", nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("company_id", "order_number", name="uq_to_number_per_company"),
    )


class TransportTripRecord(Base, BranchScopedMixin):
    __tablename__ = "transport_trip_records"

    id                 = Column(String, primary_key=True, default=erp_uuid)
    transport_order_id = Column(String, ForeignKey("transport_orders.id"), nullable=False, index=True)
    vehicle_id         = Column(String, ForeignKey("vehicles.id"), nullable=True)
    driver_id          = Column(String, ForeignKey("drivers.id"), nullable=True)
    departure_time     = Column(DateTime, nullable=True)
    arrival_time       = Column(DateTime, nullable=True)
    distance_km        = Column(Float, default=0.0, nullable=False)
    cargo_weight_kg    = Column(Float, default=0.0, nullable=False)


class TransportationExpense(Base, BranchScopedMixin):
    __tablename__ = "transportation_expenses"

    id                 = Column(String, primary_key=True, default=erp_uuid)
    transport_order_id = Column(String, ForeignKey("transport_orders.id"), nullable=False, index=True)
    expense_type       = Column(String(64), nullable=False)  # fuel | toll | freight | driver_allowance
    amount             = Column(Float, nullable=False)
    currency           = Column(String(8), default="USD", nullable=False)
    recorded_date      = Column(Date, nullable=False)

    __table_args__ = (
        CheckConstraint("amount >= 0", name="ck_trans_exp_nonneg"),
    )


class DeliveryRecord(Base, BranchScopedMixin):
    __tablename__ = "delivery_records"

    id                  = Column(String, primary_key=True, default=erp_uuid)
    transport_order_id  = Column(String, ForeignKey("transport_orders.id"), nullable=False, index=True)
    sales_order_id      = Column(String, ForeignKey("sales_orders.id"), nullable=True)
    delivered_at        = Column(DateTime, nullable=True)
    received_by         = Column(String(128), nullable=True)
    delivered_weight_kg = Column(Float, default=0.0, nullable=False)
    delivery_status     = Column(String(32), default="delivered", nullable=False)
    proof_ref           = Column(String(256), nullable=True)


class VehicleMaintenance(Base, CompanyScopedMixin):
    __tablename__ = "vehicle_maintenance"

    id           = Column(String, primary_key=True, default=erp_uuid)
    vehicle_id   = Column(String, ForeignKey("vehicles.id"), nullable=False, index=True)
    service_date = Column(Date, nullable=False)
    service_type = Column(String(64), nullable=False)
    odometer_km  = Column(Float, nullable=True)
    cost_amount  = Column(Float, default=0.0, nullable=False)
    notes        = Column(Text, nullable=True)
