# MindCare – Project Components

This document describes each file and folder in the project, key concepts (including ADB), and how to use them.

---

## Table of Contents

- [Project Structure Overview](#project-structure-overview)
- [Backend Components](#backend-components)
- [Frontend Components](#frontend-components)
- [ADB (Android Debug Bridge)](#adb-android-debug-bridge)
- [Key Concepts](#key-concepts)

---

## Project Structure Overview

```
mental-health-project/
├── backend/                 # FastAPI backend
│   ├── main.py              # App entry, CORS, routers
│   ├── config.py            # Settings from .env
│   ├── auth.py              # JWT, password hashing
│   ├── database.py          # SQLAlchemy setup
│   ├── models.py            # User model
│   ├── schemas.py           # Pydantic schemas
│   ├── requirements.txt
│   ├── .env                 # Secrets (create from README)
│   ├── routers/
│   │   ├── auth.py          # Login, register
│   │   └── chat.py          # Chat API
│   ├── agents/
│   │   ├── alert_agent.py   # LLM risk detection
│   │   ├── chat_agent.py    # Therapy-style chat (Groq LLM)
│   │   └── emotion_detection_agents/
│   │       ├── text_analysis.py   # Text emotion detection
│   │       ├── audio_emt.py       # Audio emotion
│   │       ├── video_emt.py       # Video/face emotion
│   │       └── fusion.py          # Multimodal emotion fusion
│   ├── services/
│   │   ├── chat_service.py  # Chat orchestration
│   │   └── alert_service.py # ADB emergency alerts
│   └── utils/
│       └── emotion_constants.py   # Emotion label mappings
│
├── frontend/
│   └── client/              # React + Vite app
│       ├── src/
│       │   ├── main.jsx
│       │   ├── App.jsx
│       │   ├── pages/       # Login, SignUp, Chat, Crisis
│       │   ├── components/  # Sidebar, ChatInput, etc.
│       │   ├── api/         # auth.js, chatApi.js
│       │   ├── context/     # MediaDevicesContext
│       │   ├── hooks/       # useMediaDevices
│       │   └── utils/       # storage, riskDetection
│       └── package.json
│
└── docs/
    ├── COMPONENTS.md        # This file
    └── ARCHITECTURE.md     # Architecture overview
```

---

## Backend Components

### `main.py`
- FastAPI app entry point
- Loads `.env` via `load_dotenv()`
- Registers CORS for `localhost:5173` and `127.0.0.1:5173`
- Includes auth and chat routers
- Runs `init_db()` on startup

### `config.py`
- Pydantic `Settings` class
- Reads from `.env`: `secret_key`, `database_url`, `GROQ_API_KEY`, `ADB_PATH`
- Defaults: `algorithm=HS256`, `access_token_expire_minutes=10080` (7 days)

### `auth.py`
- `hash_password()` / `verify_password()` – bcrypt
- `create_access_token()` – JWT with user id
- `get_current_user()` – FastAPI dependency for protected routes
- `user_to_response()` – maps User to response schema

### `database.py`
- SQLAlchemy engine and `SessionLocal`
- `get_db()` – dependency that yields a DB session
- `init_db()` – creates tables from models

### `models.py`
- **User** model: `id`, `username`, `password`, `age`, `gender`, `phone_number`, `address`, `emergency_contact_name`, `emergency_contact_phone`, `degree_info`, `created_at`

### `schemas.py`
- **UserCreate** – registration payload (username, password, age, gender, phone, address, emergency_contact)
- **UserLogin** – username, password
- **Token** – access_token, token_type, user
- **ChatMessageCreate** – text, mic_on, camera_on, session_id
- **ChatMessageResponse** – reply

### `routers/auth.py`
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register` | POST | Create user, return JWT |
| `/api/auth/login` | POST | Validate credentials, return JWT |

### `routers/chat.py`
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat/message` | POST | Send message, get LLM reply. Protected (JWT). Calls `chat_service.process_chat_message`. |

### `agents/chat_agent.py`
- `generate_chat_reply(text, current_emotion, user)` – generates empathetic therapy-style response
- Uses Groq `llama-3.1-8b-instant`
- Prompt includes user profile (age, gender), current emotion, and user message

### `agents/alert_agent.py`
- `detect_suicide_risk(text, user)` – sends text to Groq LLM
- System prompt: classify as YES (suicidal/self-harm) or NO
- If YES: calls `trigger_alert()` in `alert_service.py`
- Model: `llama-3.1-8b-instant`

### `services/alert_service.py`
- `trigger_alert(user, message)` – emergency alert
- Uses `ADB_PATH` from config
- Runs ADB to start a phone call to `emergency_contact_phone`
- See [ADB section](#adb-android-debug-bridge) below

### `services/chat_service.py`
- `process_chat_message(data, user)` – orchestrates chat flow before sending to the LLM
- **Flow:**
  1. Suicide risk detection via `detect_suicide_risk(text, user)`
  2. Interaction mode determination (text-only, mic-only, text+video, mic+video)
  3. Emotion detection for the active mode (e.g. text-only via `text_emotion(text)`)
  4. Chat reply generation via `generate_chat_reply(text, current_emotion, user)`
- Returns the assistant reply string

### `agents/emotion_detection_agents/text_analysis.py`
- **Text emotion detection** – analyzes user text for emotion
- **Model:** `j-hartmann/emotion-english-distilroberta-base` (HuggingFace transformers)
- **Function:** `text_emotion(text: str)` → `{"emotion": str, "confidence": float}`
- **Labels:** Maps raw labels (anger, disgust, fear, joy, neutral, sadness, surprise) to unified labels (angry, disgust, fearful, happy, neutral, sad, surprised) via `utils/emotion_constants.TEXT_EMOTION_MAP`
- Empty text returns `{"emotion": "neutral", "confidence": 100}`

### `utils/emotion_constants.py`
- `TEXT_EMOTION_MAP` – maps HuggingFace emotion labels to unified labels
- `EMOTIONS_MAP` – numeric ID to emotion name
- `EMOTION_DIMENSIONS` – valence/arousal values per emotion

---

## Frontend Components

### Pages

| File | Route | Purpose |
|------|-------|---------|
| `Login.jsx` | `/` | Username/password login form |
| `SignUp.jsx` | `/signup` | Registration with emergency contact |
| `Chat.jsx` | `/chat` | Main chat UI (sidebar, messages, camera, mic) |
| `Crisis.jsx` | `/crisis` | Crisis resources placeholder |

### Components

| File | Purpose |
|------|---------|
| `Sidebar.jsx` | Chat history grouped by date, new chat button |
| `ChatHeader.jsx` | Mic/camera/speaker toggles, status |
| `ChatInput.jsx` | Text input and send button |
| `MessageBubble.jsx` | User vs bot message styling |
| `CameraView.jsx` | Floating/draggable camera view |
| `RiskAlertBanner.jsx` | Crisis helplines when risk phrases detected |

### API Layer

| File | Purpose |
|------|---------|
| `api/auth.js` | `login()`, `register()`, `logout()`, `getStoredToken()`, `setStoredToken()`, `getAuthHeaders()` |
| `api/chatApi.js` | Chat API helpers (Chat.jsx may use `fetch` directly) |

### Context & Hooks

| File | Purpose |
|------|---------|
| `MediaDevicesContext.jsx` | Shared state for mic/camera/speaker |
| `useMediaDevices.js` | Access media streams and device state |

### Utils

| File | Purpose |
|------|---------|
| `storage.js` | Load/save chat state in `localStorage` |
| `riskDetection.js` | `checkRiskPhrases()` – client-side risk phrase detection |

---

## ADB (Android Debug Bridge)

### What It Is

ADB is a command-line tool for communicating with Android devices. In MindCare it is used to trigger emergency phone calls when the system detects suicide risk.

### How It Works

1. User sends a message in chat.
2. Backend runs `detect_suicide_risk()` in `alert_agent.py`.
3. Groq LLM classifies the message (YES = risk, NO = no risk).
4. If YES, `trigger_alert()` in `alert_service.py` is called.
5. `trigger_alert()` runs:
   ```bash
   adb shell am start -a android.intent.action.CALL -d tel:+91{emergency_contact_phone}
   ```
6. The connected Android device starts a call to the emergency contact.

### Setup Requirements

1. **Install ADB**
   - Windows: [Platform Tools](https://developer.android.com/studio/releases/platform-tools)
   - Mac: `brew install android-platform-tools`
   - Linux: `sudo apt install adb` (or equivalent)

2. **Configure Path**
   - Set `ADB_PATH` in `backend/.env` to the full path of `adb` (or `adb.exe` on Windows).
   - Example: `ADB_PATH=C:/Users/You/platform-tools/adb.exe`

3. **Android Device**
   - Connect via USB.
   - Enable **Developer options** → **USB debugging**.
   - Run `adb devices` to confirm the device is listed.

4. **User Data**
   - User must have `emergency_contact_name` and `emergency_contact_phone` set (during signup).

### Testing Without ADB

- Use a dummy `ADB_PATH` (e.g. `C:/dummy/adb.exe`).
- The app will run; `trigger_alert()` will fail when called, but other features work.

### Security Note

ADB has broad device access. Use only on trusted devices and in controlled environments.

---

## Key Concepts

### JWT Authentication

- Login/register return an `access_token`.
- Frontend stores it in `localStorage` under `mindcare_token`.
- Protected requests send: `Authorization: Bearer <token>`.
- Backend uses `get_current_user` to validate and load the user.

### Risk Detection (Two Layers)

1. **Frontend** (`riskDetection.js`): `checkRiskPhrases()` scans for known risk phrases and shows `RiskAlertBanner` with helplines.
2. **Backend** (`alert_agent.py`): LLM classifies each message. If risk is detected, `trigger_alert()` runs and ADB triggers the emergency call.

### Chat Persistence

- Chat history is stored in `localStorage` (client-side only).
- No backend persistence for chat messages.

### Media Devices

- `MediaDevicesContext` and `useMediaDevices` manage mic/camera/speaker state.
- `ChatHeader` toggles devices; `CameraView` shows the camera feed.

### Text Emotion Detection

- `text_emotion(text)` in `agents/emotion_detection_agents/text_analysis.py` analyzes user messages.
- Uses HuggingFace `j-hartmann/emotion-english-distilroberta-base` for sentiment/emotion classification.
- Output labels: angry, disgust, fearful, happy, neutral, sad, surprised.
- `chat_service` passes the detected emotion to `chat_agent` so replies can be context-aware.
