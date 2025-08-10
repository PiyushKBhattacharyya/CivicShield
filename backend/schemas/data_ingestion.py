from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

class ThreatCreate(BaseModel):
    threat_title: str = Field(..., min_length=1, max_length=200)
    threat_description: str = Field(..., min_length=1)
    threat_type: str = Field(..., min_length=1, max_length=50)
    threat_source: str = Field(..., min_length=1, max_length=50)
    severity_score: float = Field(..., ge=0, le=10)
    confidence_score: float = Field(..., ge=0, le=10)
    geolocation: Optional[str] = Field(None, max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ThreatUpdate(ThreatCreate):
    threat_title: Optional[str] = Field(None, min_length=1, max_length=200)
    threat_description: Optional[str] = Field(None, min_length=1)
    threat_type: Optional[str] = Field(None, min_length=1, max_length=50)
    threat_source: Optional[str] = Field(None, min_length=1, max_length=50)
    severity_score: Optional[float] = Field(None, ge=0, le=10)
    confidence_score: Optional[float] = Field(None, ge=0, le=10)

class SensorDataCreate(BaseModel):
    sensor_id: uuid.UUID
    timestamp: datetime
    data: Dict[str, Any]

class SensorDataUpdate(SensorDataCreate):
    data: Optional[Dict[str, Any]] = None

class IntelReportCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    classification: str = Field(..., min_length=1, max_length=50)
    source: str = Field(..., min_length=1, max_length=100)
    received_at: datetime = Field(default_factory=datetime.utcnow)

class EmergencyCallCreate(BaseModel):
    call_id: str = Field(..., min_length=1, max_length=100)
    caller_number: str = Field(..., min_length=1, max_length=20)
    location: str = Field(..., min_length=1, max_length=100)
    emergency_type: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=1)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SocialMediaPostCreate(BaseModel):
    post_id: str = Field(..., min_length=1, max_length=100)
    platform: str = Field(..., min_length=1, max_length=50)
    content: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1, max_length=100)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    location: Optional[str] = Field(None, max_length=100)
    sentiment: Optional[str] = Field(None, max_length=20)

class SatelliteDataCreate(BaseModel):
    image_url: str = Field(..., min_length=1, max_length=500)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    location: str = Field(..., min_length=1, max_length=100)
    resolution: str = Field(..., min_length=1, max_length=20)
    data_type: str = Field(..., min_length=1, max_length=50)