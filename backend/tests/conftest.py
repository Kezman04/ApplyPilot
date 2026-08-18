"""Pytest fixtures for backend tests."""

import pytest
from fastapi.testclient import TestClient
from app.main import create_app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Return a shared TestClient for the FastAPI app."""
    return TestClient(create_app())
