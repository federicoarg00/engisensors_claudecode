"""
EngiSensors Configuration Management
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import validator, Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Application
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"
    secret_key: str
    api_v1_prefix: str = "/api/v1"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Database
    database_url: str
    database_pool_size: int = 10
    database_max_overflow: int = 20

    # Redis
    redis_url: str
    redis_max_connections: int = 10

    # MQTT Broker
    mqtt_broker_host: str = "www.trustcapsupes.com"
    mqtt_broker_port: int = 1883
    mqtt_broker_username: str = ""
    mqtt_broker_password: str = ""
    mqtt_client_id: str = "engisensors-backend"
    mqtt_keepalive: int = 60
    mqtt_qos: int = 1
    mqtt_base_topic: str = "engisensors/#"

    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60
    jwt_refresh_token_expire_days: int = 7

    # Email Notifications
    sendgrid_api_key: str = ""
    sendgrid_from_email: str = "noreply@engisensors.com"
    sendgrid_from_name: str = "EngiSensors Alert System"

    # SMS Notifications
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""

    # Alert Configuration
    alert_throttle_seconds: int = 300  # 5 minutes
    default_gas_threshold_ppm: int = 800
    max_contacts_per_client: int = 10

    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]

    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment.lower() == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment.lower() == "development"


# Global settings instance
settings = Settings()
