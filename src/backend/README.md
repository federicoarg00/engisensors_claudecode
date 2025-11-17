# EngiSensors Backend

Backend API service for the EngiSensors IoT gas monitoring platform.

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+ with TimescaleDB
- Redis 7+
- Access to MQTT broker at www.trustcapsupes.com

### Local Development with Docker

1. **Copy environment file:**
   ```bash
   cp ../../.env.example ../../.env
   # Edit .env with your configuration
   ```

2. **Start services:**
   ```bash
   cd ../..  # Go to project root
   docker-compose up -d
   ```

3. **Check logs:**
   ```bash
   docker-compose logs -f backend
   ```

4. **Access API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Health check: http://localhost:8000/health
   - MQTT status: http://localhost:8000/health/mqtt

### Local Development without Docker

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment:**
   ```bash
   cp ../../.env.example ../../.env
   # Edit .env with your configuration
   ```

4. **Run the application:**
   ```bash
   python -m app.main
   # Or with uvicorn directly:
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## MQTT Configuration

The backend connects to an external MQTT broker at **www.trustcapsupes.com**.

### Environment Variables

```bash
MQTT_BROKER_HOST=www.trustcapsupes.com
MQTT_BROKER_PORT=1883
MQTT_BROKER_USERNAME=  # If authentication required
MQTT_BROKER_PASSWORD=  # If authentication required
MQTT_BASE_TOPIC=engisensors/#
```

### Topic Structure

Sensors publish to:
```
engisensors/{client_id}/{building_id}/{apartment_id}/{sensor_id}/status
```

### Message Format

```json
{
  "sensor_id": "S001",
  "timestamp": "2025-11-17T10:30:45Z",
  "status": "alert",
  "gas_level": 850,
  "threshold": 800,
  "battery": 85,
  "signal_strength": -45
}
```

## Testing MQTT Connection

You can test the MQTT connection using mosquitto clients:

```bash
# Subscribe to all topics
mosquitto_sub -h www.trustcapsupes.com -p 1883 -t "engisensors/#" -v

# Publish test message
mosquitto_pub -h www.trustcapsupes.com -p 1883 \
  -t "engisensors/test/building1/apt101/S001/status" \
  -m '{"sensor_id":"S001","timestamp":"2025-11-17T10:30:00Z","status":"normal","gas_level":100,"threshold":800,"battery":95,"signal_strength":-40}'

# Publish alert
mosquitto_pub -h www.trustcapsupes.com -p 1883 \
  -t "engisensors/test/building1/apt101/S001/status" \
  -m '{"sensor_id":"S001","timestamp":"2025-11-17T10:30:00Z","status":"alert","gas_level":850,"threshold":800,"battery":95,"signal_strength":-40}'
```

## Project Structure

```
src/backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection (to be implemented)
│   ├── models/              # SQLAlchemy models (to be implemented)
│   ├── routes/              # API endpoints (to be implemented)
│   ├── schemas/             # Pydantic schemas (to be implemented)
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   ├── mqtt_handler.py  # MQTT service ✅
│   │   └── notification_service.py  # (to be implemented)
│   └── utils/               # Utilities (to be implemented)
├── alembic/                 # Database migrations (to be set up)
├── requirements.txt         # Python dependencies
├── Dockerfile               # Production container image
└── README.md                # This file
```

## API Endpoints

### Health & Status
- `GET /` - Root endpoint
- `GET /health` - General health check
- `GET /health/mqtt` - MQTT connection status

### Authentication (to be implemented)
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/logout`
- `POST /api/v1/auth/refresh`

### Clients (to be implemented)
- `GET /api/v1/clients` - List clients
- `POST /api/v1/clients` - Create client
- `GET /api/v1/clients/{id}` - Get client
- etc...

See [docs/api/README.md](../../docs/api/README.md) for complete API documentation.

## Development

### Code Style

- **Formatter:** Black
- **Linter:** Ruff
- **Type Checker:** MyPy

```bash
# Format code
black app/

# Lint code
ruff check app/

# Type check
mypy app/
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_mqtt_handler.py
```

## Deployment to Coolify

### Prerequisites

1. Coolify installed on your VPS
2. GitHub repository connected to Coolify
3. Environment variables configured in Coolify

### Steps

1. **Connect Repository:**
   - In Coolify, add this repository as a new project
   - Select the branch to deploy (e.g., `main`)

2. **Configure Build:**
   - Build Pack: Docker
   - Dockerfile Path: `src/backend/Dockerfile`
   - Build Command: (leave default)

3. **Set Environment Variables:**
   - Copy all variables from `.env.example`
   - Set production values in Coolify's environment settings
   - **Important:** Set `ENVIRONMENT=production` and `DEBUG=False`

4. **Configure Networking:**
   - Expose port: 8000
   - Set up domain/subdomain (e.g., api.engisensors.com)
   - Enable HTTPS

5. **Deploy:**
   - Click "Deploy" in Coolify
   - Monitor deployment logs
   - Verify health check: https://api.engisensors.com/health

### Production Environment Variables

Critical variables for production:

```bash
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=<strong-random-key>
JWT_SECRET_KEY=<strong-random-key>

DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379/0

MQTT_BROKER_HOST=www.trustcapsupes.com
MQTT_BROKER_PORT=1883
MQTT_BROKER_USERNAME=<if-required>
MQTT_BROKER_PASSWORD=<if-required>

SENDGRID_API_KEY=<your-key>
TWILIO_ACCOUNT_SID=<your-sid>
TWILIO_AUTH_TOKEN=<your-token>
TWILIO_PHONE_NUMBER=<your-number>

CORS_ORIGINS=https://engisensors.com,https://www.engisensors.com
```

## Monitoring

### Logs

View application logs:
```bash
docker-compose logs -f backend
```

### Metrics

Prometheus metrics available at:
```
http://localhost:8000/metrics
```

## Troubleshooting

### MQTT Connection Issues

**Problem:** Cannot connect to MQTT broker

**Solutions:**
1. Check broker is accessible:
   ```bash
   ping www.trustcapsupes.com
   telnet www.trustcapsupes.com 1883
   ```

2. Verify credentials if authentication is enabled

3. Check firewall rules on both sides

4. Review backend logs for error details:
   ```bash
   docker-compose logs backend | grep MQTT
   ```

### Database Connection Issues

**Problem:** Cannot connect to PostgreSQL

**Solutions:**
1. Verify PostgreSQL is running:
   ```bash
   docker-compose ps postgres
   ```

2. Check DATABASE_URL is correct in .env

3. Test connection:
   ```bash
   docker-compose exec postgres psql -U engisensors -d engisensors
   ```

## Support

For issues and questions:
- Check [CLAUDE.md](../../CLAUDE.md) for development guidelines
- Review [PRD.md](../../PRD.md) for product requirements
- See troubleshooting section in [CLAUDE.md](../../CLAUDE.md#troubleshooting)

---

**Version:** 0.1.0
**Last Updated:** 2025-11-17
