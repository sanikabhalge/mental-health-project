# MindCare Backend

FastAPI backend with JWT auth, SQLite, Groq LLM chat, and ADB emergency alerts.

## Quick Start

```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows
# source venv/bin/activate    # Mac/Linux
pip install -r requirements.txt
```

Create `.env` with `SECRET_KEY`, `DATABASE_URL`, `GROQ_API_KEY`, `ADB_PATH` (see root [README](../README.md)).

```bash
uvicorn main:app --reload --port 8000
```

- API: http://localhost:8000  
- Docs: http://localhost:8000/docs  

## Documentation

- **[Setup & Config](../README.md)** – Full setup, env vars, troubleshooting
- **[Components](../docs/COMPONENTS.md)** – File-by-file breakdown, ADB usage
- **[Architecture](../docs/ARCHITECTURE.md)** – System design
