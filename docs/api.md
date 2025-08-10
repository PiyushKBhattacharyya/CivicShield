# CivicShield API Documentation

This document provides an overview of the CivicShield REST API.

## Table of Contents

- [API Overview](#api-overview)
- [Authentication](#authentication)
- [Rate Limiting](#rate-limiting)
- [Error Handling](#error-handling)
- [User Management](#user-management)
- [Threat Management](#threat-management)
- [Incident Management](#incident-management)
- [Sensor Management](#sensor-management)
- [Communication](#communication)
- [Analytics](#analytics)

## API Overview

The CivicShield API is a RESTful API that provides programmatic access to the CivicShield platform. The API follows standard REST conventions and uses JSON for request and response bodies.

### Base URL

```
https://api.civicshield.example.com/v1
```

For local development:
```
http://localhost:8000/api/v1
```

### HTTP Verbs

The API uses standard HTTP verbs:

- `GET` - Retrieve resources
- `POST` - Create resources
- `PUT` - Update resources
- `DELETE` - Delete resources

### Response Format

All API responses are in JSON format with the following structure:

```json
{
  "data": {},
  "meta": {
    "timestamp": "2023-01-01T00:00:00Z",
    "version": "1.0.0"
  }
}
```

For errors, the response follows this structure:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description",
    "details": {}
  }
}
```

## Authentication

The CivicShield API uses JWT (JSON Web Tokens) for authentication.

### Obtaining a Token

To obtain an access token, make a POST request to `/auth/login`:

```http
POST /api/v1/auth/login HTTP/1.1
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "password"
}
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Using a Token

Include the token in the Authorization header of subsequent requests:

```http
GET /api/v1/users/me HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Token Expiration

Tokens expire after 30 minutes. To refresh a token, use the `/auth/refresh` endpoint.

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Anonymous requests**: 100 requests per hour
- **Authenticated requests**: 1000 requests per hour
- **Administrative endpoints**: 100 requests per hour

When a rate limit is exceeded, the API returns a 429 (Too Many Requests) status code.

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of requests:

- `200` - Success
- `201` - Created
- `204` - No Content
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Too Many Requests
- `500` - Internal Server Error

Error responses include a JSON body with details about the error:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "email",
      "reason": "Invalid email format"
    }
  }
}
```

## User Management

### Get Current User

```http
GET /api/v1/users/me HTTP/1.1
```

Response:

```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "username": "johndoe",
  "email": "john.doe@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "agency_id": "123e4567-e89b-12d3-a456-426614174001",
  "role_id": "123e4567-e89b-12d3-a456-426614174002",
  "security_clearance_level": 3,
  "phone_number": "+1234567890",
  "mfa_enabled": true,
  "mfa_method": "totp",
  "created_at": "2023-01-01T00:00:00Z",
  "last_login": "2023-01-02T00:00:00Z",
  "is_active": true
}
```

### Create User

```http
POST /api/v1/users HTTP/1.1
Content-Type: application/json

{
  "username": "janedoe",
  "email": "jane.doe@example.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "password": "securepassword",
  "security_clearance_level": 2,
  "phone_number": "+1234567891"
}
```

### Update User

```http
PUT /api/v1/users/{user_id} HTTP/1.1
Content-Type: application/json

{
  "first_name": "Jane",
  "last_name": "Smith",
  "phone_number": "+1234567892"
}
```

### List Users

```http
GET /api/v1/users HTTP/1.1
```

Query Parameters:
- `skip` (integer, default: 0) - Number of records to skip
- `limit` (integer, default: 100) - Maximum number of records to return

## Threat Management

### Create Threat

```http
POST /api/v1/threats HTTP/1.1
Content-Type: application/json

{
  "threat_title": "Cyber Attack Detected",
  "threat_description": "Unusual network activity detected on government servers",
  "threat_type": "Cyber",
  "threat_source": "Network Sensor",
  "severity_score": 8.5,
  "confidence_score": 9.2,
  "geolocation": "40.7128,-74.0060"
}
```

### Get Threat

```http
GET /api/v1/threats/{threat_id} HTTP/1.1
```

### List Threats

```http
GET /api/v1/threats HTTP/1.1
```

Query Parameters:
- `skip` (integer, default: 0)
- `limit` (integer, default: 100)
- `threat_type` (string) - Filter by threat type
- `severity_min` (number) - Minimum severity score
- `severity_max` (number) - Maximum severity score
- `status` (string) - Filter by status

### Update Threat

```http
PUT /api/v1/threats/{threat_id} HTTP/1.1
Content-Type: application/json

{
  "status": "Resolved",
  "assigned_to": "123e4567