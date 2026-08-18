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
from typing import Dict, List

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
    # Try to locate a skills line; split by commas.
    skill_line_matches = SKILL_RE.findall(description)
    for line in skill_line_matches:
        items = [s.strip() for s in re.split(r",|and", line) if s.strip()]
        required_skills.extend(items)

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
