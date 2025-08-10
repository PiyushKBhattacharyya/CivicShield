from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime

from backend import schemas, models
from backend.database import get_db
from backend.routers.users import get_current_user

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])

@router.post("/incidents/{incident_id}/analytics", response_model=schemas.IncidentAnalyticsResponse)
def create_incident_analytics(
    incident_id: uuid.UUID,
    analytics: schemas.IncidentAnalyticsCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create analytics for an incident."""
    # Check if incident exists
    db_incident = db.query(models.Incident).filter(models.Incident.incident_id == incident_id).first()
    if not db_incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found"
        )
    
    # Check if user has permission to create analytics for this incident
    if (current_user.agency_id != db_incident.agency_id and 
        current_user.security_clearance_level < 3):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to create analytics for this incident"
        )
    
    # Check if analytics already exists for this incident
    existing_analytics = db.query(models.IncidentAnalytics).filter(
        models.IncidentAnalytics.incident_id == incident_id
    ).first()
    
    if existing_analytics:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Analytics already exists for this incident"
        )
    
    db_analytics = models.IncidentAnalytics(
        analytics_id=uuid.uuid4(),
        incident_id=incident_id,
        response_time=analytics.response_time,
        resolution_time=analytics.resolution_time,
        resource_utilization=str(analytics.resource_utilization),  # Simplified storage
        cost_estimate=analytics.cost_estimate,
        effectiveness_score=analytics.effectiveness_score,
        generated_at=datetime.utcnow()
    )
    
    db.add(db_analytics)
    db.commit()
    db.refresh(db_analytics)
    
    return db_analytics

@router.get("/incidents/{incident_id}/analytics", response_model=schemas.IncidentAnalyticsResponse)
def get_incident_analytics(
    incident_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get analytics for an incident."""
    # Check if incident exists
    db_incident = db.query(models.Incident).filter(models.Incident.incident_id == incident_id).first()
    if not db_incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incident not found"
        )
    
    # Check if user has permission to access analytics for this incident
    if (current_user.agency_id != db_incident.agency_id and 
        current_user.security_clearance_level < 3):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access analytics for this incident"
        )
    
    db_analytics = db.query(models.IncidentAnalytics).filter(
        models.IncidentAnalytics.incident_id == incident_id
    ).first()
    
    if not db_analytics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analytics not found for this incident"
        )
    
    return db_analytics

@router.post("/reports", response_model=schemas.ReportResponse)
def create_report(
    report: schemas.ReportCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new report."""
    # Check if user has permission to create reports
    if current_user.security_clearance_level < 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to create reports"
        )
    
    db_report = models.Report(
        report_id=uuid.uuid4(),
        report_title=report.report_title,
        report_type=report.report_type,
        report_content=str(report.report_content),  # Simplified storage
        file_path=report.file_path,
        access_level=report.access_level,
        generated_by=current_user.user_id
    )
    
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    return db_report

@router.get("/reports/{report_id}", response_model=schemas.ReportResponse)
def get_report(
    report_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get a report by ID."""
    db_report = db.query(models.Report).filter(models.Report.report_id == report_id).first()
    if not db_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )
    
    # Check if user has permission to access this report
    if (current_user.user_id != db_report.generated_by and 
        current_user.security_clearance_level < db_report.access_level):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this report"
        )
    
    return db_report

@router.get("/reports", response_model=List[schemas.ReportResponse])
def get_reports(
    skip: int = 0,
    limit: int = 100,
    report_type: str = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get reports."""
    query = db.query(models.Report)
    
    # Filter by report type if provided
    if report_type:
        query = query.filter(models.Report.report_type == report_type)
    
    # If user has high clearance, show all reports they have access to
    if current_user.security_clearance_level >= 4:
        reports = query.offset(skip).limit(limit).all()
    else:
        # Otherwise, only show reports generated by user or with appropriate access level
        reports = query.filter(
            (models.Report.generated_by == current_user.user_id) |
            (models.Report.access_level <= current_user.security_clearance_level)
        ).offset(skip).limit(limit).all()
    
    return reports

@router.get("/threat-patterns", response_model=List[schemas.ThreatPatternResponse])
def get_threat_patterns(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get threat patterns."""
    # Check if user has permission to access threat patterns
    if current_user.security_clearance_level < 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access threat patterns"
        )
    
    threat_patterns = db.query(models.ThreatPattern).offset(skip).limit(limit).all()
    return threat_patterns

@router.post("/threat-patterns", response_model=schemas.ThreatPatternResponse)
def create_threat_pattern(
    threat_pattern: schemas.ThreatPatternCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Create a new threat pattern."""
    # Check if user has permission to create threat patterns
    if current_user.security_clearance_level < 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to create threat patterns"
        )
    
    db_threat_pattern = models.ThreatPattern(
        pattern_id=uuid.uuid4(),
        pattern_name=threat_pattern.pattern_name,
        pattern_description=threat_pattern.pattern_description,
        pattern_type=threat_pattern.pattern_type,
        detection_algorithm=threat_pattern.detection_algorithm,
        confidence_level=threat_pattern.confidence_level,
        affected_agencies=threat_pattern.affected_agencies,
        first_detected=datetime.utcnow(),
        created_at=datetime.utcnow()
    )
    
    db.add(db_threat_pattern)
    db.commit()
    db.refresh(db_threat_pattern)
    
    return db_threat_pattern