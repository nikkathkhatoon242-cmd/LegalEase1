# LegalEase Agent Guide

## Project overview

LegalEase is a Python app for generating legal documents with:

- Backend: FastAPI in `backend/`
- Frontend: Streamlit in `frontend/`
- AI generation: Google Gemini via `backend/ai_core/gemini_generator.py`
- Exports: `.txt`, `.docx`, and `.pdf`
- Tests: `pytest` under `tests/`

## Operating conventions

- Use Python 3.10+; Python 3.11 is the preferred local version.
- Prefer the project virtual environment at `.venv` or `.venv-1` when running commands locally.
- Keep `.env` local and never commit secrets or API keys.
- Avoid touching generated or compiled files unless explicitly required.

## Directory responsibilities

- `backend/main.py`: FastAPI app entry point
- `backend/routes.py`: API endpoints and request handling
- `backend/schemas.py`: request/response models
- `backend/ai_core/gemini_generator.py`: Gemini prompt and generation logic
- `frontend/app.py`: Streamlit UI
- `frontend/export_utils.py`: document export helpers
- `tests/`: API and export verification tests

## Common commands

Run the backend:

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Run the frontend:

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run frontend/app.py
```

Run tests:

```powershell
pytest -q
```

## Coding guidance

- Preserve the existing FastAPI and Streamlit separation.
- Keep AI generation logic in the backend rather than the frontend.
- When adding features, make sure both backend validation and frontend flow remain consistent.
- Prefer small, focused changes that match the current project structure.
- For document generation, maintain the contract fields used by the app: document type, parties, terms, and effective date.
- Log or surface meaningful errors without exposing sensitive configuration.

## Before finishing work

- Check any relevant tests in `tests/`.
- Verify the changed behavior with the smallest useful command.
- Do not claim success without fresh verification output.
