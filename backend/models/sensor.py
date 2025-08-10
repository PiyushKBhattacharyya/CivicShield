from sqlalchemy import Column, String, DateTime, ForeignKey, UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
import uuid
from backend.database import Base

class Sensor(Base):
    __tablename__ = "sensors"
    
    sensor_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_name = Column(String(100), nullable=False)
    sensor_type = Column(String(50))
    # Note: In actual implementation, we would use a proper geospatial column type
    location = Column(String(100))  # Simplified for now
    installation_date = Column(DateTime(timezone=True))
    last_maintenance_date = Column(DateTime(timezone=True))
    status = Column(String(20), default="ACTIVE")
    agency_id = Column(PG_UUID(as_uuid=True), ForeignKey("agencies.agency_id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Note: The SensorData model would typically be implemented with TimescaleDB
# This is a simplified version for the SQLAlchemy model
class SensorData(Base):
    __tablename__ = "sensor_data"
    
    # Composite primary key
    sensor_id = Column(PG_UUID(as_uuid=True), ForeignKey("sensors.sensor_id"), primary_key=True)
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    # JSONB field for flexible data storage
    data = Column(String)  # In actual implementation, this would be JSONB
    processed = Column(Boolean, default=False)