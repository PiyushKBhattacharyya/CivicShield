# CivicShield Development Environment Setup

This document provides detailed instructions for setting up the development environment for the CivicShield platform.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Development Tools Installation](#development-tools-installation)
3. [Environment Configuration](#environment-configuration)
4. [Code Repository Setup](#code-repository-setup)
5. [Database Setup](#database-setup)
6. [Service Dependencies](#service-dependencies)
7. [Testing Environment](#testing-environment)
8. [First Application Run](#first-application-run)
9. [Development Workflow](#development-workflow)
10. [Troubleshooting](#troubleshooting)

## System Requirements

### Hardware Requirements
- **CPU**: Minimum 4 cores, recommended 8 cores
- **Memory**: Minimum 16GB RAM, recommended 32GB RAM
- **Storage**: Minimum 50GB free disk space, SSD recommended
- **Display**: Dual monitors recommended for productivity

### Operating System Support
- **Windows**: Windows 10/11 Pro or Enterprise (64-bit)
- **macOS**: macOS 11.0 (Big Sur) or later
- **Linux**: Ubuntu 20.04 LTS or later, CentOS 8 or later

### Network Requirements
- **Internet Access**: Stable broadband connection
- **Firewall**: Outbound access to package repositories and cloud services
- **VPN**: Access to corporate network for internal services

## Development Tools Installation

### Core Development Tools

#### Git
```bash
# Windows (using Chocolatey)
choco install git

# macOS (using Homebrew)
brew install git

# Ubuntu/Debian
sudo apt update && sudo apt install git

# Verify installation
git --version
```

#### Docker
```bash
# Windows/macOS
# Download Docker Desktop from https://www.docker.com/products/docker-desktop

# Ubuntu/Debian
sudo apt update
sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER

# Verify installation
docker --version
```

#### Python
```bash
# Windows (using Chocolatey)
choco install python

# macOS (using Homebrew)
brew install python

# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip

# Verify installation
python --version
pip --version
```

#### Node.js
```bash
# Windows/macOS/Linux (using Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
nvm install 16
nvm use 16

# Verify installation
node --version
npm --version
```

#### Kubernetes CLI
```bash
# Windows (using Chocolatey)
choco install kubernetes-cli

# macOS (using Homebrew)
brew install kubectl

# Ubuntu/Debian
curl -LO "https://dl.k8s.io/release/$(curl -LS https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/kubectl

# Verify installation
kubectl version --client
```

#### Terraform
```bash
# Windows (using Chocolatey)
choco install terraform

# macOS (using Homebrew)
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

# Ubuntu/Debian
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt update && sudo apt install terraform

# Verify installation
terraform version
```

### Integrated Development Environments (IDEs)

#### Visual Studio Code
1. Download from https://code.visualstudio.com/
2. Install recommended extensions:
   - Python extension pack
   - Docker extension
   - Kubernetes extension
   - GitLens for enhanced Git capabilities
   - Prettier for code formatting
   - ESLint for JavaScript linting
   - Bracket Pair Colorizer
   - Auto Rename Tag

#### PyCharm
1. Download from https://www.jetbrains.com/pycharm/
2. Install plugins:
   - Kubernetes and OpenShift Resource Support
   - Docker integration
   - Database Navigator
   - Markdown Navigator

#### WebStorm
1. Download from https://www.jetbrains.com/webstorm/
2. Install plugins:
   - Kubernetes and OpenShift Resource Support
   - Docker integration
   - Node.js

### Database Tools

#### pgAdmin
```bash
# Windows (using Chocolatey)
choco install pgadmin4

# macOS (using Homebrew)
brew install --cask pgadmin4

# Ubuntu/Debian
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
sudo apt update
sudo apt install pgadmin4
```

#### Redis Desktop Manager
```bash
# Windows/macOS/Linux
# Download from https://rdm.dev/
```

#### Elasticsearch Head
```bash
# Install as Chrome extension or use Kibana
```

### API and Testing Tools

#### Postman
```bash
# Windows/macOS/Linux
# Download from https://www.postman.com/downloads/
```

#### Insomnia
```bash
# Windows/macOS/Linux
# Download from https://insomnia.rest/download
```

#### Jest
```bash
# Install globally
npm install -g jest

# Verify installation
jest --version
```

#### Pytest
```bash
# Install globally
pip install pytest

# Verify installation
pytest --version
```

#### Selenium
```bash
# Install for Python
pip install selenium

# Download WebDriver for your browser
# Chrome: https://chromedriver.chromium.org/
# Firefox: https://github.com/mozilla/geckodriver/releases
```

## Environment Configuration

### Environment Variables
Create a `.env` file in the project root with the following variables:

```bash
# .env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/civicshield
REDIS_URL=redis://localhost:6379/0
ELASTICSEARCH_URL=http://localhost:9200

# API Keys
SOCIAL_MEDIA_API_KEY=your_social_media_api_key
MAPBOX_API_KEY=your_mapbox_api_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token

# Security Settings
SECRET_KEY=your_secret_key_here
JWT_SECRET=your_jwt_secret_key

# Cloud Provider Credentials
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
```

### SSH Configuration
```bash
# Generate SSH keys for Git repository access
ssh-keygen -t ed25519 -C "your_email@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add SSH key
ssh-add ~/.ssh/id_ed25519

# Copy public key to clipboard
cat ~/.ssh/id_ed25519.pub
```

### Certificate Management
```bash
# Install corporate CA certificates
# Windows:
certlm.msc

# macOS:
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain /path/to/certificate.crt

# Linux:
sudo cp certificate.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
```

## Code Repository Setup

### Repository Cloning
```bash
# Clone the main repository
git clone git@github.com:organization/civicshield.git
cd civicshield

# Clone submodules if any
git submodule init
git submodule update

# Set up Git configuration
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### Branch Strategy
```bash
# Set up branch protection rules
git config --global init.defaultBranch main

# Create develop branch
git checkout -b develop

# Set up Git hooks
cd .git/hooks
ln -s ../../hooks/pre-commit pre-commit
ln -s ../../hooks/pre-push pre-push
```

### Git Hooks
Create a `hooks` directory in the project root with the following files:

```bash
# hooks/pre-commit
#!/bin/sh
# Run code formatting and linting
echo "Running pre-commit checks..."
cd backend && python -m black . && python -m flake8 .
cd ../frontend && npm run lint
```

```bash
# hooks/pre-push
#!/bin/sh
# Run tests before pushing
echo "Running pre-push tests..."
cd backend && python -m pytest tests/
cd ../frontend && npm test
```

Make the hooks executable:
```bash
chmod +x hooks/pre-commit
chmod +x hooks/pre-push
```

## Database Setup

### Local Database Services
Using Docker Compose for local development databases:

```yaml
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: civicshield
      POSTGRES_USER: civicshield_user
      POSTGRES_PASSWORD: civicshield_pass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.14.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"
      - "9300:9300"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

volumes:
  postgres_data:
  elasticsearch_data:
```

### Database Initialization
```bash
# Start database services
docker-compose up -d

# Run database migrations
cd backend
alembic upgrade head

# Load initial data
python manage.py loaddata initial_data.json
```

### Database Connection Testing
```bash
# Test PostgreSQL connection
psql -h localhost -p 5432 -U civicshield_user -d civicshield

# Test Redis connection
redis-cli -h localhost -p 6379 ping

# Test Elasticsearch connection
curl -X GET "localhost:9200/_cluster/health?pretty"
```

## Service Dependencies

### Local Development Services
Create a `docker-compose.local.yml` for local development services:

```yaml
version: '3.8'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:latest
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092

  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin
    command: server /data --console-address ":9001"

  keycloak:
    image: quay.io/keycloak/keycloak:15.0.2
    environment:
      KEYCLOAK_USER: admin
      KEYCLOAK_PASSWORD: admin
    ports:
      - "8080:8080"

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

### Service Configuration
```bash
# Start all services
docker-compose -f docker-compose.yml -f docker-compose.local.yml up -d

# Check service status
docker-compose ps

# Stop services
docker-compose down
```

## Testing Environment

### Test Database Setup
```bash
# Create test database
createdb civicshield_test

# Set environment variable for testing
export DATABASE_URL=postgresql://user:password@localhost:5432/civicshield_test

# Run tests with coverage
cd backend
python -m pytest --cov=src tests/
```

### Mock Services
```bash
# Install WireMock for mocking external API dependencies
docker run -it --rm -p 8080:8080 wiremock/wiremock:2.32.0

# Install Testcontainers for integration testing
pip install testcontainers
```

### Test Configuration
Create `pytest.ini` for test configuration:

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --verbose --cov=src --cov-report=html
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_users.py

# Run tests with specific marker
pytest -m unit

# Run tests with coverage
pytest --cov=src --cov-report=html

# Run tests in parallel
pytest -n 4
```

## First Application Run

### Backend Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start development server
uvicorn main:app --reload
```

### Frontend Setup
```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm run dev
```

### Full Stack Development
```bash
# Start all services
docker-compose -f docker-compose.yml -f docker-compose.local.yml up -d

# Start backend
cd backend
uvicorn main:app --reload

# Start frontend (in a new terminal)
cd frontend
npm run dev

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# Backend API Docs: http://localhost:8000/docs
```

## Development Workflow

### Daily Development Process
1. Pull latest changes from develop branch
   ```bash
   git checkout develop
   git pull origin develop
   ```

2. Create feature branch for new work
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Implement changes with regular commits
   ```bash
   git add .
   git commit -m "Add feature implementation"
   ```

4. Run tests locally before pushing
   ```bash
   pytest
   ```

5. Create pull request for code review
   ```bash
   git push origin feature/your-feature-name
   ```

6. Address review feedback

7. Merge to develop after approval

### Code Quality Checks
```bash
# Pre-commit hooks for formatting and linting
cd backend
python -m black .
python -m flake8 .

cd ../frontend
npm run lint
npm run format
```

### Debugging and Troubleshooting
```bash
# Enable debug mode for development
export DEBUG=True

# Use logging with appropriate log levels
# Python:
import logging
logging.basicConfig(level=logging.DEBUG)

# JavaScript:
console.debug("Debug message");
```

### Performance Profiling
```bash
# Python profiling
python -m cProfile -o output.pstats your_script.py
pyprof2calltree -i output.pstats -o output.callgrind

# JavaScript profiling
# Use browser developer tools
```

## Troubleshooting

### Common Issues and Solutions

#### Docker Issues
```bash
# Permission denied errors
sudo usermod -aG docker $USER

# Port already in use
sudo lsof -i :port_number
sudo kill -9 process_id

# Container won't start
docker logs container_name
docker inspect container_name
```

#### Database Connection Issues
```bash
# Check if database is running
docker-compose ps

# Test database connection
psql -h localhost -p 5432 -U civicshield_user -d civicshield

# Check database logs
docker-compose logs database
```

#### Python Dependency Issues
```bash
# Clear pip cache
pip cache purge

# Reinstall dependencies
pip install --no-cache-dir -r requirements.txt

# Upgrade pip
pip install --upgrade pip
```

#### Node.js Issues
```bash
# Clear npm cache
npm cache clean --force

# Reinstall node modules
rm -rf node_modules
npm install

# Rebuild node-sass if needed
npm rebuild node-sass
```

#### Git Issues
```bash
# Fix detached HEAD
git checkout develop

# Undo last commit
git reset --soft HEAD~1

# Fix merge conflicts
git status
# Edit conflicted files
git add .
git commit
```

### Getting Help
- Check documentation in `docs/` directory
- Review existing issues on GitHub
- Contact team lead or senior developers
- Use internal communication channels

## Conclusion

This document provides a comprehensive guide for setting up the development environment for the CivicShield platform. By following these instructions, developers can quickly and consistently set up their development environments and begin contributing to the project.

For any issues not covered in this document, please contact the development team or refer to the project's internal documentation.