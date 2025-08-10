from sqlalchemy import Column, String, Text, DateTime, ForeignKey, DECIMAL, UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
import uuid
from backend.database import Base

class Threat(Base):
    __tablename__ = "threats"
    
    threat_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    threat_type = Column(String(50))
    threat_source = Column(String(50))
    threat_title = Column(String(200), nullable=False)
    threat_description = Column(Text)
    severity_score = Column(DECIMAL(3,2))
    confidence_score = Column(DECIMAL(3,2))
    # Note: In actual implementation, we would use a proper geospatial column type
    geolocation = Column(String(100))  # Simplified for now
    detected_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), default="ACTIVE")
    assigned_to = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"))
    agency_id = Column(PG_UUID(as_uuid=True), ForeignKey("agencies.agency_id"))

class Incident(Base):
    __tablename__ = "incidents"
    
    incident_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_title = Column(String(200), nullable=False)
    incident_description = Column(Text)
    incident_type = Column(String(50))
    severity_level = Column(String(20))
    priority_level = Column(String(20), default="OPEN")
    status = Column(String(20), default="OPEN")
    # Note: In actual implementation, we would use a proper geospatial column type
    geolocation = Column(String(100))  # Simplified for now
    reported_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True))
    created_by = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"))
    assigned_to = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"))
    agency_id = Column(PG_UUID(as_uuid=True), ForeignKey("agencies.agency_id"))

class IncidentThreat(Base):
    __tablename__ = "incident_threats"
    
    incident_id = Column(PG_UUID(as_uuid=True), ForeignKey("incidents.incident_id"), primary_key=True)
    threat_id = Column(PG_UUID(as_uuid=True), ForeignKey("threats.threat_id"), primary_key=True)
    associated_at = Column(DateTime(timezone=True), server_default=func.now())
    associated_by = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"))