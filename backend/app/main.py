"""FastAPI application entry point for ResCheck backend.

This module sets up the FastAPI app, includes API routers and provides a simple
health check endpoint. No business logic is implemented yet – only the minimal
structure required to start the server and run tests.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.health import router as health_router
from .api.jobs import router as jobs_router
from .api.resume import router as resume_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns
    -------
    FastAPI
        The configured FastAPI app instance.
    """
    app = FastAPI(title="ResCheck Backend")
    app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "https://reschek.onrender.com",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    # Register API routers
    app.include_router(health_router, prefix="", tags=["Health"])
    # Job analysis API – thin wrapper delegating to service layer
    app.include_router(jobs_router, prefix="", tags=["Jobs"])
    # Resume matching API – thin wrapper delegating to service layer
    app.include_router(resume_router, prefix="", tags=["Resume"])
    return app


# Expose the app for Uvicorn or other ASGI servers.
app = create_app()
