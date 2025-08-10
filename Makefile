# Makefile for CivicShield Platform

# Variables
PROJECT_NAME := civicshield
DOCKER_COMPOSE := docker-compose.yml
KUBERNETES_DIR := kubernetes
SCRIPTS_DIR := scripts

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m # No Color

# Help target
.PHONY: help
help:
	@echo "CivicShield Platform Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  help             Show this help message"
	@echo "  setup            Setup development environment"
	@echo "  start            Start development environment"
	@echo "  stop             Stop development environment"
	@echo "  restart          Restart development environment"
	@echo "  clean            Clean development environment"
	@echo "  test             Run tests"
	@echo "  test-backend     Run backend tests"
	@echo "  test-frontend    Run frontend tests"
	@echo "  lint             Run code linting"
	@echo "  lint-backend     Run backend code linting"
	@echo "  lint-frontend    Run frontend code linting"
	@echo "  build            Build Docker images"
	@echo "  deploy-k8s       Deploy to Kubernetes"
	@echo "  db-migrate       Run database migrations"
	@echo "  db-reset         Reset database"
	@echo "  docs             Generate documentation"
	@echo "  security-scan    Run security scan"

# Setup development environment
.PHONY: setup
setup:
	@echo "$(GREEN)Setting up development environment...$(NC)"
	# Install pre-commit hooks
	pip install pre-commit
	pre-commit install
	# Install backend dependencies
	cd backend && pip install -r requirements.txt -r requirements-dev.txt
	# Install frontend dependencies
	cd frontend && npm install
	# Create .env file if it doesn't exist
	if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "$(YELLOW)Created .env file. Please update with your configuration.$(NC)"; \
	fi
	@echo "$(GREEN)Development environment setup complete!$(NC)"

# Start development environment
.PHONY: start
start:
	@echo "$(GREEN)Starting development environment...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)Development environment started!$(NC)"
	@echo "Access the application at http://localhost:3000"

# Stop development environment
.PHONY: stop
stop:
	@echo "$(YELLOW)Stopping development environment...$(NC)"
	docker-compose down
	@echo "$(GREEN)Development environment stopped!$(NC)"

# Restart development environment
.PHONY: restart
restart: stop start

# Clean development environment
.PHONY: clean
clean:
	@echo "$(YELLOW)Cleaning development environment...$(NC)"
	docker-compose down -v --remove-orphans
	@echo "$(GREEN)Development environment cleaned!$(NC)"

# Run tests
.PHONY: test
test: test-backend test-frontend

# Run backend tests
.PHONY: test-backend
test-backend:
	@echo "$(GREEN)Running backend tests...$(NC)"
	cd backend && python -m pytest tests/ -v

# Run frontend tests
.PHONY: test-frontend
test-frontend:
	@echo "$(GREEN)Running frontend tests...$(NC)"
	cd frontend && npm test

# Run code linting
.PHONY: lint
lint: lint-backend lint-frontend

# Run backend code linting
.PHONY: lint-backend
lint-backend:
	@echo "$(GREEN)Running backend code linting...$(NC)"
	cd backend && python -m black . && python -m flake8 .

# Run frontend code linting
.PHONY: lint-frontend
lint-frontend:
	@echo "$(GREEN)Running frontend code linting...$(NC)"
	cd frontend && npm run lint

# Build Docker images
.PHONY: build
build:
	@echo "$(GREEN)Building Docker images...$(NC)"
	docker-compose build
	@echo "$(GREEN)Docker images built!$(NC)"

# Deploy to Kubernetes
.PHONY: deploy-k8s
deploy-k8s:
	@echo "$(GREEN)Deploying to Kubernetes...$(NC)"
	bash $(SCRIPTS_DIR)/deploy-kubernetes.sh
	@echo "$(GREEN)Deployment to Kubernetes complete!$(NC)"

# Run database migrations
.PHONY: db-migrate
db-migrate:
	@echo "$(GREEN)Running database migrations...$(NC)"
	cd backend && alembic upgrade head

# Reset database
.PHONY: db-reset
db-reset:
	@echo "$(YELLOW)Resetting database...$(NC)"
	docker-compose exec database psql -U civicshield_user -d civicshield -f /init-scripts/init-database.sql
	@echo "$(GREEN)Database reset complete!$(NC)"

# Generate documentation
.PHONY: docs
docs:
	@echo "$(GREEN)Generating documentation...$(NC)"
	cd docs && make html
	@echo "$(GREEN)Documentation generated!$(NC)"

# Run security scan
.PHONY: security-scan
security-scan:
	@echo "$(GREEN)Running security scan...$(NC)"
	cd backend && python -m bandit -r . -c bandit.yaml
	@echo "$(GREEN)Security scan complete!$(NC)"