"""
E-Waste AI — Industrial Waste Batch ORM Models
================================================
SQLAlchemy models for the full industrial workflow:
Intake → Classification → Recovery → Valuation
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base
from backend.models.base import TimestampMixin


class WasteBatch(Base, TimestampMixin):
    """Incoming e-waste batch registration."""
    __tablename__ = "waste_batches"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    batch_code      = Column(String(50), unique=True, nullable=False, index=True)
    source_name     = Column(String(500), nullable=True)
    source_type     = Column(String(50), nullable=True)  # corporate|household|municipal|retail|government
    source_contact  = Column(String(255), nullable=True)
    received_date   = Column(Date, nullable=False)
    total_weight_kg = Column(Float, nullable=True)
    item_count      = Column(Integer, nullable=True)
    location_code   = Column(String(100), nullable=True)  # storage bay/rack code
    notes           = Column(Text, nullable=True)
    status          = Column(String(50), default="received", nullable=False, index=True)
    # Status: received|sorting|classified|processing|completed|disposed

    items            = relationship("BatchItem", back_populates="batch", cascade="all, delete-orphan")
    economic_records = relationship("EconomicValuation", back_populates="batch", cascade="all, delete-orphan")
    operational_costs= relationship("OperationalCost", back_populates="batch", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<WasteBatch code={self.batch_code} items={self.item_count} status={self.status}>"


class BatchItem(Base, TimestampMixin):
    """Individual items within a waste batch."""
    __tablename__ = "batch_items"

    id            = Column(Integer, primary_key=True, autoincrement=True)
    batch_id      = Column(Integer, ForeignKey("waste_batches.id"), nullable=False, index=True)
    item_code     = Column(String(100), unique=True, nullable=False, index=True)
    image_path    = Column(Text, nullable=True)
    weight_kg     = Column(Float, nullable=True)
    condition     = Column(String(50), nullable=True)   # working|damaged|broken|scrap
    notes         = Column(Text, nullable=True)
    status        = Column(String(50), default="pending", nullable=False)
    # Status: pending|classified|components_identified|materials_analyzed|valued|completed

    batch           = relationship("WasteBatch", back_populates="items")
    classifications = relationship("ItemClassification", back_populates="item", cascade="all, delete-orphan")
    components      = relationship("ItemComponent", back_populates="item", cascade="all, delete-orphan")
    materials       = relationship("MaterialRecovery", back_populates="item", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<BatchItem code={self.item_code} weight={self.weight_kg}kg status={self.status}>"


class ItemClassification(Base, TimestampMixin):
    """AI classification results for each batch item."""
    __tablename__ = "item_classifications"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    item_id             = Column(Integer, ForeignKey("batch_items.id"), nullable=False, index=True)
    training_run_id     = Column(Integer, nullable=True, index=True)
    device_category     = Column(String(100), nullable=True)
    device_subcategory  = Column(String(100), nullable=True)
    brand_estimate      = Column(String(100), nullable=True)
    confidence_score    = Column(Float, nullable=True)
    hazard_level        = Column(String(20), nullable=True)  # low|medium|high|critical
    hazardous_materials = Column(Text, nullable=True)        # JSON list
    top_predictions     = Column(Text, nullable=True)        # JSON [{label, confidence}]
    classified_by       = Column(String(50), default="ai")  # ai|manual|hybrid

    item = relationship("BatchItem", back_populates="classifications")

    def __repr__(self):
        return f"<ItemClassification item_id={self.item_id} category={self.device_category} conf={self.confidence_score}>"


class ItemComponent(Base, TimestampMixin):
    """Components identified within each classified item."""
    __tablename__ = "item_components"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    item_id             = Column(Integer, ForeignKey("batch_items.id"), nullable=False, index=True)
    component_name      = Column(String(255), nullable=False)
    component_category  = Column(String(100), nullable=True)  # electronic|mechanical|chemical|display
    quantity            = Column(Integer, default=1)
    weight_estimate_g   = Column(Float, nullable=True)
    condition           = Column(String(50), nullable=True)
    is_recoverable      = Column(Boolean, default=True)
    recovery_difficulty = Column(String(20), nullable=True)  # easy|medium|hard
    notes               = Column(Text, nullable=True)
    identified_by       = Column(String(50), default="system")

    item = relationship("BatchItem", back_populates="components")

    def __repr__(self):
        return f"<ItemComponent item_id={self.item_id} name={self.component_name}>"


class MaterialRecovery(Base, TimestampMixin):
    """Estimated recoverable materials per item."""
    __tablename__ = "material_recovery"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    item_id             = Column(Integer, ForeignKey("batch_items.id"), nullable=False, index=True)
    material_name       = Column(String(100), nullable=False)
    material_category   = Column(String(100), nullable=True)  # precious_metal|base_metal|polymer|rare_earth|hazardous
    estimated_weight_g  = Column(Float, nullable=True)
    actual_weight_g     = Column(Float, nullable=True)        # filled after actual recovery
    purity_percent      = Column(Float, nullable=True)
    recovery_method     = Column(String(255), nullable=True)  # hydrometallurgy|pyrometallurgy|mechanical
    recovery_efficiency = Column(Float, nullable=True)        # expected yield (0-1)
    is_estimate         = Column(Boolean, default=True)       # always flag estimates
    data_source         = Column(String(500), nullable=True)  # citation
    recovery_status     = Column(String(50), default="estimated")  # estimated|planned|in_progress|completed

    item = relationship("BatchItem", back_populates="materials")

    def __repr__(self):
        return f"<MaterialRecovery item_id={self.item_id} material={self.material_name} est={self.estimated_weight_g}g>"


class EconomicValuation(Base, TimestampMixin):
    """Economic value estimation per batch or item."""
    __tablename__ = "economic_valuations"

    id                        = Column(Integer, primary_key=True, autoincrement=True)
    batch_id                  = Column(Integer, ForeignKey("waste_batches.id"), nullable=True, index=True)
    item_id                   = Column(Integer, nullable=True, index=True)
    valuation_date            = Column(Date, nullable=False)
    total_estimated_value_usd = Column(Float, nullable=True)
    gold_value_usd            = Column(Float, nullable=True)
    silver_value_usd          = Column(Float, nullable=True)
    copper_value_usd          = Column(Float, nullable=True)
    lithium_value_usd         = Column(Float, nullable=True)
    other_metals_usd          = Column(Float, nullable=True)
    processing_cost_usd       = Column(Float, nullable=True)
    net_value_usd             = Column(Float, nullable=True)
    price_data_source         = Column(String(255), nullable=True)
    price_reference_date      = Column(Date, nullable=True)
    is_estimate               = Column(Boolean, default=True)
    notes                     = Column(Text, nullable=True)

    batch = relationship("WasteBatch", back_populates="economic_records")

    def __repr__(self):
        return f"<EconomicValuation batch_id={self.batch_id} net={self.net_value_usd} USD>"


class OperationalCost(Base, TimestampMixin):
    """Operational cost tracking per batch."""
    __tablename__ = "operational_costs"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    batch_id        = Column(Integer, ForeignKey("waste_batches.id"), nullable=False, index=True)
    cost_category   = Column(String(100), nullable=False)  # labour|transport|disposal|processing|equipment
    cost_amount_usd = Column(Float, nullable=False)
    description     = Column(Text, nullable=True)
    incurred_date   = Column(Date, nullable=True)
    recorded_by     = Column(String(255), nullable=True)

    batch = relationship("WasteBatch", back_populates="operational_costs")

    def __repr__(self):
        return f"<OperationalCost batch_id={self.batch_id} category={self.cost_category} amount={self.cost_amount_usd}>"


class EwasteCategory(Base, TimestampMixin):
    """Master list of e-waste categories used for classification."""
    __tablename__ = "ewaste_categories"

    id                  = Column(Integer, primary_key=True, autoincrement=True)
    category_code       = Column(String(100), unique=True, nullable=False, index=True)
    name                = Column(String(255), nullable=False)
    category_name       = Column(String(255), nullable=True)   # alias for compatibility
    description         = Column(Text, nullable=True)
    hazmat_level        = Column(String(20), nullable=True)
    recovery_complexity = Column(String(20), nullable=True)
    parent_category     = Column(String(100), nullable=True)
    avg_weight_kg       = Column(Float, nullable=True)
    eu_weee_category    = Column(String(100), nullable=True)
    is_active           = Column(Boolean, default=True)
    parent_category     = Column(String(100), nullable=True)
    description         = Column(Text, nullable=True)
    avg_weight_kg       = Column(Float, nullable=True)
    hazard_level        = Column(String(20), nullable=True)
    eu_weee_category    = Column(String(100), nullable=True)  # EU classification code
    is_active           = Column(Boolean, default=True)

    def __repr__(self):
        return f"<EwasteCategory code={self.category_code} name={self.category_name}>"
