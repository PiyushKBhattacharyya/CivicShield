from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime

from backend import schemas, models
from backend.database import get_db
from backend.routers.users import get_current_user

router = APIRouter(prefix="/api/v1/incidents", tags=["incidents"])

@router.post("/", response_model=schemas.IncidentResponse)
def create_incident(
    incident: schemas.IncidentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new incident."""
    db_incident = models.Incident(
        incident_id=uuid.uuid4(),
        incident_title=incident.incident_title,
        incident_description=incident.incident_description,
        incident_type=incident.incident_type,
        severity_level=incident.severity_level,
        priority_level=incident.priority_level,
        status=incident.status or "OPEN",
        geolocation=incident.geolocation,
        reported_at=datetime.utcnow(),
        created_by=current_user.user_id,
        agency_id=current_user.agency_id,
        assigned_to=current_user.user_id
    )
    
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    
    return db_incident

@router.get("/{incident_id}", response_model=schemas.IncidentResponse)
def read_incident(
    incident_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get incident by ID."""
    db_incident = db.query(models.Incident).filter(models.Incident.incident_id == incident_id).first()
    if not db_incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found"
        )
    
    # Check if user has permission to access this incident
    if current_user.agency_id != db_incident.agency_id and current_user.security_clearance_level < 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this incident"
        )
    
    return db_incident

@router.get("/", response_model=List[schemas.IncidentResponse])
def read_incidents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get list of incidents."""
    # If user has high clearance, show all incidents
    if current_user.security_clearance_level >= 3:
        incidents = db.query(models.Incident).offset(skip).limit(limit).all()
    else:
        # Otherwise, only show incidents from user's agency
        incidents = db.query(models.Incident).filter(
            models.Incident.agency_id == current_user.agency_id
        ).offset(skip).limit(limit).all()
    
    return incidents

@router.put("/{incident_id}", response_model=schemas.IncidentResponse)
def update_incident(
    incident_id: uuid.UUID,
    incident_update: schemas.IncidentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Update incident information."""
    db_incident = db.query(models.Incident).filter(models.Incident.incident_id == incident_id).first()
    if not db_incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found"
        )
    
    # Check if user has permission to update this incident
    if current_user.agency_id != db_incident.agency_id and current_user.security_clearance_level < 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update this incident"
        )
    
    # Update incident fields
    update_data = incident_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_incident, key, value)
    
    # Update the updated_at timestamp
    db_incident.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_incident)
    
    return db_incident

@router.delete("/{incident_id}")
def delete_incident(
    incident_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Delete incident."""
    db_incident = db.query(models.Incident).filter(models.Incident.incident_id == incident_id).first()
    if not db_incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found"
        )
    
    # Check if user has permission to delete this incident
    if current_user.agency_id != db_incident.agency_id and current_user.security_clearance_level < 4:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this incident"
        )
    
    db.delete(db_incident)
    db.commit()
    
    return {"message": "Incident deleted successfully"}

@router.post("/{incident_id}/link-threat/{threat_id}", response_model=schemas.IncidentThreatResponse)
def link_incident_to_threat(
    incident_id: uuid.UUID,
    threat_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Link an incident to a threat."""
    # Check if incident exists
    db_incident = db.query(models.Incident).filter(models.Incident.incident_id == incident_id).first()
    if not db_incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found"
        )
    
    # Check if threat exists
    db_threat = db.query(models.Threat).filter(models.Threat.threat_id == threat_id).first()
    if not db_threat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Threat not found"
        )
    
    # Check if user has permission to link these entities
    if (current_user.agency_id != db_incident.agency_id or 
        current_user.agency_id != db_threat.agency_id) and current_user.security_clearance_level < 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to link these entities"
        )
    
    # Check if link already exists
    existing_link = db.query(models.IncidentThreat).filter(
        models.IncidentThreat.incident_id == incident_id,
        models.IncidentThreat.threat_id == threat_id
    ).first()
    
    if existing_link:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incident and threat are already linked"
        )
    
    # Create the link
    db_link = models.IncidentThreat(
        incident_id=incident_id,
        threat_id=threat_id,
        associated_by=current_user.user_id
    )
    
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    
    return db_link