# Quick Start Guide

## Getting Started with CivicShield

This guide will help you quickly set up and run the CivicShield platform on your local machine.

## Prerequisites

Install these tools on your system:

- **Docker** (https://docs.docker.com/get-docker/)
- **Git** (https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Quick Setup (5 Minutes)

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/civicshield.git
cd civicshield
```

### 2. Start the Platform

```bash
docker-compose up -d
```

This command will:
- Download all required Docker images
- Start all platform services
- Initialize the database
- Set up networking between services

### 3. Access the Platform

After 2-3 minutes, access these services in your browser:

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

Default login credentials:
- **Username**: admin@civicshield.gov
- **Password**: Admin123!

### 4. Verify Services

Check that all services are running:

```bash
docker-compose ps
```

You should see all services in the "Up" state.

## Testing Data Ingestion

### Send Test Data via API

```bash
# Submit a test threat report
curl -X POST http://localhost:8000/api/v1/data/threats \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "threat_title": "Test Network Intrusion",
    "threat_description": "Simulated unauthorized access attempt",
    "threat_type": "cyber",
    "threat_source": "network_monitoring",
    "severity_score": 8.5,
    "confidence_score": 9.0,
    "geolocation": "192.168.1.100"
  }'
```

### Connect via WebSocket

```bash
# Install wscat for testing WebSocket connections
npm install -g wscat

# Connect to streaming service
wscat -c ws://localhost:8765
```

## Stopping the Platform

To stop all services:

```bash
docker-compose down
```

To stop services and remove data volumes:

```bash
docker-compose down -v
```

## Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs for detailed API documentation
2. **Customize Configuration**: Edit the `.env` file to change settings
3. **Add Real Data Sources**: Integrate with actual IoT sensors, social media APIs, etc.
4. **Deploy to Production**: Follow the deployment guide for production setup

## Troubleshooting

### Common Issues

1. **Services won't start**:
   - Ensure Docker is running
   - Check available system resources (8GB+ RAM recommended)

2. **Database connection errors**:
   - Wait a few more minutes for initialization
   - Check Docker logs: `docker-compose logs database`

3. **Port conflicts**:
   - Edit `docker-compose.yml` to change port mappings
   - Stop other services using the same ports

### View Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
```

## System Requirements

### Minimum
- **CPU**: 4 cores
- **RAM**: 8GB
- **Disk Space**: 20GB free
- **Docker**: Version 20.10+

### Recommended
- **CPU**: 8 cores
- **RAM**: 16GB
- **Disk Space**: 50GB free (SSD recommended)
- **Docker**: Latest version

## What's Included

The platform includes:

- **Frontend**: Next.js dashboard with real-time visualization
- **Backend**: FastAPI with RESTful endpoints
- **Database**: PostgreSQL with TimescaleDB extension
- **Search**: Elasticsearch for text search
- **Caching**: Redis for session management
- **AI/ML**: Threat detection models
- **Streaming**: WebSocket service for real-time data
- **Monitoring**: Prometheus and Grafana

## Security Note

This quick start uses default credentials and settings suitable for testing only. For production use, follow the security guide to:
- Change default passwords
- Configure SSL certificates
- Set up proper authentication
- Review network security settings

## Getting Help

- **Documentation**: https://github.com/your-org/civicshield/docs
- **Issues**: https://github.com/your-org/civicshield/issues
- **Community**: Join our Slack channel

Enjoy using CivicShield!