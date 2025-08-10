# CivicShield Frontend

This directory contains the frontend implementation for the CivicShield platform, built with Next.js and React.

## Table of Contents

1. [Overview](#overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Getting Started](#getting-started)
5. [Development](#development)
6. [Testing](#testing)
7. [Deployment](#deployment)
8. [Contributing](#contributing)

## Overview

The frontend provides the user interface for the CivicShield platform, allowing users to monitor threats, manage incidents, communicate with other agencies, and analyze data through interactive dashboards and visualizations.

## Technology Stack

- **Framework**: Next.js (React)
- **Language**: TypeScript
- **UI Library**: Chakra UI
- **State Management**: Redux Toolkit
- **Mapping**: Mapbox GL JS
- **Charts**: Chart.js
- **Real-time Communication**: Socket.IO
- **Testing**: Jest, React Testing Library
- **Code Quality**: ESLint, Prettier
- **Containerization**: Docker

## Project Structure

```
frontend/
├── pages/               # Next.js pages
├── components/           # React components
├── lib/                 # Utility functions and API clients
├── styles/              # CSS and styling
├── public/              # Static assets
├── tests/               # Test suite
├── store/               # Redux store
├── hooks/               # Custom React hooks
├── context/             # React context providers
├── services/            # API service layer
├── types/               # TypeScript type definitions
├── next.config.js       # Next.js configuration
├── tsconfig.json        # TypeScript configuration
├── package.json         # NPM dependencies and scripts
└── Dockerfile           # Docker configuration
```

## Getting Started

### Prerequisites

- Node.js 16+
- npm or yarn
- Docker and Docker Compose (optional)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-organization/civicshield.git
   cd civicshield/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your configuration
   ```

4. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. Open your browser to http://localhost:3000

### Using Docker

1. Build the Docker image:
   ```bash
   docker build -t civicshield-frontend .
   ```

2. Run the container:
   ```bash
   docker run -p 3000:3000 civicshield-frontend
   ```

## Development

### Code Structure

- **Pages**: Each file in the `pages/` directory corresponds to a route
- **Components**: Reusable UI components in the `components/` directory
- **Services**: API service layer in the `services/` directory
- **Store**: Redux store configuration in the `store/` directory

### Environment Variables

The following environment variables are required for development:

- `NEXT_PUBLIC_API_BASE_URL`: Backend API base URL
- `NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN`: Mapbox access token
- `NEXT_PUBLIC_SOCKET_IO_URL`: Socket.IO server URL

### Styling

The application uses Chakra UI for component styling and a custom CSS file for global styles. Component-specific styles are defined using Chakra's style props.

### Routing

Next.js file-based routing is used. Each file in the `pages/` directory automatically becomes a route.

## Testing

Run the test suite:
```bash
npm test
# or
yarn test
```

Run tests with coverage:
```bash
npm test -- --coverage
# or
yarn test --coverage
```

Run tests in watch mode:
```bash
npm test -- --watch
# or
yarn test --watch
```

## Deployment

The frontend can be deployed using Docker and Kubernetes. See the main project README for detailed deployment instructions.

### Build for Production

```bash
npm run build
# or
yarn build
```

### Start Production Server

```bash
npm start
# or
yarn start
```

### Environment Variables for Production

The following environment variables are required for production:

- `NEXT_PUBLIC_API_BASE_URL`: Backend API base URL
- `NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN`: Mapbox access token

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

### Code Quality

- Use TypeScript for type safety
- Follow the established component structure
- Write unit tests for new functionality
- Run linting before committing:
  ```bash
  npm run lint
  # or
  yarn lint
  ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.