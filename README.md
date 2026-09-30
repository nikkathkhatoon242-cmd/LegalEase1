# ⚖️ LegalEase – AI-Powered Legal Assistant

LegalEase is an **AI-powered legal assistance platform** designed to help users understand legal information, generate legal documents, and access basic legal guidance through a simple and user-friendly interface.

## 🚀 Project Overview

LegalEase combines **Artificial Intelligence, Generative AI, and Web Technologies** to make basic legal assistance easier and more accessible.

The system allows users to enter their legal requirements and receive AI-generated responses or documents based on the provided information.

> **Note:** LegalEase is an educational/student project and does not replace professional legal advice from a qualified lawyer.

---

## ✨ Features

* 🤖 AI-powered legal assistance
* 📝 Legal document generation
* 📄 User-friendly document output
* 💬 Legal query assistance
* 🔐 Secure API-based architecture
* 🌐 Web-based interface
* ⚡ Fast backend API using FastAPI
* 🧠 Generative AI integration
* 📱 Responsive user interface

---

## 🛠️ Technologies Used

### Frontend

* HTML
* CSS
* JavaScript
* React.js

### Backend

* Python
* FastAPI
* Uvicorn

### AI

* Google Gemini API
* Generative AI

### Development Tools

* Visual Studio Code
* Git
* GitHub
* Python Virtual Environment

---

## 📂 Project Structure

```text
LegalEase/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── models.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── gemini_service.py
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/LegalEase.git
```

### 2. Open the Project

```bash
cd LegalEase
```

---

# 🐍 Backend Setup

### 3. Create a Virtual Environment

```powershell
python -m venv .venv
```

### 4. Activate Virtual Environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install Backend Dependencies

```powershell
pip install -r backend\requirements.txt
```

---

## 🔑 Gemini API Key

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_api_key_here
```

**Do not upload your real API key to GitHub.**

The `.gitignore` file should contain:

```gitignore
.env
.venv/
__pycache__/
node_modules/
```

---

# ▶️ Run Backend

From the project root:

```powershell
uvicorn backend.main:app --reload --port 8000
```

The backend will run at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 💻 Frontend Setup

Open another VS Code terminal.

Go to the frontend folder:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start the frontend:

```powershell
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

# 🔄 Application Flow

```text
User
  │
  ▼
LegalEase Frontend
  │
  ▼
FastAPI Backend
  │
  ▼
Gemini Generative AI
  │
  ▼
AI Generated Response
  │
  ▼
LegalEase Frontend
  │
  ▼
User
```

---

# 📸 Main Functionalities

### 1. Legal Query

Users can enter a legal-related question and receive an AI-generated explanation.

### 2. Document Generation

Users can provide required information and generate a structured legal document.

### 3. AI Assistance

The Gemini API processes the user's request and generates a response.

### 4. Document Output

The generated content can be viewed and prepared for further use.

---

# 🧪 Testing

Start the backend:

```powershell
uvicorn backend.main:app --reload --port 8000
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

Test the available API endpoints using Swagger UI.

For frontend testing:

```powershell
cd frontend
npm run dev
```

Then open the displayed localhost URL in your browser.

---

# 🔒 Security

LegalEase follows basic security practices:

* API keys are stored in `.env`
* `.env` is excluded from Git
* Sensitive credentials should never be committed
* User input should be validated before processing
* API access should be configured securely for production

---

# 👥 Team – Group 7

| No. | Team Member     | Role        |
| --- | --------------- | ----------- |
| 1   | Nikkath Khatoon | Team Leader |
| 2   | Arfana Begum K  | Team Member |
| 3   | Snehan          | Team Member |
| 4   | Joel            | Team Member |
| 5   | Nowfel          | Team Member |

---

# 🎓 Project Purpose

LegalEase was developed as a **student project** to demonstrate how Generative AI can be integrated with modern web technologies to create an accessible legal-assistance application.

The project demonstrates:

* Artificial Intelligence
* Generative AI
* API Integration
* Web Development
* Backend Development
* Frontend Development
* Document Generation

---

# ⚠️ Disclaimer

LegalEase provides AI-generated information for **educational and informational purposes only**.

The generated content should not be considered professional legal advice. Users should consult a qualified legal professional for advice regarding specific legal matters.

---

# 🔮 Future Enhancements

* 🌍 Multi-language legal assistance
* 📄 PDF document generation
* 🔐 User authentication
* 💾 User document history
* 🎙️ Voice-based legal queries
* 📱 Mobile application
* ⚖️ Improved legal document templates
* 🗃️ Legal information database
* 👨‍⚖️ Lawyer consultation integration

---

# 📜 License

This project is developed for educational purposes.

You may modify and improve the project according to your requirements.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

**LegalEase – Making Legal Assistance Smarter with AI.**
