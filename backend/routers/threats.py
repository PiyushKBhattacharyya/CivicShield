from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from backend import schemas, models
from backend.database import get_db
from backend.routers.users import get_current_user

router = APIRouter(prefix="/api/v1/threats", tags=["threats"])

@router.post("/", response_model=schemas.ThreatResponse)
def create_threat(
    threat: schemas.ThreatCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new threat."""
    db_threat = models.Threat(
        threat_id=uuid.uuid4(),
        threat_type=threat.threat_type,
        threat_source=threat.threat_source,
        threat_title=threat.threat_title,
        threat_description=threat.threat_description,
        severity_score=threat.severity_score,
        confidence_score=threat.confidence_score,
        geolocation=threat.geolocation,
        agency_id=current_user.agency_id,
        assigned_to=current_user.user_id
    )
    
    db.add(db_threat)
    db.commit()
    db.refresh(db_threat)
    
    return db_threat

@router.get("/{threat_id}", response_model=schemas.ThreatResponse)
def read_threat(
    threat_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get threat by ID."""
    db_threat = db.query(models.Threat).filter(models.Threat.threat_id == threat_id).first()
    if not db_threat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Threat not found"
        )
    
    # Check if user has permission to access this threat
    if current_user.agency_id != db_threat.agency_id and current_user.security_clearance_level < 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this threat"
        )
    
    return db_threat

@router.get("/", response_model=List[schemas.ThreatResponse])
def read_threats(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get list of threats."""
    # If user has high clearance, show all threats
    if current_user.security_clearance_level >= 3:
        threats = db.query(models.Threat).offset(skip).limit(limit).all()
    else:
        # Otherwise, only show threats from user's agency
        threats = db.query(models.Threat).filter(
            models.Threat.agency_id == current_user.agency_id
        ).offset(skip).limit(limit).all()
    
    return threats

@router.put("/{threat_id}", response_model=schemas.ThreatResponse)
def update_threat(
    threat_id: uuid.UUID,
    threat_update: schemas.ThreatUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update threat information."""
    db_threat = db.query(models.Threat).filter(models.Threat.threat_id == threat_id).first()
    if not db_threat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Threat not found"
        )
    
    # Check if user has permission to update this threat
    if current_user.agency_id != db_threat.agency_id and current_user.security_clearance_level < 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this threat"
        )
    
    # Update threat fields
    update_data = threat_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_threat, key, value)
    
    db.commit()
    db.refresh(db_threat)
    
    return db_threat

@router.delete("/{threat_id}")
def delete_threat(
    threat_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete threat."""
    db_threat = db.query(models.Threat).filter(models.Threat.threat_id == threat_id).first()
    if not db_threat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Threat not found"
        )
    
    # Check if user has permission to delete this threat
    if current_user.agency_id != db_threat.agency_id and current_user.security_clearance_level < 4:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this threat"
        )
    
    db.delete(db_threat)
    db.commit()
    
    return {"message": "Threat deleted successfully"}