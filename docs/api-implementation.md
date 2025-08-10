# CivicShield API Implementation

This document outlines the API implementation for the CivicShield platform, covering RESTful endpoints, authentication, and integration with external services.

## Table of Contents

1. [API Overview](#api-overview)
2. [Authentication](#authentication)
3. [User Management](#user-management)
4. [Threat Management](#threat-management)
5. [Incident Management](#incident-management)
6. [Communication](#communication)
7. [Analytics](#analytics)
8. [External Integrations](#external-integrations)
9. [Error Handling](#error-handling)
10. [Rate Limiting](#rate-limiting)
11. [API Versioning](#api-versioning)
12. [Security](#security)

## API Overview

### Base URL
```
https://api.civicshield.example.com/v1
```

### Supported Formats
- **Request/Response Format**: JSON
- **Character Encoding**: UTF-8
- **Date/Time Format**: ISO 8601

### HTTP Methods
- **GET**: Retrieve resources
- **POST**: Create resources
- **PUT**: Update resources
- **DELETE**: Delete resources
- **PATCH**: Partially update resources

### Response Codes
- **200 OK**: Successful GET and PATCH requests
- **201 Created**: Successful POST requests
- **204 No Content**: Successful DELETE requests
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Invalid or missing authentication token
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **409 Conflict**: Resource conflict
- **422 Unprocessable Entity**: Semantic errors in request data
- **429 Too Many Requests**: Rate limiting
- **500 Internal Server Error**: Server errors

## Authentication

### JSON Web Tokens (JWT)
The CivicShield API uses JWT for authentication. Tokens are obtained through the login endpoint and must be included in the Authorization header for all requests.

#### Login
```
POST /auth/login
```

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

#### Token Refresh
```
POST /auth/refresh
```

**Request Body:**
```json
{
  "refresh_token": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

#### Logout
```
POST /auth/logout
```

**Request Body:**
```json
{
  "refresh_token": "string"
}
```

**Response:**
```json
{
  "message": "Successfully logged out"
}
```

## User Management

### Get Current User
```
GET /users/me
```

**Response:**
```json
{
  "user_id": "uuid",
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "agency_id": "uuid",
  "role_id": "uuid",
  "security_clearance_level": "integer",
  "phone_number": "string",
  "mfa_enabled": "boolean",
  "mfa_method": "string",
  "created_at": "datetime",
  "last_login": "datetime",
  "is_active": "boolean"
}
```

### Update Current User
```
PUT /users/me
```

**Request Body:**
```json
{
  "first_name": "string",
  "last_name": "string",
  "phone_number": "string"
}
```

**Response:**
```json
{
  "user_id": "uuid",
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "agency_id": "uuid",
  "role_id": "uuid",
  "security_clearance_level": "integer",
  "phone_number": "string",
  "mfa_enabled": "boolean",
  "mfa_method": "string",
  "created_at": "datetime",
  "last_login": "datetime",
  "is_active": "boolean"
}
```

### Change Password
```
POST /users/me/change-password
```

**Request Body:**
```json
{
  "current_password": "string",
  "new_password": "string"
}
```

**Response:**
```json
{
  "message": "Password changed successfully"
}
```

### Get Users
```
GET /users
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Number of results per page (default: 10)
- `search`: Search term for username or email
- `agency_id`: Filter by agency
- `role_id`: Filter by role
- `is_active`: Filter by active status

**Response:**
```json
{
  "users": [
    {
      "user_id": "uuid",
      "username": "string",
      "email": "string",
      "first_name": "string",
      "last_name": "string",
      "agency_id": "uuid",
      "role_id": "uuid",
      "security_clearance_level": "integer",
      "phone_number": "string",
      "mfa_enabled": "boolean",
      "mfa_method": "string",
      "created_at": "datetime",
      "last_login": "datetime",
      "is_active": "boolean"
    }
  ],
  "pagination": {
    "page": "integer",
    "limit": "integer",
    "total": "integer",
    "pages": "integer"
  }
}
```

### Get User by ID
```
GET /users/{user_id}
```

**Response:**
```json
{
  "user_id": "uuid",
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "agency_id": "uuid",
  "role_id": "uuid",
  "security_clearance_level": "integer",
  "phone_number": "string",
  "mfa_enabled": "boolean",
  "mfa_method": "string",
  "created_at": "datetime",
  "last_login": "datetime",
  "is_active": "boolean"
}
```

### Create User
```
POST /users
```

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "agency_id": "uuid",
  "role_id": "uuid",
  "security_clearance_level": "integer",
  "phone_number": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "user_id": "uuid",
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "agency_id": "uuid",
  "role_id": "uuid",
  "security_clearance_level": "integer",
  "phone_number": "string",
  "mfa_enabled": "boolean",
  "mfa_method": "string",
  "created_at": "datetime",
  "is_active": "boolean"
}
```

### Update User
```
PUT /users/{user_id}
```

**Request Body:**
```json
{
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "agency_id": "uuid",
  "role_id": "uuid",
  "security_clearance_level": "integer",
  "phone_number": "string",
  "is_active": "boolean"
}
```

**Response:**
```json
{
  "user_id": "uuid",
  "username": "string",
  "email": "string",
  "first_name": "string",
  "last_name": "string",
  "agency_id": "uuid",
  "role_id": "uuid",
  "security_clearance_level": "integer",
  "phone_number": "string",
  "mfa_enabled": "boolean",
  "mfa_method": "string",
  "created_at": "datetime",
  "last_login": "datetime",
  "is_active": "boolean"
}
```

### Delete User
```
DELETE /users/{user_id}
```

**Response:**
```json
{
  "message": "User deleted successfully"
}
```

## Threat Management

### Get Threats
```
GET /threats
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Number of results per page (default: 10)
- `threat_type`: Filter by threat type
- `status`: Filter by status (ACTIVE, RESOLVED, DISMISSED)
- `severity_score_min`: Minimum severity score
- `severity_score_max`: Maximum severity score
- `detected_after`: Filter by detection date (ISO 8601)
- `detected_before`: Filter by detection date (ISO 8601)

**Response:**
```json
{
  "threats": [
    {
      "threat_id": "uuid",
      "threat_type": "string",
      "threat_source": "string",
      "threat_title": "string",
      "threat_description": "string",
      "severity_score": "number",
      "confidence_score": "number",
      "geolocation": "string",
      "detected_at": "datetime",
      "created_at": "datetime",
      "status": "string",
      "assigned_to": "uuid",
      "agency_id": "uuid"
    }
  ],
  "pagination": {
    "page": "integer",
    "limit": "integer",
    "total": "integer",
    "pages": "integer"
  }
}
```

### Get Threat by ID
```
GET /threats/{threat_id}
```

**Response:**
```json
{
  "threat_id": "uuid",
  "threat_type": "string",
  "threat_source": "string",
  "threat_title": "string",
  "threat_description": "string",
  "severity_score": "number",
  "confidence_score": "number",
  "geolocation": "string",
  "detected_at": "datetime",
  "created_at": "datetime",
  "status": "string",
  "assigned_to": "uuid",
  "agency_id": "uuid"
}
```

### Create Threat
```
POST /threats
```

**Request Body:**
```json
{
  "threat_type": "string",
  "threat_source": "string",
  "threat_title": "string",
  "threat_description": "string",
  "severity_score": "number",
  "confidence_score": "number",
  "geolocation": "string",
  "status": "string",
  "assigned_to": "uuid",
  "agency_id": "uuid"
}
```

**Response:**
```json
{
  "threat_id": "uuid",
  "threat_type": "string",
  "threat_source": "string",
  "threat_title": "string",
  "threat_description": "string",
  "severity_score": "number",
  "confidence_score": "number",
  "geolocation": "string",
  "detected_at": "datetime",
  "created_at": "datetime",
  "status": "string",
  "assigned_to": "uuid",
  "agency_id": "uuid"
}
```

### Update Threat
```
PUT /threats/{threat_id}
```

**Request Body:**
```json
{
  "threat_type": "string",
  "threat_source": "string",
  "threat_title": "string",
  "threat_description": "string",
  "severity_score": "number",
  "confidence_score": "number",
  "geolocation": "string",
  "status": "string",
  "assigned_to": "uuid",
  "agency_id": "uuid"
}
```

**Response:**
```json
{
  "threat_id": "uuid",
  "threat_type": "string",
  "threat_source": "string",
  "threat_title": "string",
  "threat_description": "string",
  "severity_score": "number",
  "confidence_score": "number",
  "geolocation": "string",
  "detected_at": "datetime",
  "created_at": "datetime",
  "status": "string",
  "assigned_to": "uuid",
  "agency_id": "uuid"
}
```

### Delete Threat
```
DELETE /threats/{threat_id}
```

**Response:**
```json
{
  "message": "Threat deleted successfully"
}
```

### Analyze Threat
```
POST /threats/{threat_id}/analyze
```

**Request Body:**
```json
{
  "analysis_type": "string"
}
```

**Response:**
```json
{
  "analysis_id": "uuid",
  "threat_id": "uuid",
  "analysis_type": "string",
  "results": "object",
  "created_at": "datetime"
}
```

## Incident Management

### Get Incidents
```
GET /incidents
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Number of results per page (default: 10)
- `incident_type`: Filter by incident type
- `status`: Filter by status (OPEN, IN_PROGRESS, RESOLVED, CLOSED)
- `severity_level`: Filter by severity level
- `priority_level`: Filter by priority level
- `created_after`: Filter by creation date (ISO 8601)
- `created_before`: Filter by creation date (ISO 8601)

**Response:**
```json
{
  "incidents": [
    {
      "incident_id": "uuid",
      "incident_title": "string",
      "incident_description": "string",
      "incident_type": "string",
      "severity_level": "string",
      "priority_level": "string",
      "status": "string",
      "geolocation": "string",
      "reported_at": "datetime",
      "created_at": "datetime",
      "updated_at": "datetime",
      "resolved_at": "datetime",
      "created_by": "uuid",
      "assigned_to": "uuid",
      "agency_id": "uuid"
    }
  ],
  "pagination": {
    "page": "integer",
    "limit": "integer",
    "total": "integer",
    "pages": "integer"
  }
}
```

### Get Incident by ID
```
GET /incidents/{incident_id}
```

**Response:**
```json
{
  "incident_id": "uuid",
  "incident_title": "string",
  "incident_description": "string",
  "incident_type": "string",
  "severity_level": "string",
  "priority_level": "string",
  "status": "string",
  "geolocation": "string",
  "reported_at": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime",
  "resolved_at": "datetime",
  "created_by": "uuid",
  "assigned_to": "uuid",
  "agency_id": "uuid"
}
```

### Create Incident
```
POST /incidents
```

**Request Body:**
```json
{
  "incident_title": "string",
  "incident_description": "string",
  "incident_type": "string",
  "severity_level": "string",
  "priority_level": "string",
  "status": "string",
  "geolocation": "string",
  "reported_at": "datetime",
  "created_by": "uuid",
  "assigned_to": "uuid",
  "agency_id": "uuid"
}
```

**Response:**
```json
{
  "incident_id": "uuid",
  "incident_title": "string",
  "incident_description": "string",
  "incident_type": "string",
  "severity_level": "string",
  "priority_level": "string",
  "status": "string",
  "geolocation": "string",
  "reported_at": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime",
  "resolved_at": "datetime",
  "created_by": "uuid",
  "assigned_to": "uuid",
  "agency_id": "uuid"
}
```

### Update Incident
```
PUT /incidents/{incident_id}
```

**Request Body:**
```json
{
  "incident_title": "string",
  "incident_description": "string",
  "incident_type": "string",
  "severity_level": "string",
  "priority_level": "string",
  "status": "string",
  "geolocation": "string",
  "reported_at": "datetime",
  "assigned_to": "uuid",
  "agency_id": "uuid"
}
```

**Response:**
```json
{
  "incident_id": "uuid",
  "incident_title": "string",
  "incident_description": "string",
  "incident_type": "string",
  "severity_level": "string",
  "priority_level": "string",
  "status": "string",
  "geolocation": "string",
  "reported_at": "datetime",
  "created_at": "datetime",
  "updated_at": "datetime",
  "resolved_at": "datetime",
  "created_by": "uuid",
  "assigned_to": "uuid",
  "agency_id": "uuid"
}
```

### Delete Incident
```
DELETE /incidents/{incident_id}
```

**Response:**
```json
{
  "message": "Incident deleted successfully"
}
```

### Get Incident Threats
```
GET /incidents/{incident_id}/threats
```

**Response:**
```json
{
  "threats": [
    {
      "threat_id": "uuid",
      "threat_type": "string",
      "threat_source": "string",
      "threat_title": "string",
      "threat_description": "string",
      "severity_score": "number",
      "confidence_score": "number",
      "geolocation": "string",
      "detected_at": "datetime",
      "created_at": "datetime",
      "status": "string",
      "assigned_to": "uuid",
      "agency_id": "uuid"
    }
  ]
}
```

### Add Threat to Incident
```
POST /incidents/{incident_id}/threats
```

**Request Body:**
```json
{
  "threat_id": "uuid"
}
```

**Response:**
```json
{
  "message": "Threat added to incident successfully"
}
```

### Remove Threat from Incident
```
DELETE /incidents/{incident_id}/threats/{threat_id}
```

**Response:**
```json
{
  "message": "Threat removed from incident successfully"
}
```

## Communication

### Get Communication Channels
```
GET /channels
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Number of results per page (default: 10)
- `channel_type`: Filter by channel type (GROUP, DIRECT, BROADCAST)
- `is_active`: Filter by active status

**Response:**
```json
{
  "channels": [
    {
      "channel_id": "uuid",
      "channel_name": "string",
      "channel_type": "string",
      "created_by": "uuid",
      "created_at": "datetime",
      "is_active": "boolean"
    }
  ],
  "pagination": {
    "page": "integer",
    "limit": "integer",
    "total": "integer",
    "pages": "integer"
  }
}
```

### Get Communication Channel by ID
```
GET /channels/{channel_id}
```

**Response:**
```json
{
  "channel_id": "uuid",
  "channel_name": "string",
  "channel_type": "string",
  "created_by": "uuid",
  "created_at": "datetime",
  "is_active": "boolean"
}
```

### Create Communication Channel
```
POST /channels
```

**Request Body:**
```json
{
  "channel_name": "string",
  "channel_type": "string"
}
```

**Response:**
```json
{
  "channel_id": "uuid",
  "channel_name": "string",
  "channel_type": "string",
  "created_by": "uuid",
  "created_at": "datetime",
  "is_active": "boolean"
}
```

### Update Communication Channel
```
PUT /channels/{channel_id}
```

**Request Body:**
```json
{
  "channel_name": "string",
  "is_active": "boolean"
}
```

**Response:**
```json
{
  "channel_id": "uuid",
  "channel_name": "string",
  "channel_type": "string",
  "created_by": "uuid",
  "created_at": "datetime",
  "is_active": "boolean"
}
```

### Delete Communication Channel
```
DELETE /channels/{channel_id}
```

**Response:**
```json
{
  "message": "Channel deleted successfully"
}
```

### Get Channel Members
```
GET /channels/{channel_id}/members
```

**Response:**
```json
{
  "members": [
    {
      "user_id": "uuid",
      "username": "string",
      "first_name": "string",
      "last_name": "string",
      "role_in_channel": "string",
      "joined_at": "datetime"
    }
  ]
}
```

### Add Member to Channel
```
POST /channels/{channel_id}/members
```

**Request Body:**
```json
{
  "user_id": "uuid",
  "role_in_channel": "string"
}
```

**Response:**
```json
{
  "message": "Member added to channel successfully"
}
```

### Remove Member from Channel
```
DELETE /channels/{channel_id}/members/{user_id}
```

**Response:**
```json
{
  "message": "Member removed from channel successfully"
}
```

### Get Messages
```
GET /channels/{channel_id}/messages
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Number of results per page (default: 10)
- `after`: Filter by message timestamp (ISO 8601)

**Response:**
```json
{
  "messages": [
    {
      "message_id": "uuid",
      "sender_id": "uuid",
      "sender_name": "string",
      "message_content": "string",
      "sent_at": "datetime",
      "read_at": "datetime"
    }
  ],
  "pagination": {
    "page": "integer",
    "limit": "integer",
    "total": "integer",
    "pages": "integer"
  }
}
```

### Send Message
```
POST /channels/{channel_id}/messages
```

**Request Body:**
```json
{
  "message_content": "string"
}
```

**Response:**
```json
{
  "message_id": "uuid",
  "sender_id": "uuid",
  "message_content": "string",
  "sent_at": "datetime"
}
```

## Analytics

### Get Incident Analytics
```
GET /analytics/incidents
```

**Query Parameters:**
- `start_date`: Start date for analytics (ISO 8601)
- `end_date`: End date for analytics (ISO 8601)
- `agency_id`: Filter by agency

**Response:**
```json
{
  "total_incidents": "integer",
  "incidents_by_type": "object",
  "incidents_by_severity": "object",
  "average_response_time": "string",
  "average_resolution_time": "string",
  "resolution_rate": "number"
}
```

### Get Threat Analytics
```
GET /analytics/threats
```

**Query Parameters:**
- `start_date`: Start date for analytics (ISO 8601)
- `end_date`: End date for analytics (ISO 8601)
- `agency_id`: Filter by agency

**Response:**
```json
{
  "total_threats": "integer",
  "threats_by_type": "object",
  "threats_by_severity": "object",
  "detection_rate": "number",
  "false_positive_rate": "number"
}
```

### Get User Analytics
```
GET /analytics/users
```

**Query Parameters:**
- `start_date`: Start date for analytics (ISO 8601)
- `end_date`: End date for analytics (ISO 8601)
- `agency_id`: Filter by agency

**Response:**
```json
{
  "total_users": "integer",
  "active_users": "integer",
  "user_roles": "object",
  "login_activity": "object"
}
```

### Generate Report
```
POST /analytics/reports
```

**Request Body:**
```json
{
  "report_type": "string",
  "start_date": "datetime",
  "end_date": "datetime",
  "agency_id": "uuid"
}
```

**Response:**
```json
{
  "report_id": "uuid",
  "report_title": "string",
  "report_type": "string",
  "generated_at": "datetime",
  "file_url": "string"
}
```

## External Integrations

### Social Media Integration
```
GET /external/social/feed
```

**Query Parameters:**
- `source`: Social media source (twitter, facebook, instagram)
- `query`: Search query
- `limit`: Number of results

**Response:**
```json
{
  "posts": [
    {
      "post_id": "string",
      "source": "string",
      "author": "string",
      "content": "string",
      "timestamp": "datetime",
      "location": "string",
      "sentiment": "string"
    }
  ]
}
```

### IoT Device Integration
```
GET /external/iot/devices/{device_id}/data
```

**Query Parameters:**
- `start_time`: Start time for data retrieval (ISO 8601)
- `end_time`: End time for data retrieval (ISO 8601)
- `limit`: Number of data points

**Response:**
```json
{
  "device_id": "uuid",
  "data": [
    {
      "timestamp": "datetime",
      "sensor_data": "object"
    }
  ]
}
```

### Satellite Data Integration
```
GET /external/satellite/imagery
```

**Query Parameters:**
- `location`: Geographic location
- `start_date`: Start date for imagery (ISO 8601)
- `end_date`: End date for imagery (ISO 8601)
- `resolution`: Image resolution

**Response:**
```json
{
  "images": [
    {
      "image_id": "string",
      "url": "string",
      "timestamp": "datetime",
      "location": "string",
      "resolution": "string"
    }
  ]
}
```

## Error Handling

### Standard Error Response
All error responses follow a consistent format:

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "object"
  }
}
```

### Common Error Codes
- `VALIDATION_ERROR`: Request data validation failed
- `AUTHENTICATION_ERROR`: Authentication failed
- `AUTHORIZATION_ERROR`: Insufficient permissions
- `NOT_FOUND`: Resource not found
- `CONFLICT`: Resource conflict
- `RATE_LIMIT_EXCEEDED`: Rate limit exceeded
- `INTERNAL_ERROR`: Internal server error

## Rate Limiting

### Rate Limits
- **Anonymous Requests**: 100 requests per hour
- **Authenticated Requests**: 1000 requests per hour
- **Admin Requests**: 5000 requests per hour

### Rate Limit Response Headers
- `X-RateLimit-Limit`: Request limit
- `X-RateLimit-Remaining`: Requests remaining
- `X-RateLimit-Reset`: Time when rate limit resets (Unix timestamp)

## API Versioning

### Versioning Strategy
The API uses URL versioning with the version number in the path:

```
https://api.civicshield.example.com/v1/
```

### Version Deprecation
Old API versions will be deprecated with a 6-month notice period.

## Security

### Transport Security
- **HTTPS**: All API requests must be made over HTTPS
- **TLS**: Minimum TLS 1.2 required

### Authentication Security
- **JWT**: JSON Web Tokens for authentication
- **Token Expiration**: Access tokens expire in 1 hour
- **Refresh Tokens**: Refresh tokens expire in 7 days

### Data Security
- **Encryption**: All sensitive data is encrypted at rest
- **Masking**: Sensitive data is masked in logs
- **Audit Trail**: All API requests are logged

## Conclusion

The CivicShield API provides a comprehensive set of endpoints for managing threats, incidents, users, and communications. Through proper authentication, rate limiting, and security measures, the API ensures secure and reliable access to the platform's functionality for government defense and homeland security agencies.