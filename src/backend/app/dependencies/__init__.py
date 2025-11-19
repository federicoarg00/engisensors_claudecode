"""
FastAPI Dependencies

Reusable dependencies for route protection and data injection.
"""
from app.dependencies.auth import (
    get_current_user,
    get_current_user_optional,
    get_current_active_admin,
    get_current_active_client,
    require_role,
    oauth2_scheme,
)

__all__ = [
    "get_current_user",
    "get_current_user_optional",
    "get_current_active_admin",
    "get_current_active_client",
    "require_role",
    "oauth2_scheme",
]
