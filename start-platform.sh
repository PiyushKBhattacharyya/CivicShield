#!/bin/bash

# CivicShield Platform Startup Script

echo "🚀 Starting CivicShield Platform..."

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "❌ Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null
then
    echo "❌ Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

# Check if repository is cloned
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found. Please run this script from the CivicShield root directory."
    echo "💡 Clone the repository first: git clone https://github.com/your-org/civicshield.git"
    exit 1
fi

# Pull latest images
echo "📥 Pulling latest Docker images..."
docker-compose pull

# Start services
echo "⚡ Starting platform services..."
docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to initialize..."
sleep 30

# Check service status
echo "📋 Checking service status..."
docker-compose ps

echo ""
echo "✅ CivicShield Platform is now running!"
echo ""
echo "🌍 Access the platform at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo ""
echo "🔐 Default login credentials:"
echo "   Username: admin@civicshield.gov"
echo "   Password: Admin123!"
echo ""
echo "📖 For more information, visit: https://github.com/your-org/civicshield"
echo ""
echo "💡 To stop the platform, run: docker-compose down"