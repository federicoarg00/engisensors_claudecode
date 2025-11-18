"""
EngiSensors FastAPI Application
Main entry point for the API server
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.services.mqtt_handler import mqtt_service
from app.database import check_db_connection

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("🚀 Starting EngiSensors API...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"MQTT Broker: {settings.mqtt_broker_host}:{settings.mqtt_broker_port}")

    # Start MQTT service
    try:
        mqtt_service.start()
        logger.info("✅ MQTT service started successfully")
    except Exception as e:
        logger.error(f"❌ Failed to start MQTT service: {e}")

    yield

    # Shutdown
    logger.info("🛑 Shutting down EngiSensors API...")
    try:
        mqtt_service.stop()
        logger.info("✅ MQTT service stopped")
    except Exception as e:
        logger.error(f"❌ Error stopping MQTT service: {e}")


# Create FastAPI application
app = FastAPI(
    title="EngiSensors API",
    description="IoT Gas Sensor Monitoring Platform - Real-time monitoring and alerting system for combustible gas sensors",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


# Health check endpoints
@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "version": "0.1.0"
    }


@app.get("/health/mqtt", tags=["Health"])
async def mqtt_health_check():
    """MQTT service health check."""
    is_connected = mqtt_service.is_connected()
    return {
        "status": "healthy" if is_connected else "unhealthy",
        "mqtt_broker": settings.mqtt_broker_host,
        "connected": is_connected
    }


@app.get("/health/db", tags=["Health"])
async def db_health_check():
    """Database health check."""
    is_connected = await check_db_connection()
    return {
        "status": "healthy" if is_connected else "unhealthy",
        "database": "PostgreSQL + TimescaleDB",
        "connected": is_connected
    }


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "EngiSensors API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An internal error occurred" if settings.is_production else str(exc)
            }
        }
    )


# Import and include routers
from app.routers import sensors, clients

app.include_router(sensors.router)
app.include_router(clients.router)

# TODO: Add more routers as implemented
# from app.routers import auth, buildings, apartments, locations, contacts, sensor_events
# app.include_router(auth.router)
# app.include_router(buildings.router)
# etc...


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
