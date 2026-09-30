# LegalEase — AI-Powered Legal Document Generator

LegalEase is a student-friendly full-stack project based on the supplied project documentation. It uses:

- **Frontend:** Streamlit
- **Backend:** FastAPI + Uvicorn
- **AI:** Google Gemini through the current `google-genai` SDK
- **Exports:** TXT, DOCX, PDF
- **Configuration:** `.env`
- **Testing:** pytest

> Important: LegalEase generates drafts and general legal information. It is not a substitute for advice from a qualified lawyer. Users should review generated documents for the jurisdiction and situation in which they will be used.

## 1. Project structure

```text
LegalEase/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   └── ai_core/
│       ├── __init__.py
│       └── gemini_generator.py
├── frontend/
│   ├── __init__.py
│   ├── app.py
│   └── export_utils.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_exports.py
├── assets/
│   └── README.txt
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── run_backend.bat
├── run_frontend.bat
└── README.md
```

## 2. Requirements

Python 3.10+ is required. Python 3.11 is recommended.

Check:

```powershell
py --version
python --version
```

## 3. Create the virtual environment on Windows

Open VS Code in the `LegalEase` folder.

```powershell
py -3.11 -m venv .venv
```

If `py -3.11` is unavailable, install Python 3.11 first and reopen VS Code.

Activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the commands with the venv's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Or, for the current PowerShell user, you can allow local scripts:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again.

## 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Create the Gemini API key

1. Open Google AI Studio.
2. Sign in with your Google account.
3. Create an API key.
4. Copy the key.
5. In the project root, copy `.env.example` to `.env`.
6. Put the key after `GEMINI_API_KEY=`.

Example:

```env
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-3.8-flash
BACKEND_URL=http://127.0.0.1:8000
```

Never commit `.env` or publish your API key.

## 6. Start the backend

Terminal 1:

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Test:

```text
http://127.0.0.1:8000/
```

You should see a JSON health response.

API documentation:

```text
http://127.0.0.1:8000/docs
```

## 7. Start the frontend

Open a second VS Code terminal:

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run frontend/app.py
```

The browser should open the Streamlit application.

If it does not, open:

```text
http://localhost:8501
```

## 8. Generate a document

Example:

- Document type: `Freelance Work Contract`
- Parties: `Jane Doe (Service Provider), TechNova Inc. (Client)`
- Terms:
  `Payment within 30 days; Provider delivers work by agreed deadline; Confidentiality must be maintained; Either party may terminate with 15 days notice`
- Effective date: `April 15, 2026`

Click **Generate Document**.

The result can be edited in the text area and downloaded as:

- `.txt`
- `.docx`
- `.pdf`

## 9. Run tests

With the virtual environment active:

```powershell
pytest -q
```

The API tests mock the Gemini service, so they do not require a paid/live Gemini call.

## 10. Optional logo

Place a PNG/JPG logo in:

```text
assets/logo.png
```

The Streamlit app also lets the user upload a logo for the current session. The uploaded logo is embedded into DOCX/PDF exports.

## 11. API example

POST `/generate`

```json
{
  "document_type": "Non-Disclosure Agreement",
  "parties": "Alice Smith (Disclosing Party), ABC Technologies (Receiving Party)",
  "terms": "Confidential information must not be disclosed; Exceptions include information already public; Agreement may be terminated with written notice",
  "effective_date": "April 15, 2026"
}
```

Response:

```json
{
  "document_type": "Non-Disclosure Agreement",
  "content": "..."
}
```

## 12. Docker

Build and start:

```powershell
docker compose up --build
```

The backend is available on port 8000 and Streamlit on port 8501.

## 13. Troubleshooting

### `No runtime installed that matches 3.11`

Run:

```powershell
py --version
py --list
```

Install Python 3.11 if it is not listed. Then:

```powershell
py -3.11 -m venv .venv
```

### `.venv\Scripts\Activate.ps1` not found

Make sure the terminal is inside the project folder:

```powershell
cd C:\Users\acer\Desktop\LegalEase
```

Then:

```powershell
py -3.11 -m venv .venv
```

After that:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Gemini key error

Confirm `.env` exists in the project root and contains:

```env
GEMINI_API_KEY=...
```

Restart the backend after changing `.env`.

### Frontend cannot connect to backend

Make sure Terminal 1 is running:

```powershell
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Then confirm:

```text
http://127.0.0.1:8000/
```

If you use another backend port, update `BACKEND_URL` in `.env`.

## 14. Notes about the supplied documentation

The supplied document originally describes `google-generativeai` and Gemini 1.5 Pro. This implementation uses Google's newer `google-genai` SDK and a configurable current model instead. The model can be changed in `.env` without changing application code.

The application keeps the documented four-input workflow and export features while adding practical validation, safe environment handling, automated tests, and cleaner separation between frontend, backend, AI, and export code.
