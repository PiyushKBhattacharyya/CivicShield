from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class IncidentAnalyticsBase(BaseModel):
    incident_id: Optional[UUID] = None
    response_time: Optional[str] = None
    resolution_time: Optional[str] = None
    resource_utilization: Optional[Dict[str, Any]] = None
    cost_estimate: Optional[float] = None
    effectiveness_score: Optional[float] = Field(None, ge=0, le=10)

class IncidentAnalyticsCreate(IncidentAnalyticsBase):
    incident_id: UUID

class IncidentAnalyticsUpdate(IncidentAnalyticsBase):
    response_time: Optional[str] = None
    resolution_time: Optional[str] = None
    resource_utilization: Optional[Dict[str, Any]] = None
    cost_estimate: Optional[float] = None
    effectiveness_score: Optional[float] = Field(None, ge=0, le=10)

class IncidentAnalyticsInDB(IncidentAnalyticsBase):
    analytics_id: UUID
    generated_at: datetime

    class Config:
        orm_mode = True

class IncidentAnalyticsResponse(IncidentAnalyticsInDB):
    pass

class ThreatPatternBase(BaseModel):
    pattern_name: str = Field(..., min_length=1, max_length=100)
    pattern_description: Optional[str] = None
    pattern_type: Optional[str] = Field(None, max_length=50)
    detection_algorithm: Optional[str] = Field(None, max_length=100)
    confidence_level: Optional[float] = Field(None, ge=0, le=10)
    affected_agencies: Optional[List[UUID]] = None

class ThreatPatternCreate(ThreatPatternBase):
    pass

class ThreatPatternUpdate(ThreatPatternBase):
    pattern_name: Optional[str] = Field(None, min_length=1, max_length=100)
    pattern_type: Optional[str] = Field(None, max_length=50)
    confidence_level: Optional[float] = Field(None, ge=0, le=10)

class ThreatPatternInDB(ThreatPatternBase):
    pattern_id: UUID
    first_detected: datetime
    last_seen: Optional[datetime] = None
    created_at: datetime

    class Config:
        orm_mode = True

class ThreatPatternResponse(ThreatPatternInDB):
    pass

class ReportBase(BaseModel):
    report_title: str = Field(..., min_length=1, max_length=200)
    report_type: Optional[str] = Field(None, max_length=50)
    report_content: Optional[Dict[str, Any]] = None
    file_path: Optional[str] = Field(None, max_length=255)
    access_level: Optional[int] = Field(None, ge=1, le=4)

class ReportCreate(ReportBase):
    pass

class ReportUpdate(ReportBase):
    report_title: Optional[str] = Field(None, min_length=1, max_length=200)
    report_type: Optional[str] = Field(None, max_length=50)
    access_level: Optional[int] = Field(None, ge=1, le=4)

class ReportInDB(ReportBase):
    report_id: UUID
    generated_by: Optional[UUID] = None
    generated_at: datetime

    class Config:
        orm_mode = True

class ReportResponse(ReportInDB):
    pass