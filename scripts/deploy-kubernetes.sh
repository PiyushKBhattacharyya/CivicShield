#!/bin/bash

# CivicShield Kubernetes Deployment Script

# Set variables
NAMESPACE="civicshield"
KUBECONFIG="${KUBECONFIG:-~/.kube/config}"

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed. Please install kubectl and try again."
    exit 1
fi

# Check if kubeconfig exists
if [ ! -f "$KUBECONFIG" ]; then
    echo "Kubeconfig file not found at $KUBECONFIG"
    exit 1
fi

# Create namespace
echo "Creating namespace $NAMESPACE..."
kubectl create namespace $NAMESPACE 2>/dev/null || echo "Namespace $NAMESPACE already exists"

# Apply namespace configuration
echo "Applying namespace configuration..."
kubectl apply -f kubernetes/civicshield-namespace.yaml

# Apply RBAC configuration
echo "Applying RBAC configuration..."
kubectl apply -f kubernetes/civicshield-rbac.yaml

# Apply config and secrets
echo "Applying config and secrets..."
kubectl apply -f kubernetes/civicshield-config.yaml

# Apply Grafana secrets
echo "Applying Grafana secrets..."
kubectl apply -f kubernetes/grafana-secrets.yaml

# Apply persistent volume claims
echo "Applying persistent volume claims..."
kubectl apply -f kubernetes/civicshield-pvc.yaml
kubectl apply -f kubernetes/backups-pvc.yaml

# Apply deployments
echo "Applying deployments..."
kubectl apply -f kubernetes/civicshield-deployment.yaml

# Apply services
echo "Applying services..."
kubectl apply -f kubernetes/civicshield-service.yaml

# Apply ingress
echo "Applying ingress..."
kubectl apply -f kubernetes/civicshield-ingress.yaml

# Apply horizontal pod autoscalers
echo "Applying horizontal pod autoscalers..."
kubectl apply -f kubernetes/civicshield-hpa.yaml

# Apply monitoring configuration
echo "Applying monitoring configuration..."
kubectl apply -f kubernetes/civicshield-monitoring.yaml

# Apply cron jobs
echo "Applying cron jobs..."
kubectl apply -f kubernetes/civicshield-cronjob.yaml

# Wait for deployments to be ready
echo "Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=600s deployment/civicshield-backend -n $NAMESPACE
kubectl wait --for=condition=available --timeout=600s deployment/civicshield-frontend -n $NAMESPACE
kubectl wait --for=condition=available --timeout=600s deployment/civicshield-ai -n $NAMESPACE
kubectl wait --for=condition=available --timeout=600s deployment/civicshield-database -n $NAMESPACE
kubectl wait --for=condition=available --timeout=600s deployment/civicshield-redis -n $NAMESPACE
kubectl wait --for=condition=available --timeout=600s deployment/civicshield-elasticsearch -n $NAMESPACE

# Display service information
echo "Deployment completed successfully!"
echo "Services:"
kubectl get services -n $NAMESPACE

echo "Deployments:"
kubectl get deployments -n $NAMESPACE

echo "Pods:"
kubectl get pods -n $NAMESPACE

echo "Ingress:"
kubectl get ingress -n $NAMESPACE

echo "To access the application, use the ingress hostname or the external load balancer IP."