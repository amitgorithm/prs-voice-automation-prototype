# PRS Voice Automation Prototype

A **voice-enabled Patient Reported Symptom (PRS) questionnaire prototype** that demonstrates AI-assisted administration and scoring of clinical scales using natural language responses.

Built as a fast, showcase-ready prototype using Flask, HTML/JS, and OpenAI.

---

## 🧠 Overview

- Voice or text-based PRS responses
- AI maps free-text answers to standardized PRS options
- Automatic scoring with clinical-style rationale
- JSON export of completed sessions
- Works on desktop and mobile browsers

**Note:** This is a prototype for demo and exploration, not a production medical system.

---

## 🏗 Architecture

| Component | Hosting |
|--------|---------|
| Frontend (HTML/JS) | Vercel |
| Backend (Flask API) | Render |
| AI Scoring | OpenAI API |

---

## 🌐 Live URLs

- **Frontend:** https://prs-voice-automation-prototype.vercel.app  
- **Backend:** https://prs-voice-backend.onrender.com  
- **Health Check:** https://prs-voice-backend.onrender.com/health  

---

## 🏃 Run Locally

### 1. Clone repo
```bash
git clone https://github.com/amitgorithm/prs-voice-automation-prototype.git
cd prs-voice-automation-prototype
```

## 2. Setup Environment
python -m venv venv
Activate

Windows: venv\Scripts\Activate.ps1

macOS/Linux: source venv/bin/activate

## 3. Install dependencies
pip install -r requirements.txt

## 4. Set OpenAI Key
# Windows
$env:OPENAI_API_KEY="sk-xxxx"

# macOS/Linux
export OPENAI_API_KEY="sk-xxxx"

## 5. Start Backend
python server.py
Backend runs at:

http://localhost:5003

## 6. Run Frontend
Open index.html in Chrome/Edge/Safari
(or use VS Code Live Server)

🔌 API

POST /api/score
Scores a PRS response using OpenAI.

🔐 Environment Variables
Name	Required
OPENAI_API_KEY	Yes
OPENAI_MODEL	No (default: gpt-4o-mini)

⚠️ Notes

Never commit API keys
Free Render instances may sleep
Browser voice features require Chrome / Edge / Safari
No diagnosis or medical advice is provided

👥 Contributing

Create a branch from main
Open a PR with a clear description
Keep commits small and focused
