import asyncio
import json
import logging
import websockets
from typing import Dict, Any, Callable
from datetime import datetime
import uuid
from sqlalchemy.orm import Session

# Import data ingestion service
from backend.services.data_ingestion import DataIngestionService
from backend.database import get_db

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StreamingService:
    def __init__(self):
        """
        Initialize the streaming service
        """
        self.data_ingestion_service = DataIngestionService()
        self.connected_clients = set()
        self.db = next(get_db())
        logger.info("Streaming service initialized")
    
    async def register_client(self, websocket):
        """
        Register a new client connection
        """
        self.connected_clients.add(websocket)
        logger.info(f"Client registered: {websocket.remote_address}")
    
    async def unregister_client(self, websocket):
        """
        Unregister a client connection
        """
        self.connected_clients.discard(websocket)
        logger.info(f"Client unregistered: {websocket.remote_address}")
    
    async def process_websocket_data(self, websocket, path):
        """
        Process incoming WebSocket data
        """
        await self.register_client(websocket)
        
        try:
            async for message in websocket:
                try:
                    # Parse the incoming message
                    data = json.loads(message)
                    data_type = data.get("type")
                    
                    # Process based on data type
                    if data_type == "threat_report":
                        result = await self.data_ingestion_service.process_threat_report(
                            data.get("payload", {}), self.db
                        )
                    elif data_type == "sensor_data":
                        result = await self.data_ingestion_service.process_sensor_data(
                            data.get("payload", []), self.db
                        )
                    elif data_type == "social_media":
                        result = await self.data_ingestion_service.process_social_media_data(
                            data.get("payload", []), self.db
                        )
                    elif data_type == "emergency_call":
                        result = await self.data_ingestion_service.process_emergency_call_data(
                            data.get("payload", {}), self.db
                        )
                    else:
                        result = {"status": "error", "message": f"Unknown data type: {data_type}"}
                    
                    # Send response back to client
                    await websocket.send(json.dumps(result))
                    
                except json.JSONDecodeError as e:
                    error_response = {
                        "status": "error",
                        "message": f"Invalid JSON: {str(e)}"
                    }
                    await websocket.send(json.dumps(error_response))
                except Exception as e:
                    error_response = {
                        "status": "error",
                        "message": f"Processing error: {str(e)}"
                    }
                    await websocket.send(json.dumps(error_response))
        
        except websockets.exceptions.ConnectionClosed:
            logger.info("WebSocket connection closed")
        except Exception as e:
            logger.error(f"WebSocket error: {str(e)}")
        finally:
            await self.unregister_client(websocket)
    
    async def broadcast_message(self, message: Dict[str, Any]):
        """
        Broadcast a message to all connected clients
        """
        if self.connected_clients:
            # Convert message to JSON
            message_json = json.dumps(message)
            
            # Send to all connected clients
            await asyncio.gather(
                *[client.send(message_json) for client in self.connected_clients],
                return_exceptions=True
            )
    
    async def start_websocket_server(self, host: str = "localhost", port: int = 8765):
        """
        Start the WebSocket server
        """
        logger.info(f"Starting WebSocket server on {host}:{port}")
        
        server = await websockets.serve(
            self.process_websocket_data,
            host,
            port
        )
        
        return server
    
    async def process_mqtt_message(self, topic: str, payload: bytes):
        """
        Process an MQTT message
        """
        try:
            # Parse payload
            data = json.loads(payload.decode())
            
            # Process based on topic
            if topic.startswith("sensors/"):
                # Sensor data
                sensor_data = [{
                    "sensor_id": topic.split("/")[-1],  # Use last part of topic as sensor ID
                    "timestamp": datetime.utcnow(),
                    "data": data
                }]
                
                result = await self.data_ingestion_service.process_sensor_data(
                    sensor_data, self.db
                )
                
                logger.info(f"Processed MQTT sensor data: {result}")
                
            elif topic.startswith("threats/"):
                # Threat report
                result = await self.data_ingestion_service.process_threat_report(
                    data, self.db
                )
                
                logger.info(f"Processed MQTT threat report: {result}")
                
                # Broadcast threat alert to connected clients
                if result["status"] == "success":
                    alert_message = {
                        "type": "threat_alert",
                        "threat_id": result["threat_id"],
                        "message": "New threat detected",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    await self.broadcast_message(alert_message)
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in MQTT message: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing MQTT message: {str(e)}")
    
    async def simulate_data_stream(self):
        """
        Simulate a data stream for testing purposes
        """
        logger.info("Starting data stream simulation")
        
        # Simulate sensor data
        sensor_data = {
            "temperature": 25.5,
            "humidity": 60.2,
            "pressure": 1013.25
        }
        
        # Simulate threat report
        threat_report = {
            "threat_title": "Simulated Network Anomaly",
            "threat_description": "Simulated network traffic anomaly detected",
            "threat_type": "cyber",
            "threat_source": "network_monitoring",
            "severity_score": 7.5,
            "confidence_score": 8.0,
            "geolocation": "192.168.1.100"
        }
        
        while True:
            try:
                # Send sensor data every 5 seconds
                sensor_message = {
                    "type": "sensor_data",
                    "payload": [{
                        "sensor_id": "00000000-0000-0000-0000-000000000001",
                        "timestamp": datetime.utcnow().isoformat(),
                        "data": sensor_data
                    }]
                }
                
                # Broadcast to connected clients
                await self.broadcast_message(sensor_message)
                
                # Send threat report every 30 seconds
                if datetime.utcnow().second % 30 == 0:
                    threat_message = {
                        "type": "threat_alert",
                        "payload": threat_report,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    
                    # Broadcast to connected clients
                    await self.broadcast_message(threat_message)
                
                # Wait before sending next message
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"Error in data stream simulation: {str(e)}")
                await asyncio.sleep(5)

# Example usage
async def main():
    """
    Example usage of the streaming service
    """
    # Initialize service
    service = StreamingService()
    
    # Start WebSocket server
    server = await service.start_websocket_server()
    
    # Start data stream simulation
    stream_task = asyncio.create_task(service.simulate_data_stream())
    
    logger.info("Streaming service started")
    
    # Keep the server running
    try:
        await asyncio.gather(
            server.wait_closed(),
            stream_task
        )
    except KeyboardInterrupt:
        logger.info("Shutting down streaming service")
        server.close()
        await server.wait_closed()

if __name__ == "__main__":
    # Run example
    asyncio.run(main())