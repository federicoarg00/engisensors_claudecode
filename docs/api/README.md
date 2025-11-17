# EngiSensors API Documentation

## Overview

RESTful API documentation for the EngiSensors platform.

## API Endpoints

### Authentication

```
POST /api/auth/login
POST /api/auth/logout
POST /api/auth/refresh
POST /api/auth/forgot-password
```

### Clients (Admin only)

```
GET    /api/clients
POST   /api/clients
GET    /api/clients/{id}
PUT    /api/clients/{id}
DELETE /api/clients/{id}
```

### Buildings

```
GET    /api/buildings
POST   /api/buildings
GET    /api/buildings/{id}
PUT    /api/buildings/{id}
DELETE /api/buildings/{id}
GET    /api/buildings/{id}/sensors  # All sensors in building
```

### Apartments

```
GET    /api/apartments
POST   /api/apartments
GET    /api/apartments/{id}
PUT    /api/apartments/{id}
DELETE /api/apartments/{id}
```

### Locations

```
GET    /api/locations
POST   /api/locations
GET    /api/locations/{id}
PUT    /api/locations/{id}
DELETE /api/locations/{id}
```

### Sensors

```
GET    /api/sensors
POST   /api/sensors
GET    /api/sensors/{id}
PUT    /api/sensors/{id}
DELETE /api/sensors/{id}
GET    /api/sensors/{id}/events  # Historical events
GET    /api/sensors/{id}/status  # Current status
```

### Contacts

```
GET    /api/contacts
POST   /api/contacts
GET    /api/contacts/{id}
PUT    /api/contacts/{id}
DELETE /api/contacts/{id}
PATCH  /api/contacts/{id}/toggle  # Activate/deactivate
```

### Events

```
GET    /api/events
GET    /api/events/{id}
GET    /api/events/recent  # Last 24h
```

### Notifications

```
GET    /api/notifications
GET    /api/notifications/{id}
POST   /api/notifications/test  # Send test notification
```

### WebSocket

```
WS /ws  # Real-time updates
```

## Authentication

All endpoints (except `/api/auth/login`) require JWT authentication:

```
Authorization: Bearer <token>
```

## Response Format

### Success Response

```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": { ... }
  }
}
```

## Rate Limiting

- **General:** 100 requests/minute per IP
- **Login:** 5 requests/minute per IP
- **Notifications:** 10 requests/minute per user

## OpenAPI/Swagger

Interactive API documentation available at:
```
http://localhost:8000/docs        # Swagger UI
http://localhost:8000/redoc       # ReDoc
http://localhost:8000/openapi.json # OpenAPI Schema
```

---

**Last Updated:** 2025-11-17
