from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.sql import func
from db.database import Base

class SupplyEvent(Base):
    __tablename__ = "supply_events"
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(100))
    location = Column(String(200))
    severity = Column(String(20))
    description = Column(Text)
    affected_commodities = Column(JSON)
    source_url = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    country = Column(String(100))
    commodity = Column(String(100))
    lead_time_days = Column(Integer)
    reliability_score = Column(Float)
    price_per_unit = Column(Float)
    unit = Column(String(50))
    contact_info = Column(JSON)
    is_active = Column(Integer, default=1)

class InventorySnapshot(Base):
    __tablename__ = "inventory_snapshots"
    id = Column(Integer, primary_key=True, index=True)
    commodity = Column(String(100))
    quantity_available = Column(Float)
    unit = Column(String(50))
    weeks_of_stock = Column(Float)
    reorder_point = Column(Float)
    snapshot_date = Column(DateTime, server_default=func.now())

class WorkflowLog(Base):
    __tablename__ = "workflow_logs"
    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(String(100))
    agent_name = Column(String(100))
    action = Column(String(200))
    input_data = Column(JSON)
    output_data = Column(JSON)
    duration_ms = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())