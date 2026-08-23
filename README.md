# ResChek

ResChek is an AI-powered resume analysis and tailoring web application that compares a candidate's resume against a job description, identifies strengths and gaps, and generates safer resume improvement suggestions without inventing unsupported experience.

## Live Demo

https://reschek.onrender.com

> ResChek is currently hosted using Render's free tier. The backend may spin down after inactivity, so the first request can take longer while the server wakes up.

## Features

- Upload PDF, DOCX, and TXT resumes
- Automatically extract resume text
- Paste and analyze a target job description
- Generate a 0–100 resume match score
- Identify matched skills
- Identify missing skills and requirements
- Highlight resume strengths and areas for improvement
- Generate targeted recommendations
- Produce resume-tailoring suggestions
- Recommend skills and keywords to emphasize
- Suggest safer bullet-point rewrites
- Avoid adding unsupported skills or experience
- Responsive interface for desktop and mobile

## Tech Stack

### Frontend
- React
- Vite
- JavaScript
- CSS

### Backend
- Python
- FastAPI
- Uvicorn
- Pydantic

### AI
- OpenRouter API for deployed AI inference
- Ollama support for local AI development

### Resume Processing
- PyPDF
- python-docx
- Plain-text parsing

### Deployment
- Render Static Site — frontend
- Render Web Service — backend

## How It Works

1. The user uploads a resume.
2. The FastAPI backend extracts the resume text.
3. The user pastes a target job description.
4. ResChek compares the resume against the job requirements.
5. The application returns a structured match analysis including:
   - Match score
   - Matched skills
   - Missing skills
   - Strengths
   - Gaps
   - Recommendations
6. The Resume Tailor generates targeted improvement suggestions while preserving the factual meaning of the original resume.

## Resume Safety

A major goal of ResChek is to avoid misleading resume suggestions.

The tailoring system is designed to:

- Preserve facts already supported by the resume
- Avoid inventing technologies, projects, responsibilities, or experience
- Keep unsupported requirements categorized as missing skills
- Reject rewrites that introduce stronger or unsupported claims
- Suggest learning opportunities instead of pretending missing experience already exists

## Project Structure

```text
ResChek
├── backend
│   ├── app
│   │   ├── api
│   │   ├── schemas
│   │   ├── services
│   │   └── main.py
│   └── tests
├── frontend
│   ├── src
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   └── index.html
└── README.md