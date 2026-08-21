from typing import List

from pydantic import BaseModel


class BulletRewrite(BaseModel):
    original: str
    suggested: str
    reason: str


class ResumeTailorRequest(BaseModel):
    resume_text: str
    job_description: str


class ResumeTailorResponse(BaseModel):
    summary_suggestion: str
    keywords_to_add: List[str]
    bullet_rewrites: List[BulletRewrite]
    skills_to_emphasize: List[str]
    missing_skills: List[str]
    general_recommendations: List[str]