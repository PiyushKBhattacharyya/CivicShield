# Running the CivicShield Platform

## Overview

This document provides detailed instructions on how to set up and run the CivicShield platform in different environments. The platform can be run locally for development and testing, or deployed to a production environment using Docker Compose or Kubernetes.

## Prerequisites

Before running the platform, ensure you have the following installed:

- **Docker** (version 20.10 or higher)
- **Docker Compose** (version 1.29 or higher)
- **Git** (for cloning the repository)
- **kubectl** (for Kubernetes deployment)
- **Terraform** (for infrastructure provisioning)

For development:
- **Python** 3.9 or higher
- **Node.js** 16 or higher
- **npm** or **yarn**

## Getting the Code

First, clone the repository:

```bash
git clone https://github.com/your-org/civicshield.git
cd civicshield
```

## Local Development Setup

### Option 1: Docker Compose (Recommended for Testing)

1. **Start the platform**:
   ```bash
   docker-compose up -d
   ```

2. **Wait for services to initialize** (this may take a few minutes):
   ```bash
   docker-compose logs -f
   ```

3. **Access the services**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Database: localhost:5432
   - Redis: localhost:6379
   - Elasticsearch: http://localhost:9200

4. **Stop the platform**:
   ```bash
   docker-compose down
   ```

### Option 2: Manual Setup (For Development)

1. **Set up the database**:
   ```bash
   # Start PostgreSQL database
   docker run -d --name civicshield-db \
     -e POSTGRES_DB=civicshield \
     -e POSTGRES_USER=civicshield_user \
     -e POSTGRES_PASSWORD=civicshield_pass \
     -p 5432:5432 \
     postgres:13

   # Initialize database schema
   docker cp init-scripts/init-database.sql civicshield-db:/tmp/
   docker exec civicshield-db psql -U civicshield_user -d civicshield -f /tmp/init-database.sql
   ```

2. **Start backend services**:
   ```bash
   # Navigate to backend directory
   cd backend

   # Install Python dependencies
   pip install -r requirements.txt

   # Start the backend API
   python main.py
   ```

3. **Start frontend services**:
   ```bash
   # Navigate to frontend directory
   cd frontend

   # Install Node.js dependencies
   npm install

   # Start the frontend
   npm run dev
   ```

4. **Start AI services**:
   ```bash
   # Navigate to AI directory
   cd ai

   # Install Python dependencies
   pip install -r requirements.txt

   # Start the AI service
   python threat_detection.py
   ```

## Environment Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```bash
# Database configuration
DATABASE_URL=postgresql://civicshield_user:civicshield_pass@localhost:5432/civicshield
REDIS_URL=redis://localhost:6379/0
ELASTICSEARCH_URL=http://localhost:9200

# Security settings
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API keys (for external services)
SOCIAL_MEDIA_API_KEY=your_social_media_api_key
MAPBOX_API_KEY=your_mapbox_api_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token

# Cloud provider credentials (if using cloud services)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
```

### Database Initialization

The database is automatically initialized when using Docker Compose. For manual setup, run:

```bash
# Run database initialization script
