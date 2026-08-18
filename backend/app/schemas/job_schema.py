"""Pydantic schemas for job‑description analysis.

Two models are defined:

``JobAnalysisRequest``
    Incoming payload with a single field ``job_description``. Pydantic validates the type and
    ensures it is a string.

``JobAnalysisResponse``
    Structured response containing optional fields that may be omitted or empty when not found in the
    job description. All non‑string list fields default to empty lists, string fields default to
    ``None``.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

__all__ = [
    "JobAnalysisRequest",
    "JobAnalysisResponse",
]


class JobAnalysisRequest(BaseModel):
    job_description: str = Field(..., description="Raw job posting text")


class JobAnalysisResponse(BaseModel):
    job_title: Optional[str] = None
    company: Optional[str] = None
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    responsibilities: List[str] = []
    education_requirements: List[str] = []
    experience_requirements: List[str] = []
    keywords: List[str] = []
