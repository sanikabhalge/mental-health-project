# MindCare – Mental Health Chat Project

A full-stack mental health support app with JWT auth, AI chat (Groq LLM), risk detection, and emergency alerts via ADB (Android).

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Configuration Reference](#configuration-reference)
- [Running the Project](#running-the-project)
- [Troubleshooting](#troubleshooting)
- [Documentation](#documentation)

---

## Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| **Node.js** | 18+ | Frontend (React + Vite) |
| **npm** | 9+ | Package manager |
| **Python** | 3.10+ | Backend (FastAPI) |
| **Android device** (optional) | — | Emergency alerts via ADB |

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/mental-health-project.git
cd mental-health-project

# 2. Backend setup
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1    # Windows PowerShell
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt //the requirment.txt should work but if not then do
cd ..
pip install -r req.txt
#also need to install the ffmpeg package 
https://www.gyan.dev/ffmpeg/builds/ # extract this zip file 
#then add ffmpeg path to env vairable C:\ffmpeg\bin
# 3. Create backend/.env (see Configuration Reference below)
# Copy .env.example and fill in values

# 4. Start backend
uvicorn main:app --reload --port 8000

# 5. In a new terminal – Frontend setup
cd frontend/client
npm install
npm run dev

# 6. Open http://localhost:5173
```

---

## Detailed Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/mental-health-project.git
cd mental-health-project
```

Replace `YOUR_USERNAME` with the repo owner’s GitHub username.

---

### 2. Backend Setup

#### 2.1 Create Virtual Environment

```bash
cd backend
python -m venv venv
```

#### 2.2 Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

#### 2.3 Install Dependencies

```bash
pip install -r requirements.txt
```

If `python-dotenv` is missing (used by `main.py`), add it:
```bash
pip install python-dotenv
```

#### 2.4 Create `.env` File

Copy the example file and edit:

```bash
# Windows (from backend folder)
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Then edit `.env` with your values. Required variables:

```env
SECRET_KEY=your-super-secret-key-change-in-production
DATABASE_URL=sqlite:///./mindcare.db
GROQ_API_KEY=your-groq-api-key
ADB_PATH=C:/path/to/platform-tools/adb.exe
```

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Used to sign JWTs. Use a long random string in production. |
| `DATABASE_URL` | Yes | SQLite default: `sqlite:///./mindcare.db`. For PostgreSQL: `postgresql://user:pass@localhost/mindcare` |
| `GROQ_API_KEY` | Yes | Get from [console.groq.com](https://console.groq.com). Used for chat and risk detection. |
| `ADB_PATH` | Yes* | Full path to `adb.exe`. *Required only if using emergency alerts. |

**Getting a Groq API Key:**
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up or log in
3. Create an API key under API Keys
4. Copy and paste into `GROQ_API_KEY`

**ADB Path (Windows):**
- Download [Platform Tools](https://developer.android.com/studio/releases/platform-tools)
- Extract and use path like: `C:/Users/YourName/platform-tools/adb.exe`

**ADB Path (Mac/Linux):**
- Often: `/Users/YourName/Library/Android/sdk/platform-tools/adb`
- Or install via: `brew install android-platform-tools` (Mac)

#### 2.5 First Run

On first run, SQLite creates `mindcare.db` in the `backend` folder with a `users` table.

---

### 3. Frontend Setup

#### 3.1 Install Dependencies

```bash
cd frontend/client
npm install
```

#### 3.2 Optional: Frontend Environment

Create `frontend/client/.env` if the backend runs on a different host/port:

```env
VITE_API_URL=http://localhost:8000
```

Default is `http://localhost:8000` if not set.

---

## Configuration Reference

### Backend (`backend/.env`)

| Variable | Example | Notes |
|----------|---------|-------|
| `SECRET_KEY` | `my-secret-key-123` | Min 32 chars recommended for production |
| `DATABASE_URL` | `sqlite:///./mindcare.db` | SQLite (dev) or PostgreSQL (prod) |
| `GROQ_API_KEY` | `gsk_xxxxx` | From Groq console |
| `ADB_PATH` | `C:/platform-tools/adb.exe` | Full path to ADB executable |

### Frontend (`frontend/client/.env`)

| Variable | Example | Notes |
|----------|---------|-------|
| `VITE_API_URL` | `http://localhost:8000` | Backend API base URL |

### Backend Config (`backend/config.py`)

Additional settings (with defaults):

- `algorithm`: `HS256` (JWT algorithm)
- `access_token_expire_minutes`: `10080` (7 days)

---

## Running the Project

### Option A: Two Terminals

**Terminal 1 – Backend:**
```bash
cd backend
venv\Scripts\Activate.ps1   # or source venv/bin/activate
uvicorn main:app --reload --port 8000
```

**Terminal 2 – Frontend:**
```bash
cd frontend/client
npm run dev
```

### URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

---

## Troubleshooting

### Backend won’t start – missing env vars

**Error:** `ValidationError` or `secret_key`, `GROQ_API_KEY`, etc. missing

**Fix:** Ensure `backend/.env` exists and contains all required variables. Variable names must match exactly (case-sensitive).

### CORS errors in browser

**Fix:** Backend allows `http://localhost:5173` and `http://127.0.0.1:5173`. If using a different port, add it in `backend/main.py`:

```python
allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:YOUR_PORT"]
```

### ADB not found / emergency alerts fail

- Ensure `ADB_PATH` in `.env` is the full path to `adb.exe`
- On Windows, use forward slashes or escaped backslashes
- For testing without a device, you can use a dummy path; alerts will fail but the app will run

### Frontend can’t reach backend

- Confirm backend is running on port 8000
- If backend is elsewhere, set `VITE_API_URL` in `frontend/client/.env`
- Restart the Vite dev server after changing `.env`

### Database locked / SQLite errors

- Close other processes using `mindcare.db`
- For concurrent access, consider switching to PostgreSQL via `DATABASE_URL`

---

## Documentation

- **[COMPONENTS.md](docs/COMPONENTS.md)** – File-by-file breakdown, ADB usage, concepts
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** – System architecture and design

---

## Teammate Quick Reference

```bash
git clone https://github.com/YOUR_USERNAME/mental-health-project.git
cd mental-health-project
# Follow "Detailed Setup" above – create backend/.env with your keys
cd backend && python -m venv venv && .\venv\Scripts\Activate.ps1 && pip install -r requirements.txt
uvicorn main:app --reload --port 8000
# New terminal:
cd frontend/client && npm install && npm run dev
# Open http://localhost:5173
```
