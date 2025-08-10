# CivicShield Development Setup

This document provides instructions for setting up a development environment for the CivicShield platform, covering system requirements, installation procedures, and configuration steps.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Development Environment Setup](#development-environment-setup)
3. [Backend Development Setup](#backend-development-setup)
4. [Frontend Development Setup](#frontend-development-setup)
5. [AI/ML Development Setup](#aiml-development-setup)
6. [Database Setup](#database-setup)
7. [Development Workflow](#development-workflow)
8. [Testing](#testing)
9. [Debugging](#debugging)
10. [Code Quality](#code-quality)
11. [Documentation](#documentation)
12. [Contributing](#contributing)

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
- **VPN**: Access to corporate network for internal services (if required)

## Development Environment Setup

### Core Development Tools

1. **Git**: Version control system (latest stable version)
   - Download from: https://git-scm.com/
   - Verify installation: `git --version`

2. **Docker**: Containerization platform
   - For Windows/macOS: Docker Desktop
   - For Linux: Docker Engine and Docker Compose
   - Verify installation: `docker --version` and `docker-compose --version`

3. **Python**: Python 3.9+ for backend services
   - Download from: https://www.python.org/
   - Verify installation: `python --version`

4. **Node.js**: Node.js 16+ for frontend development
   - Download from: https://nodejs.org/
   - Verify installation: `node --version` and `npm --version`

5. **Kubernetes CLI**: kubectl for Kubernetes cluster interaction
   - Download from: https://kubernetes.io/docs/tasks/tools/
   - Verify installation: `kubectl version --client`

6. **Terraform**: Infrastructure as Code tool
   - Download from: https://www.terraform.io/
   - Verify installation: `terraform version`

7. **Helm**: Kubernetes package manager
   - Download from: https://helm.sh/
   - Verify installation: `helm version`

### Integrated Development Environments (IDEs)

#### Visual Studio Code (Recommended)
- Extensions:
  - Python extension pack
  - Docker extension
  - Kubernetes extension
  - GitLens for enhanced Git capabilities
  - Prettier for code formatting
  - ESLint for JavaScript linting
  - Bracket Pair Colorizer for better code readability

#### PyCharm
- Alternative IDE for Python development
- Professional edition recommended for Django support

#### WebStorm
- Alternative IDE for frontend development
- Excellent JavaScript/TypeScript support

### Database Tools

1. **pgAdmin**: PostgreSQL administration tool
   - Download from: https://www.pgadmin.org/
   - For Docker: `docker run -d -p 5050:80 -e "PGADMIN_DEFAULT_EMAIL=user@domain.com" -e "PGADMIN_DEFAULT_PASSWORD=SuperSecret" dpage/pgadmin4`

2. **Redis Desktop Manager**: Redis database management
   - Download from: https://redisdesktop.com/
   - For Docker: `docker run -d -p 6379:6379 redis`

3. **Elasticsearch Head**: Elasticsearch cluster management
   - For Docker: `docker run -d -p 9100:9100 mobz/elasticsearch-head:5`

4. **Supabase CLI**: Local development with Supabase
   - Install: `npm install -g supabase`
   - Verify: `supabase --version`

### API and Testing Tools

1. **Postman**: API testing and development
   - Download from: https://www.postman.com/
   - For Docker: `docker run -d -p 3000:3000 -p 3001:3001 --name postman postman/postman

2. **Insomnia**: Alternative API client
   - Download from: https://insomnia.rest/

3. **Jest**: JavaScript testing framework
   - Install: `npm install -g jest`
   - Verify: `jest --version`

4. **Pytest**: Python testing framework
   - Install: `pip install pytest`
   - Verify: `pytest --version`

5. **Selenium**: Browser automation for end-to-end testing
   - Install: `pip install selenium`
   - Download browser drivers: https://www.selenium.dev/downloads/

## Backend Development Setup

### Python Environment Setup

1. **Create Virtual Environment**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Environment Variables**:
   Create a `.env` file in the backend directory:
   ```bash
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=postgresql://user:password@localhost:5432/civicshield
   REDIS_URL=redis://localhost:6379/0
   ELASTICSEARCH_URL=http://localhost:9200
   DEBUG=True
   ```

### Database Migration

1. **Run Migrations**:
   ```bash
   cd backend
   alembic upgrade head
   ```

2. **Create New Migration**:
   ```bash
   alembic revision -m "Description of changes"
   ```

### Running the Backend

1. **Development Server**:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **Docker Development**:
   ```bash
   docker-compose up backend
   ```

## Frontend Development Setup

### Node.js Environment Setup

1. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Environment Variables**:
   Create a `.env.local` file in the frontend directory:
   ```bash
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
   NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN=your_mapbox_token
   ```

### Running the Frontend

1. **Development Server**:
   ```bash
   cd frontend
   npm run dev
   ```

2. **Docker Development**:
   ```bash
   docker-compose up frontend
   ```

### Frontend Testing

1. **Run Tests**:
   ```bash
   cd frontend
   npm test
   ```

2. **Run Tests with Coverage**:
   ```bash
   npm test -- --coverage
   ```

## AI/ML Development Setup

### Python Environment Setup

1. **Create Virtual Environment**:
   ```bash
   cd ai
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download Required NLTK Data**:
   ```bash
   python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt')"
   ```

### Running the AI Service

1. **Development Server**:
   ```bash
   cd ai
   python threat_detection.py
   ```

2. **Docker Development**:
   ```bash
   docker-compose up ai
   ```

## Database Setup

### PostgreSQL Setup

1. **Docker Setup**:
   ```bash
   docker-compose up database
   ```

2. **Manual Setup**:
   ```bash
   # Install PostgreSQL
   # Create database and user
   # Run initialization script
   ```

### Redis Setup

1. **Docker Setup**:
   ```bash
   docker-compose up redis
   ```

2. **Manual Setup**:
   ```bash
   # Install Redis
   # Start Redis server
   ```

### Elasticsearch Setup

1. **Docker Setup**:
   ```bash
   docker-compose up elasticsearch
   ```

2. **Manual Setup**:
   ```bash
   # Install Elasticsearch
   # Start Elasticsearch service
   ```

## Development Workflow

### Git Workflow

1. **Branch Strategy**:
   - `main`: Production-ready code
   - `develop`: Integration branch for ongoing development
   - `feature/*`: Feature branches for new functionality
   - `hotfix/*`: Emergency fixes for production issues
   - `release/*`: Release preparation branches

2. **Commit Messages**:
   - Use conventional commit format
   - Example: `feat(auth): add multi-factor authentication`

3. **Pull Requests**:
   - Create PR against `develop` branch
   - Request review from team members
   - Address feedback before merging

### Code Review Process

1. **Pre-review Checklist**:
   - Code follows style guidelines
   - Tests are included and passing
   - Documentation is updated
   - Security considerations are addressed

2. **Review Process**:
   - Reviewer assigned by team lead
   - Review within 24 hours
   - Address comments and resubmit

### Continuous Integration

1. **GitHub Actions**:
   - Automated testing on push and pull request
   - Security scanning
   - Code quality checks
   - Deployment to staging

2. **Local Testing**:
   - Run tests before pushing
   - Use pre-commit hooks
   - Verify functionality locally

## Testing

### Backend Testing

1. **Unit Tests**:
   ```bash
   cd backend
   python -m pytest tests/unit
   ```

2. **Integration Tests**:
   ```bash
   cd backend
   python -m pytest tests/integration
   ```

3. **API Tests**:
   ```bash
   cd backend
   python -m pytest tests/api
   ```

### Frontend Testing

1. **Unit Tests**:
   ```bash
   cd frontend
   npm run test:unit
   ```

2. **Integration Tests**:
   ```bash
   cd frontend
   npm run test:integration
   ```

3. **End-to-End Tests**:
   ```bash
   cd frontend
   npm run test:e2e
   ```

### AI/ML Testing

1. **Model Tests**:
   ```bash
   cd ai
   python -m pytest tests/models
   ```

2. **Data Tests**:
   ```bash
   cd ai
   python -m pytest tests/data
   ```

## Debugging

### Backend Debugging

1. **VS Code Debugging**:
   - Use Python debugger
   - Set breakpoints in code
   - Inspect variables and execution flow

2. **Logging**:
   ```python
   import logging
   logger = logging.getLogger(__name__)
   logger.debug("Debug message")
   logger.info("Info message")
   logger.warning("Warning message")
   logger.error("Error message")
   ```

3. **Database Debugging**:
   - Use pgAdmin to inspect database
   - Run SQL queries directly
   - Check query performance

### Frontend Debugging

1. **Browser Developer Tools**:
   - Use Chrome DevTools or Firefox Developer Tools
   - Inspect elements and network requests
   - Debug JavaScript code

2. **React Developer Tools**:
   - Install React Developer Tools extension
   - Inspect React component hierarchy
   - Monitor component state and props

3. **Redux DevTools**:
   - Install Redux DevTools extension
   - Monitor Redux state changes
   - Time-travel debugging

### AI/ML Debugging

1. **Model Debugging**:
   - Use print statements for debugging
   - Log intermediate results
   - Visualize model outputs

2. **Data Debugging**:
   - Inspect data at different processing stages
   - Check for data quality issues
   - Validate data transformations

## Code Quality

### Backend Code Quality

1. **Black**: Code formatting
   ```bash
   cd backend
   python -m black .
   ```

2. **Flake8**: Code linting
   ```bash
   cd backend
   python -m flake8 .
   ```

3. **MyPy**: Type checking
   ```bash
   cd backend
   python -m mypy .
   ```

### Frontend Code Quality

1. **ESLint**: JavaScript/TypeScript linting
   ```bash
   cd frontend
   npm run lint
   ```

2. **Prettier**: Code formatting
   ```bash
   cd frontend
   npm run format
   ```

### AI/ML Code Quality

1. **Black**: Code formatting
   ```bash
   cd ai
   python -m black .
   ```

2. **Flake8**: Code linting
   ```bash
   cd ai
   python -m flake8 .
   ```

## Documentation

### Code Documentation

1. **Backend Documentation**:
   - Use docstrings for functions and classes
   - Follow Google Python Style Guide
   - Generate API documentation with FastAPI

2. **Frontend Documentation**:
   - Use JSDoc for JavaScript functions
   - Document React components with PropTypes
   - Generate documentation with Storybook

3. **AI/ML Documentation**:
   - Document model architectures
   - Explain data processing steps
   - Provide usage examples

### Project Documentation

1. **README Files**:
   - Project overview and setup instructions
   - Contribution guidelines
   - License information

2. **Architecture Documentation**:
   - System architecture diagrams
   - Component descriptions
   - Data flow explanations

3. **API Documentation**:
   - Endpoint descriptions
   - Request/response examples
   - Authentication requirements

## Contributing

### Contribution Process

1. **Fork Repository**:
   - Fork the repository to your GitHub account
   - Clone your fork locally

2. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**:
   - Implement your feature or fix
   - Write tests for your changes
   - Update documentation as needed

4. **Commit Changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature"
   ```

5. **Push to Fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**:
   - Navigate to the original repository
   - Create pull request from your fork
   - Describe your changes in detail

### Code Review Guidelines

1. **Review Process**:
   - All code must be reviewed before merging
   - Request review from team members
   - Address feedback promptly

2. **Review Criteria**:
   - Code correctness and efficiency
   - Security considerations
   - Code style and maintainability
   - Test coverage and quality

### Release Process

1. **Versioning**:
   - Follow Semantic Versioning (SemVer)
   - Update version numbers in relevant files

2. **Release Branch**:
   ```bash
   git checkout -b release/v1.0.0
   ```

3. **Release Preparation**:
   - Update changelog
   - Finalize documentation
   - Run comprehensive tests

4. **Release Creation**:
   - Create release tag
   - Publish release on GitHub
   - Deploy to production

## Conclusion

This development setup guide provides a comprehensive overview of setting up a development environment for the CivicShield platform. By following these instructions, developers can quickly get started contributing to the project while maintaining code quality and security standards.