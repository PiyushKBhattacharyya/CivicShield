from sqlalchemy import Column, String, Text, DateTime, ForeignKey, DECIMAL, UUID, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY
from sqlalchemy.sql import func
import uuid
from backend.database import Base

class IncidentAnalytics(Base):
    __tablename__ = "incident_analytics"
    
    analytics_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_id = Column(PG_UUID(as_uuid=True), ForeignKey("incidents.incident_id"))
    # In actual implementation, these would be INTERVAL types
    response_time = Column(String)  # Simplified for now
    resolution_time = Column(String)  # Simplified for now
    # JSONB field for flexible data storage
    resource_utilization = Column(String)  # In actual implementation, this would be JSONB
    cost_estimate = Column(DECIMAL(12,2))
    effectiveness_score = Column(DECIMAL(3,2))
    generated_at = Column(DateTime(timezone=True), server_default=func.now())

class ThreatPattern(Base):
    __tablename__ = "threat_patterns"
    
    pattern_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pattern_name = Column(String(100), nullable=False)
    pattern_description = Column(Text)
    pattern_type = Column(String(50))  # CORRELATION, ANOMALY, TREND
    detection_algorithm = Column(String(100))
    first_detected = Column(DateTime(timezone=True))
    last_seen = Column(DateTime(timezone=True))
    confidence_level = Column(DECIMAL(3,2))
    # Array of agency IDs
    affected_agencies = Column(ARRAY(UUID))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Report(Base):
    __tablename__ = "reports"
    
    report_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_title = Column(String(200), nullable=False)
    report_type = Column(String(50))  # INCIDENT_SUMMARY, COMPLIANCE, TREND_ANALYSIS, AFTER_ACTION
    generated_by = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"))
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    # JSONB field for structured report data
    report_content = Column(String)  # In actual implementation, this would be JSONB
    file_path = Column(String(255))  # Path to report file if stored externally
    access_level = Column(Integer)