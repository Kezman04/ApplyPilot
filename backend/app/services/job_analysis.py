"""Business logic for parsing a raw job description.

The parser is intentionally simple and deterministic. It uses keyword matching
and rudimentary regexes to extract structured information from the supplied text.
It does **not** rely on external APIs or language models; it only operates on
the plaintext provided by the client.  The goal of this placeholder implementation
is to provide a predictable, testable baseline that can later be swapped out for an LLM
backed parser without changing the API contract.

The function returns a plain ``dict`` matching the fields defined in
``JobAnalysisResponse`` so that the router can validate it with Pydantic.
"""

from __future__ import annotations

import re
import json
from typing import Dict, List
from unittest import result

from app.services.ollama_client import ask_ollama

# Regular expressions used for simple parsing. These are deliberately very
# lightweight and not designed to handle every possible job description.
TITLE_RE = re.compile(r"(?i)^\s*(?P<title>.*) at (?P<company>[A-Za-z0-9 &.-]+)", re.MULTILINE)
SKILL_RE = re.compile(r"(?i)(?:skills?|technologies?)\b.*:\s*([\w, ]+)", re.IGNORECASE)
RESP_RE = re.compile(r"(?i)^\s*-\s*(?P<item>.+)$", re.MULTILINE)
EDU_RE = re.compile(r"(?i)education|degree|bachelor|master|phd", re.IGNORECASE)
EXPERIENCE_RE = re.compile(r"(?i)(?:experience|yrs?|years)\s*[:\-]\s*(?P<item>.+?)$", re.MULTILINE | re.DOTALL)

def _extract_section(text: str, pattern: re.Pattern[str]) -> List[str]:
    """Return a list of captured groups from ``pattern`` applied to ``text``."""
    return [m.group(1).strip() for m in pattern.finditer(text) if m.group(1)]


def analyze_job_description(description: str) -> Dict[str, List[str] | None]:
    """Parse a raw job description into structured fields.

    Parameters
    ----------
    description:
        Raw text of the job posting.

    Returns
    -------
    dict
        Mapping matching ``JobAnalysisResponse`` keys. String values may be ``None``;
        list values default to empty lists.
    """

    title_match = TITLE_RE.search(description)
    job_title = title_match.group("title").strip() if title_match else None
    company = title_match.group("company").strip() if title_match else None

    required_skills: List[str] = []
    preferred_skills: List[str] = []

    # Common technical skills ApplyPilot should recognize in natural-language postings.
    KNOWN_SKILLS = [
        "Python",
        "Java",
        "JavaScript",
        "C",
        "C++",
        "C#",
        "Git",
        "SQL",
        "HTML",
        "CSS",
        "React",
        "Node.js",
        "REST APIs",
        "Docker",
        "Linux",
        "AWS",
        "Azure",
        "MATLAB",
        "Object-Oriented Programming",
    ]

    description_lower = description.lower()

    for skill in KNOWN_SKILLS:
        skill_lower = skill.lower()

        if re.search(rf"(?<!\w){re.escape(skill_lower)}(?!\w)", description_lower):
            required_skills.append(skill)
    # Handle common abbreviation for object-oriented programming.
    if (
        "oop" in description_lower
        or "object oriented programming" in description_lower
        or "object-oriented programming" in description_lower
    ):
        if "Object-Oriented Programming" not in required_skills:
            required_skills.append("Object-Oriented Programming")

    # Responsibilities: look for bullet points after a heading like "Responsibilities"
    responsibilities: List[str] = []
    resp_sections = RESP_RE.findall(description)
    responsibilities.extend(resp_sections)

    education_requirements = _extract_section(description, EDU_RE)
    experience_requirements = _extract_section(description, EXPERIENCE_RE)

    # Generic keywords: take the first 10 words after removing common stopwords.
    stopwords = {"the", "and", "or", "for", "with", "to", "of", "in", "at"}
    words = [w.lower() for w in re.findall(r"\b[\w']+\b", description) if w.lower() not in stopwords]
    keywords: List[str] = list(dict.fromkeys(words[:10]))

    return {
        "job_title": job_title,
        "company": company,
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "responsibilities": responsibilities,
        "education_requirements": education_requirements,
        "experience_requirements": experience_requirements,
        "keywords": keywords,
    }

def analyze_job_description_ai(description: str) -> Dict[str, List[str] | str | None]:
    prompt = f"""
You are analyzing a job posting for a job application assistant.
RECOMMENDATION SAFETY RULES:

- Never recommend that the candidate add a missing skill, technology, tool, or experience to the resume unless the resume already supports it.

- If a skill is listed under "missing_skills", recommendations must NOT say:
  "add X to your resume",
  "mention X",
  "highlight X",
  "include experience with X",
  or anything that implies the candidate already has X.

- For genuinely missing skills, recommendations should instead use wording such as:
  "Consider gaining experience with X."
  "Consider learning X."
  "If you have undocumented experience with X, consider adding it to your resume."

- Never encourage fabrication or unsupported claims.

- Recommendations must distinguish between:
  1. existing experience that could be emphasized, and
  2. missing experience that should be learned or gained.

Return ONLY valid JSON with exactly these keys:

{{
  "job_title": null,
  "company": null,
  "required_skills": [],
  "preferred_skills": [],
  "responsibilities": [],
  "education_requirements": [],
  "experience_requirements": [],
  "keywords": []
}}

Rules:
- Use null if the job title or company is not provided.
- Use arrays of strings for every other field.
- Do not invent information.
- Keep entries short and specific.
- Put programming languages, tools, frameworks, APIs, and technical abilities in required_skills when they are required.
- Put optional, bonus, preferred, or nice-to-have skills in preferred_skills.
- Put actual work duties in responsibilities.
- Put degree, diploma, major, or education requirements in education_requirements.
- Put only true experience-level requirements in experience_requirements, such as "2 years of experience", "previous internship experience", or "entry level".
- Do NOT put phrases like "experience in Python", "experience with Git", or "experience with REST APIs" in experience_requirements. Those belong in required_skills.
- Avoid duplicating the same information across multiple fields.
- Keywords should contain concise important terms from the posting, not full sentences.
Job posting:
{description}
"""
    raw_response = ask_ollama(prompt)
    result = json.loads(raw_response)

    # Remove skill-like phrases that the model incorrectly places in experience requirements.
    result["experience_requirements"] = [
        item
        for item in result.get("experience_requirements", [])
        if not item.lower().startswith(("experience in ", "experience with "))
    ]

    # Safety check: never tell the user to claim a skill that is missing.
    missing_skills = result.get("missing_skills", [])
    recommendations = result.get("recommendations", [])

    safe_recommendations = []

    for recommendation in recommendations:
        replacement = recommendation

        for skill in missing_skills:
            if skill.lower() in recommendation.lower():
                replacement = f"Consider gaining experience with {skill}."
                break

        safe_recommendations.append(replacement)

    result["recommendations"] = safe_recommendations

    return result