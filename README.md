# ApplyPilot

ApplyPilot is an AI-powered resume analysis and tailoring application that compares a candidate's resume against a job description, identifies strengths and gaps, and generates safer resume improvement suggestions without inventing unsupported experience.

## Live Demo

https://applypilot-wca4.onrender.com

> The backend is hosted on Render's free tier, so the first request after a period of inactivity may take longer while the service wakes up.

## Features

- Upload PDF, DOCX, and TXT resumes
- Automatically extract resume text
- Compare a resume against a target job description
- Generate a 0–100 resume match score
- Identify matched skills and missing requirements
- Highlight resume strengths and areas for improvement
- Generate dynamic recommendations based on the specific job posting
- Generate a tailored professional summary
- Identify existing skills that should be emphasized
- Suggest relevant keywords already supported by the resume
- Rewrite resume bullet points for clarity and impact
- Reject AI-generated rewrites that introduce unsupported or exaggerated claims
- Clearly indicate when the original resume bullet should be kept
- Copy suggested bullet rewrites directly from the interface
- Support both local and cloud AI inference

## Tech Stack

### Frontend

- React
- Vite
- JavaScript
- CSS

### Backend

- Python
- FastAPI
- Pydantic
- python-docx
- pypdf

### AI

- OpenRouter for the deployed application
- Ollama for local AI development
- Structured prompting for resume analysis and tailoring

### Deployment

- Render Static Site — frontend
- Render Web Service — FastAPI backend
- OpenRouter — hosted AI inference

## How It Works

1. The user uploads a resume.
2. ApplyPilot extracts the resume text.
3. The user pastes a target job description.
4. The backend compares the resume against the job requirements.
5. ApplyPilot returns:
   - overall match score
   - matched skills
   - missing requirements
   - strengths
   - areas to improve
   - actionable recommendations
6. The user can run Resume Tailoring.
7. ApplyPilot generates:
   - a suggested professional summary
   - skills to emphasize
   - relevant keywords
   - bullet-point rewrites
   - general resume recommendations
8. Generated bullet rewrites are checked before being presented to the user.

## Safety-Focused Resume Tailoring

ApplyPilot is designed to improve how existing experience is communicated without fabricating experience.

The tailoring pipeline checks generated suggestions and rejects rewrites that introduce unsupported technologies, responsibilities, experience, or stronger claims than the original resume supports.

When a generated rewrite is rejected, ApplyPilot clearly recommends keeping the original bullet instead.

Missing qualifications are treated as development opportunities rather than being falsely added to the resume.

## Match Scoring

ApplyPilot evaluates the degree of alignment between the supplied resume and job description and returns a whole-number score from 0–100.

The scoring prompt does not restrict results to multiples of 5 or 10, allowing scores such as 63, 71, 84, or 92 when justified by the actual resume-to-job alignment.

## Local vs. Production AI

ApplyPilot supports two AI configurations:

### Local Development

```text
AI_PROVIDER=ollama