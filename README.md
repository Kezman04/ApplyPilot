# ApplyPilot

ApplyPilot is a local AI-powered resume analysis and tailoring tool that compares a candidate's resume against a job description, identifies strengths and gaps, and generates safer resume improvement suggestions without inventing unsupported experience.

## Features

- Upload and extract text from PDF, DOCX, and TXT resumes
- Compare a resume against a job description
- Generate an overall match score
- Identify matched skills and missing skills
- Highlight strengths and gaps
- Generate safe recommendations for missing experience
- Tailor resume summaries and bullet points
- Reject unsupported or exaggerated rewrite suggestions
- Copy improved bullet suggestions directly from the interface
- Run AI processing locally using Ollama

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

### AI
- Ollama
- Local language model inference

## How It Works

1. The user uploads a resume.
2. ApplyPilot extracts the resume text.
3. The user pastes a target job description.
4. The backend sends structured prompts to a local Ollama model.
5. ApplyPilot returns:
   - match score
   - matched skills
   - missing skills
   - strengths
   - gaps
   - recommendations
6. The resume tailoring feature generates improved wording while applying safeguards against unsupported claims.

## Safety-Focused Resume Tailoring

ApplyPilot is designed to improve wording without fabricating experience.

The tailoring pipeline checks generated suggestions and rejects rewrites that introduce unsupported technologies, skills, responsibilities, or stronger claims than the original resume supports.

For genuinely missing skills, the application recommends gaining experience rather than falsely adding them to the resume.

## Project Structure

```text
ApplyPilot/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   └── tests/
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   └── package.json
│
└── README.md