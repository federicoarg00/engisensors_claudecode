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
EngiSensors is a project focused on engineering sensor integration, data processing, and analysis.

### Technology Stack
*To be determined as project develops. Update this section with:*
- **Backend:** (e.g., Python, Node.js, Go)
- **Frontend:** (e.g., React, Vue, Angular)
- **Database:** (e.g., PostgreSQL, MongoDB, TimescaleDB)
- **IoT/Hardware:** (e.g., MQTT, CoAP, sensor protocols)
- **Infrastructure:** (e.g., Docker, Kubernetes, cloud platforms)

### Key Components
*Update as components are developed:*
- Data acquisition layer
- Sensor management
- Data processing pipeline
- Analytics engine
- API layer
- Frontend dashboard
- Configuration management

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

#### Sensor-Specific Considerations
1. **Data validation** - sensor readings must be validated
2. **Error margins** - account for sensor accuracy limits
3. **Calibration** - support sensor calibration workflows
4. **Failure modes** - handle sensor disconnection gracefully
5. **Units** - always specify and convert units explicitly
6. **Sampling rates** - respect sensor timing constraints

### Common Patterns to Follow

#### Configuration Management
```python
# Store configurations in version control
# Secrets in environment variables or secret management
config = {
    "sensor_type": "BME280",
    "i2c_address": "0x76",
    "sampling_rate": 1.0,  # Hz
}
```

#### Error Handling Pattern
```python
# Fail fast, provide context
try:
    reading = sensor.read()
    if not validate_reading(reading):
        raise SensorValidationError(
            f"Invalid reading from {sensor.id}: {reading}"
        )
except I2CError as e:
    logger.error(f"I2C communication failed: {e}")
    raise SensorCommunicationError(f"Failed to read {sensor.id}") from e
```

#### Logging Pattern
```python
# Structured logging with context
logger.info(
    "Sensor reading acquired",
    extra={
        "sensor_id": sensor.id,
        "reading": reading.value,
        "unit": reading.unit,
        "timestamp": reading.timestamp,
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

### Adding a New Sensor

1. Create sensor driver in `src/sensors/<sensor_name>/`
2. Implement standard sensor interface
3. Add configuration schema
4. Write unit tests
5. Write integration tests
6. Document sensor specifications
7. Update sensor registry
8. Add example usage

### Adding a New API Endpoint

1. Define endpoint in appropriate router
2. Implement request/response validation
3. Add authentication/authorization if needed
4. Implement business logic
5. Add error handling
6. Write API tests
7. Update API documentation
8. Add example requests

### Debugging Sensor Issues

1. Check sensor physical connections
2. Verify I2C/SPI/UART configuration
3. Check sensor address/ID
4. Verify power supply voltage
5. Review sensor datasheet timing requirements
6. Check logs for communication errors
7. Test with minimal example code
8. Verify calibration data

---

## Troubleshooting

### Common Issues

#### Sensor Not Detected
- Check physical connections (power, ground, data lines)
- Verify I2C address with `i2cdetect -y 1`
- Check pull-up resistors on I2C lines
- Verify sensor power supply voltage

#### Inconsistent Readings
- Check sensor calibration
- Verify sampling rate isn't too high
- Check for electromagnetic interference
- Ensure adequate power supply
- Review sensor warm-up time requirements

#### Build/Test Failures
- Clear cache/build artifacts
- Reinstall dependencies
- Check environment variables
- Review recent changes
- Check for version conflicts

#### Performance Issues
- Profile code to find bottlenecks
- Check database query efficiency
- Review caching strategy
- Monitor memory usage
- Check for N+1 queries

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

---

## Additional Resources

### Documentation
- Project README: `README.md`
- Architecture docs: `docs/architecture.md`
- API documentation: `docs/api/`
- Sensor specs: `docs/sensors/`

### External Resources
*Add relevant links as project develops:*
- Sensor datasheets
- Protocol specifications
- Framework documentation
- Cloud platform guides

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
