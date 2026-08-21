from pydantic import BaseModel, Field
from typing import List


class ResumeMatchRequest(BaseModel):
    resume_text: str = Field(..., min_length=1)
    job_description: str = Field(..., min_length=1)


class ResumeMatchResponse(BaseModel):
    match_score: int
    matched_skills: List[str]
    missing_skills: List[str]
    strengths: List[str]
    gaps: List[str]
    recommendations: List[str]