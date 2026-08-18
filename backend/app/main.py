"""FastAPI application entry point for ApplyPilot backend.

This module sets up the FastAPI app, includes API routers and provides a simple
health check endpoint. No business logic is implemented yet – only the minimal
structure required to start the server and run tests.
"""

from fastapi import FastAPI
from .api.health import router as health_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns
    -------
    FastAPI
        The configured FastAPI app instance.
    """
    app = FastAPI(title="ApplyPilot Backend")
    # Register API routers
    app.include_router(health_router, prefix="", tags=["Health"])
    return app


# Expose the app for Uvicorn or other ASGI servers.
app = create_app()

