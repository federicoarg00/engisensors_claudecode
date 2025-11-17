# EngiSensors Scripts

Utility scripts for database management and administration.

## Database Initialization

### 1. Initialize Database

Creates all tables and sets up TimescaleDB hypertable:

```bash
# From project root
cd src/backend
python ../../scripts/init_db.py
```

This script:
- ✅ Enables TimescaleDB extension
- ✅ Creates all database tables
- ✅ Converts `sensor_events` to TimescaleDB hypertable
- ✅ Sets up compression policy (compress after 7 days)
- ✅ Sets up retention policy (delete after 2 years)
- ✅ Creates performance indexes

### 2. Create Admin User

Creates an initial admin user for system access:

```bash
cd src/backend
python ../../scripts/create_admin.py
```

Follow the prompts to enter:
- Admin email
- Password (minimum 8 characters)
- Password confirmation

## Using with Docker

If running in Docker, execute scripts inside the container:

```bash
# Initialize database
docker-compose exec backend python ../../scripts/init_db.py

# Create admin user
docker-compose exec backend python ../../scripts/create_admin.py
```

## Alembic Migrations (Alternative)

Instead of using `init_db.py`, you can use Alembic for migrations:

```bash
cd src/backend

# Create initial migration
alembic revision --autogenerate -m "initial schema"

# Apply migrations
alembic upgrade head

# Then manually run TimescaleDB setup
python ../../scripts/init_db.py  # (will skip table creation)
```

## Troubleshooting

### TimescaleDB Extension Not Available

**Error:** `extension "timescaledb" is not available`

**Solution:** Make sure you're using the TimescaleDB Docker image:
```yaml
# In docker-compose.yml
postgres:
  image: timescale/timescaledb:latest-pg15
```

### Permission Denied

**Error:** `permission denied to create extension`

**Solution:** Connect as superuser or grant permissions:
```sql
ALTER USER engisensors WITH SUPERUSER;
```

### Database Connection Failed

**Error:** `could not connect to server`

**Solution:** Check that PostgreSQL is running and DATABASE_URL is correct:
```bash
docker-compose ps postgres
echo $DATABASE_URL
```

## Available Scripts

- `init_db.py` - Initialize database with all tables and TimescaleDB setup
- `create_admin.py` - Create an admin user interactively
- More scripts will be added as needed

## Notes

- Always backup your database before running migration scripts in production
- The `init_db.py` script is idempotent - safe to run multiple times
- Retention policy keeps 2 years of data (configurable)
- Compression policy compresses data older than 7 days (configurable)
