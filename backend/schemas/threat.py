from pydantic import BaseModel, Field
from typing import Optional, List, UUID
from datetime import datetime
from decimal import Decimal

class ThreatBase(BaseModel):
    threat_type: Optional[str] = Field(None, max_length=50)
    threat_source: Optional[str] = Field(None, max_length=50)
    threat_title: str = Field(..., min_length=1, max_length=200)
    threat_description: Optional[str] = None
    severity_score: Optional[Decimal] = Field(None, ge=0, le=10)
    confidence_score: Optional[Decimal] = Field(None, ge=0, le=10)
    geolocation: Optional[str] = Field(None, max_length=100)

class ThreatCreate(ThreatBase):
    pass

class ThreatUpdate(ThreatBase):
    threat_type: Optional[str] = Field(None, max_length=50)
    threat_source: Optional[str] = Field(None, max_length=50)
    threat_title: Optional[str] = Field(None, min_length=1, max_length=200)

class ThreatInDB(ThreatBase):
    threat_id: UUID
    detected_at: datetime
    created_at: datetime
    status: str = "ACTIVE"
    assigned_to: Optional[UUID] = None
    agency_id: Optional[UUID] = None

    class Config:
        orm_mode = True

class ThreatResponse(ThreatInDB):
    pass

class IncidentBase(BaseModel):
    incident_title: str = Field(..., min_length=1, max_length=200)
    incident_description: Optional[str] = None
    incident_type: Optional[str] = Field(None, max_length=50)
    severity_level: Optional[str] = Field(None, max_length=20)
    priority_level: Optional[str] = Field(None, max_length=20)
    status: Optional[str] = Field(None, max_length=20)
    geolocation: Optional[str] = Field(None, max_length=100)

class IncidentCreate(IncidentBase):
    pass

class IncidentUpdate(IncidentBase):
    incident_title: Optional[str] = Field(None, min_length=1, max_length=200)
    status: Optional[str] = Field(None, max_length=20)

class IncidentInDB(IncidentBase):
    incident_id: UUID
    reported_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None
    created_by: Optional[UUID] = None
    assigned_to: Optional[UUID] = None
    agency_id: Optional[UUID] = None

    class Config:
        orm_mode = True

class IncidentResponse(IncidentInDB):
    pass

class IncidentThreatBase(BaseModel):
    incident_id: UUID
    threat_id: UUID

class IncidentThreatCreate(IncidentThreatBase):
    associated_by: Optional[UUID] = None

class IncidentThreatInDB(IncidentThreatBase):
    associated_at: datetime
    associated_by: Optional[UUID] = None

    class Config:
        orm_mode = True

class IncidentThreatResponse(IncidentThreatInDB):
    pass