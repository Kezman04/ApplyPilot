"""API router for job‑description analysis.

This module provides a single ``POST /api/jobs/analyze`` endpoint that accepts a raw
job description string and returns a structured representation. The logic is kept in the
service layer (see :pymod:`services.job_analysis`).  No external LLMs are used – the
parser is deterministic and based on simple keyword extraction.

The response follows the :class:`schemas.JobAnalysisResponse` Pydantic model which
enforces type safety and guarantees that all expected keys are present.  Unknown or
missing values are represented with ``None`` for string fields and empty lists for
array fields, per the specifications.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError

from ..schemas.job_schema import JobAnalysisRequest, JobAnalysisResponse
from ..services.job_analysis import analyze_job_description

router = APIRouter()


@router.post(
    "/api/jobs/analyze",
    status_code=status.HTTP_200_OK,
    response_model=JobAnalysisResponse,
)
def job_analyze(request: JobAnalysisRequest) -> JobAnalysisResponse:
    """Analyze a raw job description.

    Parameters
    ----------
    request: JobAnalysisRequest
        The incoming payload containing ``job_description``.

    Returns
    -------
    JobAnalysisResponse
        Structured representation of the job posting.
    """

    # Validation handled by Pydantic; ensure non‑empty description
    if not request.job_description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="job_description must be non‑empty",
        )

    result = analyze_job_description(request.job_description)
    try:
        response = JobAnalysisResponse(**result)
    except ValidationError as exc:  # pragma: no cover - defensive
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Invalid analysis result: {exc}",
        ) from exc

    return response
