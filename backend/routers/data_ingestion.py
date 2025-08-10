from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import json
from backend.database import get_db
from backend.models.threat import Threat
from backend.models.sensor import SensorData
from backend.schemas.threat import ThreatCreate
from backend.schemas.sensor import SensorDataCreate
from backend.core.security import get_current_active_user
import uuid

router = APIRouter(prefix="/data", tags=["data ingestion"])

@router.post("/threats")
async def submit_threat_report(
    threat_data: ThreatCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Submit a threat report from any source
    """
    try:
        # Create threat record
        threat = Threat(
            threat_id=uuid.uuid4(),
            threat_title=threat_data.threat_title,
            threat_description=threat_data.threat_description,
            threat_type=threat_data.threat_type,
            threat_source=threat_data.threat_source,
            severity_score=threat_data.severity_score,
            confidence_score=threat_data.confidence_score,
            geolocation=threat_data.geolocation,
            created_at=threat_data.created_at,
            agency_id=current_user.agency_id
        )
        db.add(threat)
        db.commit()
        db.refresh(threat)
        return {"message": "Threat report submitted successfully", "threat_id": threat.threat_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error submitting threat report: {str(e)}")

@router.post("/sensors/data")
async def submit_sensor_data(
    sensor_data: SensorDataCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Submit sensor data from IoT devices
    """
    try:
        # Create sensor data record
        data = SensorData(
            sensor_id=sensor_data.sensor_id,
            timestamp=sensor_data.timestamp,
            data=json.dumps(sensor_data.data),
            processed=False
        )
        db.add(data)
        db.commit()
        return {"message": "Sensor data submitted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error submitting sensor data: {str(e)}")

@router.post("/intel/reports")
async def submit_intel_report(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Submit intelligence reports via file upload
    """
    try:
        # Save file and process content
        content = await file.read()
        # Process the intelligence report
        # This would typically involve parsing the document and extracting relevant information
        return {"message": "Intelligence report submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting intelligence report: {str(e)}")

@router.post("/emergency/calls")
async def submit_emergency_call(
    call_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Submit emergency call data
    """
    try:
        # Process emergency call data
        # This would typically involve creating an incident record
        return {"message": "Emergency call data submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting emergency call data: {str(e)}")

@router.post("/social/feed")
async def submit_social_media_data(
    social_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Submit social media data for analysis
    """
    try:
        # Process social media data
        # This would typically involve sentiment analysis and threat detection
        return {"message": "Social media data submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting social media data: {str(e)}")

@router.post("/satellite/imagery")
async def submit_satellite_data(
    satellite_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Submit satellite imagery data
    """
    try:
        # Process satellite imagery data
        # This would typically involve image analysis for threat detection
        return {"message": "Satellite data submitted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting satellite data: {str(e)}")