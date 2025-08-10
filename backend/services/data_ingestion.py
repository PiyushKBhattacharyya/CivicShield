import asyncio
import json
import logging
from typing import Dict, Any, List
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# Import models
from backend.models.threat import Threat, SensorData
from backend.models.user import User
from backend.database import get_db

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataIngestionService:
    def __init__(self):
        """
        Initialize the data ingestion service
        """
        logger.info("Data ingestion service initialized")
    
    async def process_threat_report(self, threat_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """
        Process a threat report and store it in the database
        """
        try:
            # Create threat record
            threat = Threat(
                threat_id=uuid.uuid4(),
                threat_title=threat_data.get("threat_title", ""),
                threat_description=threat_data.get("threat_description", ""),
                threat_type=threat_data.get("threat_type", ""),
                threat_source=threat_data.get("threat_source", ""),
                severity_score=threat_data.get("severity_score", 0.0),
                confidence_score=threat_data.get("confidence_score", 0.0),
                geolocation=threat_data.get("geolocation", ""),
                created_at=threat_data.get("created_at", datetime.utcnow()),
                agency_id=threat_data.get("agency_id")
            )
            
            db.add(threat)
            db.commit()
            db.refresh(threat)
            
            logger.info(f"Threat report processed: {threat.threat_id}")
            
            return {
                "status": "success",
                "threat_id": str(threat.threat_id),
                "message": "Threat report processed successfully"
            }
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error processing threat report: {str(e)}")
            return {
                "status": "error",
                "message": f"Database error: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Error processing threat report: {str(e)}")
            return {
                "status": "error",
                "message": f"Processing error: {str(e)}"
            }
    
    async def process_sensor_data(self, sensor_data: List[Dict[str, Any]], db: Session) -> Dict[str, Any]:
        """
        Process sensor data and store it in the database
        """
        try:
            processed_count = 0
            errors = []
            
            for data_point in sensor_data:
                try:
                    # Create sensor data record
                    sensor_record = SensorData(
                        sensor_id=data_point.get("sensor_id"),
                        timestamp=data_point.get("timestamp"),
                        data=json.dumps(data_point.get("data", {})),
                        processed=False
                    )
                    
                    db.add(sensor_record)
                    processed_count += 1
                    
                except Exception as e:
                    errors.append(f"Error processing data point: {str(e)}")
                    logger.error(f"Error processing sensor data point: {str(e)}")
            
            db.commit()
            
            logger.info(f"Processed {processed_count} sensor data points")
            
            return {
                "status": "success",
                "processed_count": processed_count,
                "errors": errors,
                "message": f"Processed {processed_count} sensor data points"
            }
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Database error processing sensor data: {str(e)}")
            return {
                "status": "error",
                "message": f"Database error: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Error processing sensor data: {str(e)}")
            return {
                "status": "error",
                "message": f"Processing error: {str(e)}"
            }
    
    async def process_social_media_data(self, social_data: List[Dict[str, Any]], db: Session) -> Dict[str, Any]:
        """
        Process social media data for threat analysis
        """
        try:
            # This would typically involve:
            # 1. Filtering and cleaning the data
            # 2. Running sentiment analysis
            # 3. Detecting threat keywords
            # 4. Creating threat reports for flagged content
            
            threat_reports = []
            
            for post in social_data:
                # Simple threat keyword detection
                content = post.get("content", "").lower()
                threat_keywords = ["attack", "bomb", "threat", "danger", "emergency", "violence"]
                
                if any(keyword in content for keyword in threat_keywords):
                    # Create a threat report for this post
                    threat_report = {
                        "threat_title": f"Social Media Threat: {post.get('platform', 'Unknown')}",
                        "threat_description": f"Potential threat detected in social media post: {content[:100]}...",
                        "threat_type": "social_media",
                        "threat_source": post.get("platform", "social_media"),
                        "severity_score": 7.0 if "bomb" in content or "attack" in content else 5.0,
                        "confidence_score": 8.0,
                        "geolocation": post.get("location", ""),
                        "created_at": post.get("timestamp", datetime.utcnow()),
                        "agency_id": post.get("agency_id")
                    }
                    
                    result = await self.process_threat_report(threat_report, db)
                    if result["status"] == "success":
                        threat_reports.append(result["threat_id"])
            
            logger.info(f"Processed social media data and created {len(threat_reports)} threat reports")
            
            return {
                "status": "success",
                "threat_reports_created": len(threat_reports),
                "threat_report_ids": threat_reports,
                "message": f"Processed social media data and created {len(threat_reports)} threat reports"
            }
        except Exception as e:
            logger.error(f"Error processing social media data: {str(e)}")
            return {
                "status": "error",
                "message": f"Processing error: {str(e)}"
            }
    
    async def process_emergency_call_data(self, call_data: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """
        Process emergency call data
        """
        try:
            # Create a threat/incident report from the emergency call
            threat_report = {
                "threat_title": f"Emergency Call: {call_data.get('emergency_type', 'Unknown')}",
                "threat_description": f"Emergency call received: {call_data.get('description', '')}",
                "threat_type": "emergency_call",
                "threat_source": "emergency_services",
                "severity_score": 9.0,  # Emergency calls are typically high severity
                "confidence_score": 10.0,  # High confidence as this is a real emergency call
                "geolocation": call_data.get("location", ""),
                "created_at": call_data.get("timestamp", datetime.utcnow()),
                "agency_id": call_data.get("agency_id")
            }
            
            result = await self.process_threat_report(threat_report, db)
            
            logger.info("Emergency call data processed")
            
            return {
                "status": "success",
                "threat_report_result": result,
                "message": "Emergency call data processed successfully"
            }
        except Exception as e:
            logger.error(f"Error processing emergency call data: {str(e)}")
            return {
                "status": "error",
                "message": f"Processing error: {str(e)}"
            }
    
    async def batch_process_data(self, data_batches: Dict[str, Any], db: Session) -> Dict[str, Any]:
        """
        Process multiple data batches in a single operation
        """
        results = {}
        
        # Process threat reports
        if "threats" in data_batches:
            results["threats"] = await self.process_threat_report(data_batches["threats"], db)
        
        # Process sensor data
        if "sensor_data" in data_batches:
            results["sensor_data"] = await self.process_sensor_data(data_batches["sensor_data"], db)
        
        # Process social media data
        if "social_media" in data_batches:
            results["social_media"] = await self.process_social_media_data(data_batches["social_media"], db)
        
        # Process emergency call data
        if "emergency_calls" in data_batches:
            results["emergency_calls"] = await self.process_emergency_call_data(data_batches["emergency_calls"], db)
        
        logger.info("Batch data processing completed")
        
        return {
            "status": "completed",
            "results": results,
            "message": "Batch data processing completed"
        }

# Example usage
async def main():
    """
    Example usage of the data ingestion service
    """
    # Initialize service
    service = DataIngestionService()
    
    # Get database session
    db = next(get_db())
    
    # Example threat data
    threat_data = {
        "threat_title": "Network Intrusion Detected",
        "threat_description": "Unauthorized access attempt detected on government network",
        "threat_type": "cyber",
        "threat_source": "network_monitoring",
        "severity_score": 8.5,
        "confidence_score": 9.0,
        "geolocation": "192.168.1.100",
        "agency_id": "00000000-0000-0000-0000-000000000001"
    }
    
    # Process threat report
    result = await service.process_threat_report(threat_data, db)
    print(f"Threat processing result: {result}")
    
    # Example sensor data
    sensor_data = [
        {
            "sensor_id": "00000000-0000-0000-0000-000000000002",
            "timestamp": datetime.utcnow(),
            "data": {
                "temperature": 25.5,
                "humidity": 60.2,
                "pressure": 1013.25
            }
        }
    ]
    
    # Process sensor data
    result = await service.process_sensor_data(sensor_data, db)
    print(f"Sensor data processing result: {result}")

if __name__ == "__main__":
    # Run example
    asyncio.run(main())