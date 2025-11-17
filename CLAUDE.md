# CLAUDE.md - EngiSensors Project Guide for AI Assistants

**Last Updated:** 2025-11-17
**Repository:** engisensors_claudecode
**Status:** Initial Setup

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Repository Structure](#repository-structure)
3. [Development Workflows](#development-workflows)
4. [Coding Conventions](#coding-conventions)
5. [Testing Guidelines](#testing-guidelines)
6. [Git Workflows](#git-workflows)
7. [AI Assistant Guidelines](#ai-assistant-guidelines)
8. [Common Tasks](#common-tasks)
9. [Troubleshooting](#troubleshooting)

---

## Project Overview

### Purpose
EngiSensors is an IoT platform for monitoring and managing combustible gas sensors in residential and industrial environments. The system receives real-time data from distributed gas sensors via MQTT protocol and provides a multi-channel alerting system (email, SMS) to notify stakeholders of potentially dangerous gas leaks.

**Critical Mission:** Prevent accidents, explosions, and poisoning through early detection and rapid notification of gas leaks.

### Technology Stack

#### Backend (Proposed)
- **Language:** Python 3.11+ (FastAPI) or Node.js 20+ (NestJS)
- **Database:** PostgreSQL 15+ with TimescaleDB extension for time-series data
- **Cache:** Redis 7+ (sessions, caching, rate limiting)
- **Message Broker:** MQTT (Mosquitto or EMQX)
- **Queue:** RabbitMQ or Redis Streams for notification processing

#### Frontend (Proposed)
- **Framework:** React 18+ or Vue 3+
- **UI Library:** Material UI, Ant Design, or Tailwind CSS
- **Real-time:** Socket.io or WebSockets for live updates
- **Charts:** Chart.js or Recharts for sensor data visualization

#### DevOps
- **Containerization:** Docker + Docker Compose (MVP), Kubernetes (production)
- **CI/CD:** GitHub Actions
- **Monitoring:** Prometheus + Grafana
- **Logging:** Structured JSON logs with centralized collection

#### External Services
- **Email Notifications:** SendGrid, AWS SES, or Mailgun
- **SMS Notifications:** Twilio, AWS SNS, or MessageBird

### Key Components
- **MQTT Handler Service:** Receives and processes sensor messages
- **Notification Service:** Multi-channel alert system (email, SMS)
- **API Layer:** RESTful APIs for CRUD operations and data queries
- **WebSocket Service:** Real-time dashboard updates
- **Web Dashboard:** Client and admin interfaces
- **Data Hierarchy Management:** Client → Building → Apartment → Location → Sensor
- **Contact Management:** Email and phone contacts for notifications
- **Event Logging:** Historical record of all detections and alerts

---

## Repository Structure

```
engisensors_claudecode/
├── CLAUDE.md              # This file - AI assistant guide
├── README.md              # Project README
├── docs/                  # Documentation
│   ├── architecture.md    # System architecture
│   ├── api/              # API documentation
│   └── sensors/          # Sensor specifications
├── src/                   # Source code
│   ├── backend/          # Backend services
│   ├── frontend/         # Frontend application
│   ├── common/           # Shared utilities
│   └── config/           # Configuration files
├── tests/                 # Test suites
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── e2e/              # End-to-end tests
├── scripts/              # Build and deployment scripts
├── docker/               # Docker configurations
└── .github/              # GitHub workflows and templates
```

*Note: This structure will be refined as the project develops.*

---

## Development Workflows

### Initial Setup

```bash
# Clone the repository
git clone <repository-url>
cd engisensors_claudecode

# Install dependencies (update when determined)
# npm install  # or
# pip install -r requirements.txt  # or
# go mod download
```

### Branch Naming Conventions

- **Feature branches:** `feature/<descriptive-name>`
- **Bug fixes:** `fix/<issue-description>`
- **Documentation:** `docs/<topic>`
- **Refactoring:** `refactor/<component>`
- **Claude branches:** `claude/claude-md-<session-id>` (auto-generated)

### Development Cycle

1. **Create branch** from main/master
2. **Implement changes** with frequent commits
3. **Write tests** for new functionality
4. **Run test suite** before committing
5. **Update documentation** as needed
6. **Create PR** with detailed description
7. **Code review** and address feedback
8. **Merge** after approval

---

## Coding Conventions

### General Principles

- **Code clarity over cleverness** - prioritize readable, maintainable code
- **DRY (Don't Repeat Yourself)** - extract common patterns
- **SOLID principles** - especially Single Responsibility
- **Fail fast** - validate inputs early, handle errors explicitly
- **Security first** - never commit secrets, validate all inputs

### Code Style

*Update when language(s) are chosen:*

#### Python (if used)
- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use docstrings for all public functions/classes
- Format with `black`
- Lint with `ruff` or `pylint`

#### JavaScript/TypeScript (if used)
- Follow Airbnb style guide
- Use ESLint and Prettier
- Prefer TypeScript over JavaScript
- Use async/await over promises chains
- Maximum line length: 100 characters

#### Go (if used)
- Follow effective Go guidelines
- Use `gofmt` and `golint`
- Document all exported functions/types
- Handle all errors explicitly

### Naming Conventions

- **Variables/Functions:** descriptive names, avoid abbreviations
- **Constants:** UPPER_SNAKE_CASE (or language-specific convention)
- **Classes:** PascalCase
- **Files:** snake_case or kebab-case (maintain consistency)
- **Sensors:** Use manufacturer and model in naming (e.g., `bme280_temp_sensor`)

### Comments and Documentation

- **Why, not what** - explain reasoning, not obvious code
- **TODO comments** - include ticket numbers: `// TODO(#123): implement retry logic`
- **API documentation** - document all public interfaces
- **Inline comments** - for complex algorithms or non-obvious decisions

---

## Testing Guidelines

### Test Coverage Requirements

- **Minimum coverage:** 80% for new code
- **Critical paths:** 100% coverage for sensor data processing, API endpoints
- **Unit tests:** Test individual components in isolation
- **Integration tests:** Test component interactions
- **E2E tests:** Test complete user workflows

### Test Structure

```
# Pattern: Arrange-Act-Assert
def test_sensor_reading_validation():
    # Arrange
    sensor = TemperatureSensor(config)
    invalid_data = {"temp": "invalid"}

    # Act
    result = sensor.validate(invalid_data)

    # Assert
    assert result.is_valid == False
    assert "temperature" in result.errors
```

### Test Naming

- Use descriptive names: `test_<what>_<condition>_<expected_result>`
- Example: `test_sensor_reading_when_out_of_range_raises_error`

### Running Tests

```bash
# Update these commands when determined
# Python: pytest tests/
# Node.js: npm test
# Go: go test ./...
```

---

## Git Workflows

### Commit Messages

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(sensors): add BME280 temperature sensor support

Implement driver for BME280 sensor with I2C communication.
Includes calibration and temperature compensation.

Closes #42
```

```
fix(api): handle null sensor readings gracefully

Add validation to prevent null pointer errors when sensor
returns no data. Returns 503 status with retry-after header.
```

### Commit Best Practices

- **Atomic commits** - one logical change per commit
- **Frequent commits** - commit working increments
- **Meaningful messages** - future you will thank you
- **No secrets** - never commit API keys, passwords, tokens

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project conventions
- [ ] Documentation updated
- [ ] Tests pass locally
- [ ] No security vulnerabilities introduced
```

---

## AI Assistant Guidelines

### When Working on This Project

#### Discovery Phase
1. **Always explore first** - use Task tool with Explore agent for codebase understanding
2. **Read existing code** - understand patterns before adding new code
3. **Check for similar implementations** - avoid duplicating logic
4. **Review recent commits** - understand current development direction

#### Implementation Phase
1. **Use TodoWrite tool** - track multi-step tasks
2. **Prefer editing over creating** - extend existing files when appropriate
3. **Match existing patterns** - maintain consistency
4. **Test as you go** - write tests alongside implementation
5. **Document new features** - update relevant documentation

#### Code Quality
1. **Security scanning** - check for OWASP top 10 vulnerabilities:
   - SQL injection
   - XSS attacks
   - Command injection
   - Insecure deserialization
   - Sensitive data exposure
2. **Input validation** - validate all external inputs
3. **Error handling** - use appropriate error types, log errors
4. **Resource cleanup** - close connections, release resources

#### Sensor-Specific Considerations (Gas Detection)
1. **Data validation** - ALL sensor readings must be validated against thresholds
2. **Gas level units** - Use PPM (parts per million) consistently, validate range (0-10000 typical)
3. **Alert thresholds** - Default: 800 PPM for combustible gas (configurable per sensor)
4. **Critical timing** - Alert processing MUST complete in < 5 seconds end-to-end
5. **Failure modes** - Handle sensor disconnection gracefully:
   - Mark sensor as "disconnected" if no heartbeat for 2 minutes
   - Send alert to administrators if critical sensor goes offline
   - Never suppress alerts due to system errors
6. **Battery monitoring** - Track battery levels, warn at < 20%, critical at < 10%
7. **Signal strength** - Monitor MQTT signal strength to detect connectivity issues
8. **Throttling** - Maximum 1 alert per sensor per 5 minutes (prevent alert fatigue)
9. **MQTT QoS** - Use QoS 1 or 2 for alert messages (guaranteed delivery)
10. **False positive handling** - Log all detections but allow configurable sensitivity

### Common Patterns to Follow

#### MQTT Message Structure
```python
# Standard message format from gas sensors
{
    "sensor_id": "S001",
    "timestamp": "2025-11-17T10:30:45Z",
    "status": "alert",  # normal, alert, warning, offline
    "gas_level": 850,   # PPM
    "threshold": 800,   # PPM
    "battery": 85,      # percentage
    "signal_strength": -45  # dBm
}

# Topic structure: engisensors/{client_id}/{building_id}/{apartment_id}/{sensor_id}/status
```

#### Gas Level Validation Pattern
```python
# Critical: Validate ALL gas readings
def validate_gas_reading(reading: dict) -> bool:
    """Validate gas sensor reading before processing."""
    if not isinstance(reading.get("gas_level"), (int, float)):
        logger.error(f"Invalid gas_level type: {reading}")
        return False

    gas_level = reading["gas_level"]

    # Validate range (0-10000 PPM typical for combustible gas)
    if not 0 <= gas_level <= 10000:
        logger.warning(f"Gas level out of range: {gas_level} PPM")
        return False

    # Check threshold
    threshold = reading.get("threshold", 800)
    if gas_level >= threshold:
        logger.critical(
            f"GAS ALERT: Sensor {reading['sensor_id']} detected {gas_level} PPM"
        )
        # Trigger alert workflow
        trigger_alert(reading)

    return True
```

#### Notification Pattern
```python
# Never fail silently on notifications - this is critical safety system
async def send_gas_alert(sensor_event: SensorEvent):
    """Send multi-channel alert for gas detection."""
    try:
        # Get all active contacts for the client
        contacts = await get_client_contacts(sensor_event.client_id)

        # Prepare alert message
        message = format_alert_message(sensor_event)

        # Send to notification queue (with retries)
        await notification_queue.publish(
            {
                "event_id": sensor_event.id,
                "contacts": contacts,
                "message": message,
                "channels": ["email", "sms"],
                "priority": "critical"
            },
            delivery_mode=2  # persistent
        )

        logger.critical(
            "Gas alert queued",
            extra={
                "sensor_id": sensor_event.sensor_id,
                "gas_level": sensor_event.gas_level,
                "location": sensor_event.location,
                "contacts_count": len(contacts)
            }
        )
    except Exception as e:
        # NEVER suppress notification errors
        logger.exception(f"CRITICAL: Failed to queue gas alert: {e}")
        # Fallback: direct notification or escalate to admins
        await emergency_fallback_notification(sensor_event, e)
```

#### Logging Pattern
```python
# Structured logging with full context for audit trail
logger.critical(
    "Gas detection event",
    extra={
        "event_type": "gas_alert",
        "sensor_id": sensor.id,
        "device_id": sensor.device_id,
        "gas_level": reading.gas_level,
        "threshold": reading.threshold,
        "location": {
            "client": client.name,
            "building": building.name,
            "apartment": apartment.number,
            "room": location.type
        },
        "timestamp": reading.timestamp,
        "notification_sent": True,
        "contacts_notified": len(contacts)
    }
)
```

### What to Avoid

- **Don't commit commented-out code** - use version control
- **Don't use print() for debugging** - use proper logging
- **Don't hardcode values** - use configuration
- **Don't ignore errors** - handle or propagate explicitly
- **Don't mix concerns** - separate data access, business logic, presentation
- **Don't write flaky tests** - tests should be deterministic
- **Don't skip validation** - especially for sensor data and API inputs

### Before Committing - Checklist

- [ ] Code runs without errors
- [ ] Tests pass (unit, integration)
- [ ] No security vulnerabilities introduced
- [ ] Documentation updated
- [ ] Code follows project conventions
- [ ] No debugging code left behind
- [ ] No secrets in commits
- [ ] Commit message follows conventions

---

## Common Tasks

### Registering a New Gas Sensor

1. **Create Client** (if new): POST `/api/clients` with company information
2. **Create Building**: POST `/api/buildings` linked to client
3. **Create Apartment**: POST `/api/apartments` linked to building
4. **Create Location**: POST `/api/locations` (cocina, lavadero, sala, etc.)
5. **Register Sensor**: POST `/api/sensors` with:
   - Unique `device_id`
   - Model and firmware version
   - Link to location
   - Alert threshold (default 800 PPM)
6. **Configure MQTT subscription**: System auto-subscribes to sensor's topic
7. **Test sensor**: Send test MQTT message to verify communication
8. **Verify in dashboard**: Check sensor appears and updates in real-time

### Adding a New API Endpoint

1. Define endpoint in appropriate router (`/routes/sensors.py`, `/routes/clients.py`, etc.)
2. Implement Pydantic models for request/response validation
3. Add authentication decorator (`@require_auth`, `@require_admin`)
4. Implement authorization (users can only access their own data)
5. Add comprehensive error handling with proper HTTP status codes
6. Write API tests (happy path + edge cases + security)
7. Update OpenAPI/Swagger documentation
8. Add example requests to Postman collection

### Debugging Gas Detection Issues

**Sensor Not Sending Data:**
1. Check MQTT broker logs: `docker logs engisensors-mqtt`
2. Verify sensor topic subscription: Check MQTT Handler logs
3. Test with MQTT client: `mosquitto_pub -t "engisensors/..." -m "{}"`
4. Check sensor authentication credentials
5. Verify network connectivity (WiFi signal strength in sensor data)
6. Check battery level (< 10% may cause connection issues)

**Alerts Not Being Sent:**
1. Check notification queue: Verify messages are queued
2. Check Notification Service logs for errors
3. Verify contact information is valid and active
4. Check email/SMS provider API status
5. Review throttling logic (max 1 alert per 5 minutes per sensor)
6. Verify event was logged in `sensor_events` table
7. Check notification records in `notifications` table

**False Positives:**
1. Review gas level trends (check if gradual increase or sudden spike)
2. Adjust sensor threshold if needed
3. Check for sensor calibration issues
4. Verify sensor placement (away from stoves, vents during cooking)
5. Review sensor maintenance history
6. Check for environmental factors (humidity, temperature extremes)

---

## Troubleshooting

### Common Issues

#### MQTT Broker Connection Failures
**Symptoms:** Sensors not sending data, MQTT Handler cannot connect

**Solutions:**
- Verify broker is running: `docker ps | grep mqtt`
- Check broker logs: `docker logs engisensors-mqtt`
- Test connection: `mosquitto_sub -h localhost -p 1883 -t "#" -v`
- Verify authentication credentials
- Check firewall rules (port 1883 or 8883 for TLS)
- Restart broker if needed: `docker restart engisensors-mqtt`

#### Notification Delivery Failures
**Symptoms:** Gas detected but no emails/SMS sent

**Solutions:**
- Check notification queue: Verify messages are being published
- Review Notification Service logs for API errors
- Verify email provider API key is valid (SendGrid, SES)
- Verify SMS provider credentials (Twilio)
- Check contact information format (valid email, phone with country code)
- Test with manual notification: POST `/api/test-notification`
- Review rate limits on email/SMS providers
- Check notification records status: `SELECT * FROM notifications WHERE status='failed'`

#### Database Performance Issues
**Symptoms:** Slow API responses, dashboard lag

**Solutions:**
- Check for missing indexes: Review query execution plans
- Verify TimescaleDB hypertable is created: `SELECT * FROM timescaledb_information.hypertables`
- Implement data retention policy (compress/delete old sensor_events)
- Review connection pool settings
- Check for slow queries: Enable PostgreSQL slow query log
- Optimize N+1 queries: Use JOIN or eager loading
- Add caching layer with Redis for frequent queries

#### Real-time Dashboard Not Updating
**Symptoms:** Dashboard shows stale data, doesn't reflect sensor changes

**Solutions:**
- Check WebSocket connection in browser devtools
- Verify WebSocket Service is running
- Check CORS configuration
- Review WebSocket event publishing in backend
- Test connection: `wscat -c ws://localhost:8000/ws`
- Check client-side error console
- Verify user authentication for WebSocket connection

#### High Memory/CPU Usage
**Symptoms:** Server slowing down, high resource consumption

**Solutions:**
- Profile application: Use cProfile (Python) or built-in profilers
- Check for memory leaks in MQTT Handler (connections not closed)
- Review TimescaleDB chunk management (compress old data)
- Implement rate limiting on APIs
- Scale horizontally: Add more service instances
- Optimize database queries
- Review log verbosity (disable DEBUG in production)
- Check for runaway notification workers

#### Security Vulnerabilities
**Symptoms:** Unauthorized access, suspicious activity

**Solutions:**
- Review authentication logs: `SELECT * FROM audit_logs WHERE action='failed_login'`
- Enable rate limiting on login endpoint
- Rotate JWT secrets if compromised
- Review API authorization logic (users can only access own data)
- Run security scan: `safety check` (Python) or `npm audit`
- Check for SQL injection vulnerabilities in custom queries
- Verify all inputs are validated (Pydantic models)
- Enable HTTPS/TLS in production
- Review MQTT authentication (ensure sensors use strong credentials)

---

## Project Evolution

This CLAUDE.md file should be updated whenever:
- New components are added
- Architecture changes occur
- Development workflows change
- New conventions are established
- Common issues/solutions are discovered
- Technology stack decisions are made

### Update History
- **2025-11-17:** Initial creation - project setup phase
- **2025-11-17:** Updated with gas sensor detection project specifics, MQTT patterns, notification workflows, and troubleshooting guides

---

## Additional Resources

### Documentation
- **Product Requirements Document:** `PRD.md` - Comprehensive product specification
- **Project README:** `README.md` - Quick start and project overview
- **Architecture docs:** `docs/architecture.md` (to be created)
- **API documentation:** Generated via OpenAPI/Swagger at `/docs` endpoint
- **Database Schema:** See PRD.md for complete schema definitions

### External Resources

**MQTT Protocol:**
- [MQTT Specification v3.1.1](https://mqtt.org/mqtt-specification/)
- [MQTT Essentials](https://www.hivemq.com/mqtt-essentials/)
- [Mosquitto Documentation](https://mosquitto.org/documentation/)
- [EMQX Documentation](https://www.emqx.io/docs/)

**Gas Sensor Information:**
- Gas sensor calibration guides (manufacturer-specific)
- Combustible gas safety thresholds and regulations
- OSHA guidelines for gas detection systems

**Framework Documentation:**
- [FastAPI Documentation](https://fastapi.tiangolo.com/) (if using Python)
- [NestJS Documentation](https://nestjs.com/) (if using Node.js)
- [TimescaleDB Documentation](https://docs.timescale.com/)
- [PostgreSQL Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)

**Notification Services:**
- [SendGrid API Documentation](https://docs.sendgrid.com/)
- [Twilio SMS API](https://www.twilio.com/docs/sms)
- [AWS SES Documentation](https://docs.aws.amazon.com/ses/)

**Security:**
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [IoT Security Best Practices](https://owasp.org/www-project-internet-of-things/)

---

## Getting Help

### For AI Assistants
- Read this entire file before starting work
- Use Explore agent to understand codebase
- Check git history for context
- Look for similar implementations
- When in doubt, ask clarifying questions

### For Developers
- Check documentation in `docs/`
- Review existing code for patterns
- Consult sensor datasheets
- Check GitHub issues for similar problems

---

**Remember:** This is a living document. Keep it updated as the project evolves!
