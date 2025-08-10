from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class SensorBase(BaseModel):
    sensor_name: str = Field(..., min_length=1, max_length=100)
    sensor_type: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=100)

class SensorCreate(SensorBase):
    agency_id: Optional[UUID] = None

class SensorUpdate(SensorBase):
    sensor_name: Optional[str] = Field(None, min_length=1, max_length=100)
    sensor_type: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field(None, max_length=20)

class SensorInDB(SensorBase):
    sensor_id: UUID
    installation_date: Optional[datetime] = None
    last_maintenance_date: Optional[datetime] = None
    status: str = "ACTIVE"
    agency_id: Optional[UUID] = None
    created_at: datetime

    class Config:
        orm_mode = True

class SensorResponse(SensorInDB):
    pass

class SensorDataBase(BaseModel):
    sensor_id: UUID
    timestamp: datetime
    data: Optional[Dict[str, Any]] = None
    processed: bool = False

class SensorDataCreate(SensorDataBase):
    pass

class SensorDataUpdate(BaseModel):
    processed: Optional[bool] = None

class SensorDataInDB(SensorDataBase):
    pass

    class Config:
        orm_mode = True

class SensorDataResponse(SensorDataInDB):
    pass