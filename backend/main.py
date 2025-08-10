from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import routers
from backend.routers import users, threats, incidents, sensors, communication, analytics, data_ingestion

# Initialize FastAPI app
app = FastAPI(
    title="CivicShield API",
    description="AI-Driven Threat Detection & Crisis Management Platform API",
    version="1.0.0"
)

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(threats.router, prefix="/api/v1/threats", tags=["threats"])
app.include_router(incidents.router, prefix="/api/v1/incidents", tags=["incidents"])
app.include_router(sensors.router, prefix="/api/v1/sensors", tags=["sensors"])
app.include_router(communication.router, prefix="/api/v1/communication", tags=["communication"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(data_ingestion.router, prefix="/api/v1/data", tags=["data ingestion"])

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "CivicShield API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)