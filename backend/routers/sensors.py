from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime

from backend import schemas, models
from backend.database import get_db
from backend.routers.users import get_current_user

router = APIRouter(prefix="/api/v1/sensors", tags=["sensors"])

@router.post("/", response_model=schemas.SensorResponse)
def create_sensor(
    sensor: schemas.SensorCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new sensor."""
    # Check if user has permission to create sensors
    if current_user.security_clearance_level < 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to create sensors"
        )
    
    db_sensor = models.Sensor(
        sensor_id=uuid.uuid4(),
        sensor_name=sensor.sensor_name,
        sensor_type=sensor.sensor_type,
        location=sensor.location,
        agency_id=sensor.agency_id or current_user.agency_id,
        installation_date=datetime.utcnow()
    )
    
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    
    return db_sensor

@router.get("/{sensor_id}", response_model=schemas.SensorResponse)
def read_sensor(
    sensor_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get sensor by ID."""
    db_sensor = db.query(models.Sensor).filter(models.Sensor.sensor_id == sensor_id).first()
    if not db_sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor not found"
        )
    
    # Check if user has permission to access this sensor
    if current_user.agency_id != db_sensor.agency_id and current_user.security_clearance_level < 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this sensor"
        )
    
    return db_sensor

@router.get("/", response_model=List[schemas.SensorResponse])
def read_sensors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get list of sensors."""
    # If user has high clearance, show all sensors
    if current_user.security_clearance_level >= 3:
        sensors = db.query(models.Sensor).offset(skip).limit(limit).all()
    else:
        # Otherwise, only show sensors from user's agency
        sensors = db.query(models.Sensor).filter(
            models.Sensor.agency_id == current_user.agency_id
        ).offset(skip).limit(limit).all()
    
    return sensors

@router.put("/{sensor_id}", response_model=schemas.SensorResponse)
def update_sensor(
    sensor_id: uuid.UUID,
    sensor_update: schemas.SensorUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update sensor information."""
    db_sensor = db.query(models.Sensor).filter(models.Sensor.sensor_id == sensor_id).first()
    if not db_sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor not found"
        )
    
    # Check if user has permission to update this sensor
    if current_user.agency_id != db_sensor.agency_id and current_user.security_clearance_level < 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this sensor"
        )
    
    # Update sensor fields
    update_data = sensor_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_sensor, key, value)
    
    db.commit()
    db.refresh(db_sensor)
    
    return db_sensor

@router.delete("/{sensor_id}")
def delete_sensor(
    sensor_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete sensor."""
    db_sensor = db.query(models.Sensor).filter(models.Sensor.sensor_id == sensor_id).first()
    if not db_sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor not found"
        )
    
    # Check if user has permission to delete this sensor
    if current_user.agency_id != db_sensor.agency_id and current_user.security_clearance_level < 4:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this sensor"
        )
    
    db.delete(db_sensor)
    db.commit()
    
    return {"message": "Sensor deleted successfully"}

@router.post("/{sensor_id}/data", response_model=schemas.SensorDataResponse)
def create_sensor_data(
    sensor_id: uuid.UUID,
    sensor_data: schemas.SensorDataCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create new sensor data."""
    # Check if sensor exists
    db_sensor = db.query(models.Sensor).filter(models.Sensor.sensor_id == sensor_id).first()
    if not db_sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sensor not found"
        )
    
    # Check if user has permission to create data for this sensor
    if current_user.agency_id != db_sensor.agency_id and current_user.security_clearance_level < 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to create data for this sensor"
        )
    
    # In a real implementation, we would use TimescaleDB for sensor data
    # For now, we'll use a simplified approach
    db_sensor_data = models.SensorData(
        sensor_id=sensor_id,
        timestamp=sensor_data.timestamp,
        data=str(sensor_data.data),  # Simplified storage
        processed=sensor_data.processed
    )
    
    db.add(db_sensor_data)
    db.commit()
    db.refresh(db_sensor_data)
    
    return db_sensor_data