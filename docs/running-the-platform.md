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
psql -U civicshield_user -d civicshield -f init-scripts/init-database.sql
```

## Running Tests

### Backend Tests

```bash
# Navigate to backend directory
cd backend

# Run tests
python -m pytest tests/ -v
```

### Frontend Tests

```bash
# Navigate to frontend directory
cd frontend

# Run tests
npm test
```

### AI/ML Tests

```bash
# Navigate to AI directory
cd ai

# Run tests
python -m pytest tests/ -v
```

## Production Deployment

### Docker Compose Deployment

For production deployment using Docker Compose:

1. **Create production environment file**:
   ```bash
   cp .env.example .env.prod
   # Edit .env.prod with production values
   ```

2. **Start production services**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Kubernetes Deployment

For production deployment using Kubernetes:

1. **Set up Kubernetes cluster** (if not already done)

2. **Configure kubectl** to point to your cluster

3. **Apply Kubernetes configurations**:
   ```bash
   kubectl apply -f kubernetes/
   ```

4. **Check deployment status**:
   ```bash
   kubectl get pods -n civicshield
   ```

5. **Access services**:
   ```bash
   # Get service URLs
   kubectl get services -n civicshield
   ```

### Terraform Deployment

For infrastructure provisioning using Terraform:

1. **Navigate to Terraform directory**:
   ```bash
   cd terraform
   ```

2. **Initialize Terraform**:
   ```bash
   terraform init
   ```

3. **Review the plan**:
   ```bash
   terraform plan
   ```

4. **Apply the infrastructure**:
   ```bash
   terraform apply
   ```

## Monitoring and Logging

### Accessing Monitoring Dashboards

1. **Prometheus** (metrics collection):
   ```bash
   # If using Docker Compose
   http://localhost:9090

   # If using Kubernetes
   kubectl port-forward svc/prometheus 9090:9090 -n monitoring
   ```

2. **Grafana** (dashboard visualization):
   ```bash
   # If using Docker Compose
   http://localhost:3001

   # If using Kubernetes
   kubectl port-forward svc/grafana 3001:3001 -n monitoring
   ```

3. **Kibana** (log analysis):
   ```bash
   # If using Docker Compose
   http://localhost:5601

   # If using Kubernetes
   kubectl port-forward svc/kibana 5601:5601 -n monitoring
   ```

## Troubleshooting

### Common Issues

1. **Database connection errors**:
   - Check if the database container is running
   - Verify database credentials in environment variables
   - Ensure the database has been initialized

2. **Port conflicts**:
   - Check if ports are already in use
   - Modify port mappings in docker-compose.yml

3. **Service dependencies**:
   - Ensure all required services are started
   - Check service logs for error messages

### Checking Service Status

```bash
# Docker Compose
docker-compose ps

# Kubernetes
kubectl get pods -n civicshield
```

### Viewing Logs

```bash
# Docker Compose
docker-compose logs [service-name]

# Kubernetes
kubectl logs [pod-name] -n civicshield
```

## Scaling the Platform

### Horizontal Scaling with Docker Compose

```bash
# Scale backend services
docker-compose up -d --scale backend=3
```

### Horizontal Scaling with Kubernetes

```bash
# Scale backend deployment
kubectl scale deployment civicshield-backend --replicas=3 -n civicshield
```

## Backup and Recovery

### Database Backup

```bash
# Docker Compose backup
docker exec civicshield-database pg_dump -U civicshield_user civicshield > backup.sql

# Kubernetes backup
kubectl exec civicshield-database-0 -n civicshield -- pg_dump -U civicshield_user civicshield > backup.sql
```

### Database Restore

```bash
# Docker Compose restore
docker exec -i civicshield-database psql -U civicshield_user civicshield < backup.sql

# Kubernetes restore
kubectl exec -i civicshield-database-0 -n civicshield -- psql -U civicshield_user civicshield < backup.sql
```

## Updating the Platform

### Docker Compose Update

```bash
# Pull latest images
docker-compose pull

# Restart services
docker-compose up -d
```

### Kubernetes Update

```bash
# Update deployment
kubectl set image deployment/civicshield-backend backend=civicshield/backend:latest -n civicshield
```

## Conclusion

The CivicShield platform can be run in multiple environments with varying levels of complexity. For development and testing, Docker Compose provides the simplest setup. For production deployments, Kubernetes offers better scalability and management capabilities.

Always ensure you have proper backups and follow security best practices when running the platform in production environments.