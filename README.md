# README for ApplyPilot root project

## Overview
ApplyPilot is a local‑first AI job‑application assistant. This repo contains two
primary components:

* **Backend** – FastAPI service providing health checks and a foundation for
  future business logic.
* **Frontend** – React + Vite starter that will host the user interface.

Both parts are intentionally minimal at this stage to serve as a solid
foundation for subsequent phases.

## Project Structure (Phase 2 – Backend API routes added)
```
ApplyPilot/
├─ backend/        # FastAPI application
│  ├─ app/
│  │  ├─ api/
│  │  │  ├─ health.py
│  │  │  └─ jobs.py
│  │  └─ main.py
│  ├─ tests/
│  │  ├─ conftest.py
│  │  └─ test_health.py
│  ├─ .env.example
│  └─ pyproject.toml
├─ frontend/       # React + Vite app
│  ├─ src/
│  │  └─ App.jsx
│  ├─ vite.config.js
│  ├─ package.json
│  └─ .env.example
└─ README.md
```

## Getting Started

### Backend
```bash
cd backend
pip install -e .[dev]   # or pip install -r requirements.txt if you prefer
uvicorn app.main:app --reload
```
The service will be available at `http://localhost:8000`. The health endpoint is
`GET /health`.

### Frontend
```bash
cd frontend
npm install
npm run dev   # starts the Vite dev server on http://localhost:5173
```

## Testing
Backend tests are written with Pytest and can be executed from the `backend`
directory:
```bash
pytest
```
Frontend build verification is handled via the Vite build script.

## Contributing
Feel free to open issues or pull requests. This repository follows standard
Python/Node conventions and aims to keep the codebase lightweight.
```
---
Author: ApplyPilot Core Team
Date: 2026-08-17
