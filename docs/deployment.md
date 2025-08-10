# CivicShield Deployment Guide

This guide provides instructions for deploying the CivicShield platform in various environments.

## Prerequisites

Before deploying CivicShield, ensure you have the following:

- Docker and Docker Compose installed
- Access to a cloud provider (AWS, Azure, or GCP) or on-premises infrastructure
- Domain name and SSL certificate (for production deployment)
- Required API keys and credentials for external services

## Deployment Options

### 1. Local Development Deployment

For local development and testing, use the provided docker-compose.yml file:

```bash
# Clone the repository
git clone https://github.com/your-org/civicshield.git
cd civicshield

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# Database: localhost:5432
# Redis: localhost:6379
# Elasticsearch: http://localhost:9200
```

### 2. Staging Environment Deployment

For staging environments, you can use the same docker-compose setup but with different configurations:

```bash
# Create a docker-compose.staging.yml file with staging-specific settings
# Then deploy with:
docker-compose -f docker-compose.staging.yml up -d
```

### 3. Production Deployment

For production deployment, we recommend using Kubernetes with the provided Helm charts:

```bash
# Add the CivicShield Helm repository
helm repo add civicshield https://helm.civicshield.example.com

# Install the CivicShield chart
helm install civicshield civicshield/civicshield \
  --namespace civicshield \
  --create-namespace \
  --set ingress.enabled=true \
  --set ingress.hosts[0].host=civicshield.example.com \
  --set ingress.tls[0].hosts[0]=civicshield.example.com \
  --set ingress.tls[0].secretName=civicshield-tls
```

## Environment Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@database:5432/civicshield
REDIS_URL=redis://redis:6379/0
ELASTICSEARCH_URL=http://elasticsearch:9200

# Security Configuration
SECRET_KEY=your-production-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys
SOCIAL_MEDIA_API_KEY=your_social_media_api_key
MAPBOX_API_KEY=your_mapbox_api_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token

# Cloud Provider Credentials
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
```

### Kubernetes Configuration

For Kubernetes deployments, create the following secrets:

```bash
# Create a secret for environment variables
kubectl create secret generic civicshield-env \
  --from-literal=DATABASE_URL=postgresql://user:password@database:5432/civicshield \
  --from-literal=REDIS_URL=redis://redis:6379/0 \
  --from-literal=ELASTICSEARCH_URL=http://elasticsearch:9200 \
  --from-literal=SECRET_KEY=your-production-secret-key \
  --namespace=civicshield

# Create a secret for API keys
kubectl create secret generic civicshield-api-keys \
  --from-literal=SOCIAL_MEDIA_API_KEY=your_social_media_api_key \
  --from-literal=MAPBOX_API_KEY=your_mapbox_api_key \
  --from-literal=TWILIO_ACCOUNT_SID=your_twilio_sid \
  --from-literal=TWILIO_AUTH_TOKEN=your_twilio_token \
  --namespace=civicshield
```

## Database Setup

### Initial Database Migration

After deploying the application, run the initial database migration:

```bash
# For Docker Compose deployments
docker-compose exec backend alembic upgrade head

# For Kubernetes deployments
kubectl exec -it deployment/civicshield-backend -n civicshield -- alembic upgrade head
```

### Database Backup and Restore

Regular database backups are essential for production deployments:

```bash
# Backup
docker-compose exec database pg_dump -U civicshield_user civicshield > backup.sql

# Restore
docker-compose exec -T database psql -U civicshield_user civicshield < backup.sql
```

## Monitoring and Logging

### Prometheus and Grafana

The deployment includes Prometheus for metrics collection and Grafana for visualization:

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (default credentials: admin/admin)

### ELK Stack

For log aggregation and analysis, the deployment includes the ELK stack:

- Elasticsearch: http://localhost:9200
- Logstash: http://localhost:9600
- Kibana: http://localhost:5601

## Scaling

### Horizontal Scaling

To scale the application horizontally, adjust the replica counts in your deployment configuration:

```bash
# For Docker Compose
docker-compose up -d --scale backend=3 --scale frontend=2

# For Kubernetes
kubectl scale deployment civicshield-backend --replicas=3 -n civicshield
kubectl scale deployment civicshield-frontend --replicas=2 -n civicshield
```

### Vertical Scaling

To scale vertically, adjust the resource limits in your deployment configuration:

```yaml
# In your Kubernetes deployment YAML
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

## Security Considerations

### Network Security

- Use network policies to restrict traffic between services
- Implement a service mesh for advanced traffic management
- Use ingress controllers with SSL termination

### Data Security

- Enable encryption at rest for databases
- Use TLS for all service-to-service communication
- Regularly rotate API keys and secrets

### Access Control

- Implement role-based access control (RBAC)
- Use OAuth 2.0 for user authentication
- Enable multi-factor authentication (MFA)

## Backup and Disaster Recovery

### Regular Backups

- Schedule regular database backups
- Backup configuration files and secrets
- Store backups in multiple geographic locations

### Disaster Recovery Plan

- Define recovery time objectives (RTO) and recovery point objectives (RPO)
- Test disaster recovery procedures regularly
- Maintain up-to-date documentation of the recovery process

## Troubleshooting

### Common Issues

1. **Services not starting**: Check logs with `docker-compose logs` or `kubectl logs`
2. **Database connection issues**: Verify database credentials and network connectivity
3. **API errors**: Check backend logs for error messages
4. **Performance issues**: Monitor resource usage and scale accordingly

### Getting Help

For additional support, please contact the CivicShield team at support@civicshield.example.com.