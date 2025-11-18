# EngiSensors API Documentation

**Version:** 0.1.0
**Base URL:** `http://localhost:8000` (development)
**API Prefix:** `/api/v1`

---

## Table of Contents

1. [Authentication](#authentication)
2. [Health Checks](#health-checks)
3. [Sensors](#sensors)
4. [Clients](#clients)
5. [Error Responses](#error-responses)
6. [Database Migrations](#database-migrations)

---

## Authentication

🚧 **Status:** Not yet implemented
Authentication using JWT tokens will be added in the next phase.

---

## Health Checks

### GET /health

Basic health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "environment": "development",
  "version": "0.1.0"
}
```

### GET /health/mqtt

MQTT service health check.

**Response:**
```json
{
  "status": "healthy",
  "mqtt_broker": "www.trustcapsupes.com",
  "connected": true
}
```

### GET /health/db

Database health check.

**Response:**
```json
{
  "status": "healthy",
  "database": "PostgreSQL + TimescaleDB",
  "connected": true
}
```

---

## Sensors

### POST /api/v1/sensors

Register a new gas sensor in the system.

**Request Body:**
```json
{
  "device_id": "S-TC-203-001",
  "location_id": "550e8400-e29b-41d4-a716-446655440000",
  "model": "MQ-4 Gas Sensor",
  "firmware_version": "1.2.3",
  "gas_threshold_ppm": 800
}
```

**Response:** `201 Created`
```json
{
  "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "device_id": "S-TC-203-001",
  "model": "MQ-4 Gas Sensor",
  "firmware_version": "1.2.3",
  "status": "inactive",
  "gas_threshold_ppm": 800,
  "battery_level": null,
  "signal_strength": null,
  "last_seen": null,
  "location_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2025-11-18T10:30:00Z",
  "updated_at": "2025-11-18T10:30:00Z"
}
```

**Errors:**
- `400 Bad Request`: Device ID already exists
- `404 Not Found`: Location not found

### GET /api/v1/sensors

List all sensors with location hierarchy.

**Query Parameters:**
- `skip` (int, default: 0): Number of records to skip
- `limit` (int, default: 100, max: 1000): Maximum records to return
- `status` (enum): Filter by sensor status (`active`, `inactive`, `alert`, `maintenance`, `disconnected`)
- `client_id` (UUID): Filter by client ID
- `building_id` (UUID): Filter by building ID

**Response:** `200 OK`
```json
[
  {
    "id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
    "device_id": "S-TC-203-001",
    "model": "MQ-4 Gas Sensor",
    "firmware_version": "1.2.3",
    "status": "active",
    "gas_threshold_ppm": 800,
    "battery_level": 85,
    "signal_strength": -45,
    "last_seen": "2025-11-18T10:45:00Z",
    "location_id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2025-11-18T10:30:00Z",
    "updated_at": "2025-11-18T10:45:00Z",
    "location": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "type": "cocina",
      "description": "Cocina principal"
    },
    "apartment": {
      "id": "450e8400-e29b-41d4-a716-446655440000",
      "number": "203",
      "floor": "2"
    },
    "building": {
      "id": "350e8400-e29b-41d4-a716-446655440000",
      "name": "Torre Central",
      "address": "Av. Reforma 2350, CDMX"
    },
    "client": {
      "id": "250e8400-e29b-41d4-a716-446655440000",
      "name": "Inmobiliaria Reforma",
      "company": "Grupo Reforma SA de CV"
    }
  }
]
```

### GET /api/v1/sensors/{sensor_id}

Get sensor by ID with full location hierarchy.

**Path Parameters:**
- `sensor_id` (UUID): Sensor ID

**Response:** `200 OK` (same structure as list item above)

**Errors:**
- `404 Not Found`: Sensor not found

### GET /api/v1/sensors/device/{device_id}

Get sensor by device ID (useful for MQTT handler).

**Path Parameters:**
- `device_id` (string): Device identifier (e.g., "S-TC-203-001")

**Response:** `200 OK` (same structure as GET by ID)

**Errors:**
- `404 Not Found`: Sensor not found

### PATCH /api/v1/sensors/{sensor_id}

Update sensor information.

**Path Parameters:**
- `sensor_id` (UUID): Sensor ID

**Request Body (all fields optional):**
```json
{
  "model": "MQ-4 Gas Sensor v2",
  "firmware_version": "1.3.0",
  "gas_threshold_ppm": 750,
  "status": "maintenance",
  "location_id": "660e8400-e29b-41d4-a716-446655440000"
}
```

**Response:** `200 OK` (updated sensor object)

**Errors:**
- `404 Not Found`: Sensor or new location not found

### PATCH /api/v1/sensors/{sensor_id}/status

Update sensor status, battery, and signal strength.

**Path Parameters:**
- `sensor_id` (UUID): Sensor ID

**Request Body:**
```json
{
  "status": "active",
  "battery_level": 75,
  "signal_strength": -50
}
```

**Response:** `200 OK` (updated sensor object)

**Errors:**
- `404 Not Found`: Sensor not found

### DELETE /api/v1/sensors/{sensor_id}

Delete a sensor (also deletes all associated sensor events).

**Path Parameters:**
- `sensor_id` (UUID): Sensor ID

**Response:** `204 No Content`

**Errors:**
- `404 Not Found`: Sensor not found

---

## Clients

### POST /api/v1/clients

Create a new client.

**Request Body:**
```json
{
  "name": "Juan Pérez",
  "company": "Inmobiliaria Reforma SA de CV",
  "email": "contacto@reforma.com",
  "phone": "+52 55 1234 5678",
  "address": "Av. Reforma 2350, CDMX",
  "user_id": null
}
```

**Response:** `201 Created`
```json
{
  "id": "250e8400-e29b-41d4-a716-446655440000",
  "name": "Juan Pérez",
  "company": "Inmobiliaria Reforma SA de CV",
  "email": "contacto@reforma.com",
  "phone": "+52 55 1234 5678",
  "address": "Av. Reforma 2350, CDMX",
  "is_active": true,
  "user_id": null,
  "created_at": "2025-11-18T10:00:00Z",
  "updated_at": "2025-11-18T10:00:00Z"
}
```

### GET /api/v1/clients

List all clients with statistics.

**Query Parameters:**
- `skip` (int, default: 0): Number of records to skip
- `limit` (int, default: 100, max: 1000): Maximum records to return
- `is_active` (bool): Filter by active status

**Response:** `200 OK`
```json
[
  {
    "id": "250e8400-e29b-41d4-a716-446655440000",
    "name": "Juan Pérez",
    "company": "Inmobiliaria Reforma SA de CV",
    "email": "contacto@reforma.com",
    "phone": "+52 55 1234 5678",
    "address": "Av. Reforma 2350, CDMX",
    "is_active": true,
    "user_id": null,
    "created_at": "2025-11-18T10:00:00Z",
    "updated_at": "2025-11-18T10:00:00Z",
    "total_buildings": 3,
    "total_sensors": 27,
    "active_sensors": 25,
    "alert_sensors": 1
  }
]
```

### GET /api/v1/clients/{client_id}

Get client by ID with statistics.

**Path Parameters:**
- `client_id` (UUID): Client ID

**Response:** `200 OK` (same structure as list item above)

**Errors:**
- `404 Not Found`: Client not found

### PATCH /api/v1/clients/{client_id}

Update client information.

**Path Parameters:**
- `client_id` (UUID): Client ID

**Request Body (all fields optional):**
```json
{
  "name": "Juan Carlos Pérez",
  "phone": "+52 55 9876 5432",
  "is_active": false
}
```

**Response:** `200 OK` (updated client object)

**Errors:**
- `404 Not Found`: Client not found

### DELETE /api/v1/clients/{client_id}

Delete a client (also deletes all associated buildings, apartments, locations, sensors, and events).

⚠️ **Warning:** This operation is destructive and will cascade delete all related data!

**Path Parameters:**
- `client_id` (UUID): Client ID

**Response:** `204 No Content`

**Errors:**
- `404 Not Found`: Client not found

---

## Error Responses

All error responses follow this structure:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

**Common HTTP Status Codes:**
- `400 Bad Request`: Invalid input data
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error (Pydantic)
- `500 Internal Server Error`: Server error

**Validation Error Example (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "gas_threshold_ppm"],
      "msg": "ensure this value is less than or equal to 10000",
      "type": "value_error.number.not_le"
    }
  ]
}
```

---

## Database Migrations

### Initialize Database

Run migrations and set up TimescaleDB:

```bash
cd /home/user/engisensors_claudecode
python scripts/init_db.py
```

This will:
1. Enable TimescaleDB extension
2. Run Alembic migrations to create all tables
3. Convert `sensor_events` to TimescaleDB hypertable
4. Set up compression policy (7 days)
5. Set up retention policy (2 years)
6. Create performance indexes

### Create Admin User

After database initialization:

```bash
python scripts/create_admin.py
```

### Alembic Commands

Located in `src/backend/`:

```bash
cd src/backend

# Create a new migration (after model changes)
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show current revision
alembic current

# Show migration history
alembic history
```

---

## Testing Endpoints

### Using curl

**Create a client:**
```bash
curl -X POST http://localhost:8000/api/v1/clients \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Client",
    "company": "Test Company",
    "email": "test@example.com"
  }'
```

**List sensors with filters:**
```bash
curl "http://localhost:8000/api/v1/sensors?status=alert&limit=10"
```

### Using HTTPie

```bash
# Create a client
http POST http://localhost:8000/api/v1/clients \
  name="Test Client" \
  company="Test Company" \
  email="test@example.com"

# List sensors
http GET http://localhost:8000/api/v1/sensors status==alert limit==10
```

### Using Swagger UI

Navigate to: `http://localhost:8000/docs`

Interactive API documentation with "Try it out" functionality.

### Using ReDoc

Navigate to: `http://localhost:8000/redoc`

Alternative API documentation format.

---

## MQTT Integration

Sensors automatically send data to MQTT broker at `www.trustcapsupes.com:1883`.

**Topic Structure:**
```
engisensors/{client_id}/{building_id}/{apartment_id}/{sensor_id}/status
```

**Message Format:**
```json
{
  "sensor_id": "S-TC-203-001",
  "timestamp": "2025-11-18T10:45:00Z",
  "status": "alert",
  "gas_level": 850,
  "threshold": 800,
  "battery": 85,
  "signal_strength": -45
}
```

**Gas Levels:**
- `0-799 PPM`: Normal (status: "normal")
- `≥800 PPM`: Alert (status: "alert", default threshold)
- Threshold configurable per sensor

---

## Next Steps

**Endpoints to be implemented:**
- `/api/v1/buildings` - Building CRUD
- `/api/v1/apartments` - Apartment CRUD
- `/api/v1/locations` - Location CRUD
- `/api/v1/sensor-events` - Query sensor events (read-only)
- `/api/v1/contacts` - Contact CRUD
- `/api/v1/notifications` - Notification history (read-only)
- `/api/v1/auth/login` - JWT authentication
- `/api/v1/auth/logout` - Logout
- `/api/v1/users` - User management (admin only)

**Features to be added:**
- JWT authentication and authorization
- WebSocket for real-time updates
- Notification service (email/SMS)
- Dashboard API endpoints (aggregated statistics)
- Data export (CSV, JSON)
- Sensor calibration endpoints
- Batch operations
