@echo off
title CivicShield Platform Startup

echo 🚀 Starting CivicShield Platform...

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker and try again.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose and try again.
    pause
    exit /b 1
)

REM Check if repository is cloned
if not exist "docker-compose.yml" (
    echo ❌ docker-compose.yml not found. Please run this script from the CivicShield root directory.
    echo 💡 Clone the repository first: git clone https://github.com/your-org/civicshield.git
    pause
    exit /b 1
)

REM Pull latest images
echo 📥 Pulling latest Docker images...
docker-compose pull

REM Start services
echo ⚡ Starting platform services...
docker-compose up -d

REM Wait for services to start
echo ⏳ Waiting for services to initialize...
timeout /t 30 /nobreak >nul

REM Check service status
echo 📋 Checking service status...
docker-compose ps

echo.
echo ✅ CivicShield Platform is now running!
echo.
echo 🌍 Access the platform at:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000
echo    API Documentation: http://localhost:8000/docs
echo.
echo 🔐 Default login credentials:
echo    Username: admin@civicshield.gov
echo    Password: Admin123!
echo.
echo 📖 For more information, visit: https://github.com/your-org/civicshield
echo.
echo 💡 To stop the platform, run: docker-compose down
echo.
pause