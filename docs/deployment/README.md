# EngiSensors Deployment Guide

## Overview

Deployment instructions and infrastructure configuration for EngiSensors.

## Deployment Environments

### Development
- Local development with Docker Compose
- Hot reload enabled
- Debug logging
- Mock notification services

### Staging
- Pre-production testing environment
- Mirrors production configuration
- Real notification services with test recipients
- Performance testing

### Production
- High availability configuration
- Load balanced services
- Automated backups
- Monitoring and alerting
- 99.9% uptime SLA

## Infrastructure Requirements

### Minimum Requirements (MVP)

**Application Server:**
- 2 vCPU
- 4 GB RAM
- 50 GB SSD

**Database Server:**
- 2 vCPU
- 8 GB RAM
- 100 GB SSD (with auto-scaling)

**MQTT Broker:**
- 1 vCPU
- 2 GB RAM
- 20 GB SSD

### Recommended Production Setup

**Load Balancer:**
- Nginx or cloud provider LB
- SSL/TLS termination
- HTTP/2 support

**Application Servers (2+):**
- 4 vCPU
- 8 GB RAM
- Auto-scaling based on load

**Database:**
- PostgreSQL 15+ with TimescaleDB
- Primary + Replica setup
- Automated backups (daily + point-in-time recovery)
- 500 GB SSD minimum

**Cache/Queue:**
- Redis cluster (3 nodes)
- 4 GB RAM each

**MQTT Broker:**
- EMQX cluster (3 nodes)
- 4 GB RAM each
- Persistent sessions enabled

## Docker Compose Setup (Development)

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: timescale/timescaledb:latest-pg15
    environment:
      POSTGRES_DB: engisensors
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  mqtt:
    image: eclipse-mosquitto:2
    volumes:
      - ./config/mosquitto.conf:/mosquitto/config/mosquitto.conf
    ports:
      - "1883:1883"
      - "9001:9001"

  backend:
    build: ./src/backend
    environment:
      DATABASE_URL: ${DATABASE_URL}
      REDIS_URL: ${REDIS_URL}
      MQTT_BROKER_URL: ${MQTT_BROKER_URL}
      JWT_SECRET: ${JWT_SECRET}
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
      - mqtt

  frontend:
    build: ./src/frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  postgres_data:
```

## Environment Variables

```bash
# .env.example
DATABASE_URL=postgresql://user:pass@localhost:5432/engisensors
REDIS_URL=redis://localhost:6379
MQTT_BROKER_URL=mqtt://localhost:1883

JWT_SECRET=<random-secret-key>
JWT_EXPIRATION=3600

SENDGRID_API_KEY=<your-key>
TWILIO_ACCOUNT_SID=<your-sid>
TWILIO_AUTH_TOKEN=<your-token>
TWILIO_PHONE_NUMBER=<your-number>

ENVIRONMENT=development
LOG_LEVEL=DEBUG
```

## Deployment Steps

### Using Docker Compose

```bash
# 1. Clone repository
git clone https://github.com/federicoarg00/engisensors_claudecode.git
cd engisensors_claudecode

# 2. Configure environment
cp .env.example .env
# Edit .env with your values

# 3. Build and start services
docker-compose up -d

# 4. Run database migrations
docker-compose exec backend alembic upgrade head

# 5. Create initial admin user
docker-compose exec backend python scripts/create_admin.py

# 6. Verify services
curl http://localhost:8000/health
```

### Using Kubernetes (Production)

*To be documented when ready for production deployment*

## Monitoring

### Health Checks

```bash
# Application health
curl http://localhost:8000/health

# Database health
curl http://localhost:8000/health/db

# MQTT broker health
curl http://localhost:8000/health/mqtt

# Redis health
curl http://localhost:8000/health/redis
```

### Metrics

Prometheus metrics available at:
```
http://localhost:8000/metrics
```

### Logging

Centralized logging with structured JSON format:
```json
{
  "timestamp": "2025-11-17T10:30:45Z",
  "level": "INFO",
  "service": "mqtt-handler",
  "message": "Gas alert processed",
  "sensor_id": "S001",
  "gas_level": 850
}
```

## Backup and Recovery

### Database Backups

```bash
# Daily automated backup
0 2 * * * pg_dump engisensors | gzip > backup_$(date +%Y%m%d).sql.gz

# Point-in-time recovery enabled with WAL archiving
```

### Disaster Recovery

- **RTO (Recovery Time Objective):** < 1 hour
- **RPO (Recovery Point Objective):** < 15 minutes

## Security Checklist

- [ ] HTTPS/TLS enabled
- [ ] MQTT over TLS
- [ ] Firewall configured (allow only necessary ports)
- [ ] Database access restricted to application servers
- [ ] Secrets stored in secret manager (not env files)
- [ ] Regular security updates applied
- [ ] Monitoring and alerting configured
- [ ] Backups tested regularly

---

**Last Updated:** 2025-11-17
