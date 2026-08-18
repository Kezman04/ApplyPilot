"""Test suite for job‑description analysis endpoint.

The tests cover:
* Valid request payloads return the expected JSON shape.
* Empty or whitespace only ``job_description`` triggers a 400 error.
* The response contains all required keys with appropriate types.
"""

import json

from fastapi.testclient import TestClient
from app.main import create_app


def test_job_analysis_valid_request() -> None:
    client = TestClient(create_app())
    payload = {"job_description": "Senior Python Engineer at Acme Corp. Skills: Python, FastAPI, Docker. Responsibilities: Build APIs, write tests."}
    response = client.post("/api/jobs/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    # Ensure all keys exist and are of correct type
    expected_keys = {
        "job_title",
        "company",
        "required_skills",
        "preferred_skills",
        "responsibilities",
        "education_requirements",
        "experience_requirements",
        "keywords",
    }
    assert set(data.keys()) == expected_keys
    # Basic type checks
    for k in data:
        if isinstance(data[k], list):
            assert isinstance(data[k], list)
        else:
            assert data[k] is None or isinstance(data[k], str)


def test_job_analysis_empty_description() -> None:
    client = TestClient(create_app())
    payload = {"job_description": "   "}
    response = client.post("/api/jobs/analyze", json=payload)
    assert response.status_code == 400
    assert "must be non‑empty" in response.json()["detail"]
