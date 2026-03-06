# MindCare – Architecture Overview

This document describes the system architecture, data flow, and design patterns used in MindCare.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React + Vite)                   │
│  Port 5173                                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │  Login   │  │  SignUp  │  │   Chat   │  │  MediaDevices     │ │
│  │  SignUp  │  │          │  │ Sidebar  │  │  Context          │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────────┬─────────┘ │
│       │             │             │                  │           │
│       └─────────────┴─────────────┴──────────────────┘           │
│                             │                                    │
│                    api/auth.js, fetch                             │
│                             │                                    │
└─────────────────────────────┼────────────────────────────────────┘
                              │ HTTP / REST
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND (FastAPI)                         │
│  Port 8000                                                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Routers: /api/auth/*, /api/chat/*                            ││
│  └──────────────────────────┬──────────────────────────────────┘│
│                              │                                    │
│  ┌──────────────────────────┼──────────────────────────────────┐│
│  │  Auth (JWT)  │  Database  │  Agents (LLM)  │  Services (ADB)  ││
│  └──────────────────────────┼──────────────────────────────────┘│
│                              │                                    │
│                    SQLite (mindcare.db)                           │
└──────────────────────────────┼────────────────────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Android Device     │
                    │  (ADB – emergency   │
                    │   phone call)       │
                    └─────────────────────┘
```

---

## Request Flow

### Authentication Flow

```
User → Login/SignUp form → api/auth.js → POST /api/auth/login|register
  → auth router → database (User) → JWT created
  → Token returned → Frontend stores in localStorage
  → Redirect to /chat
```

### Chat Flow

```
User types message → Chat.jsx → POST /api/chat/message (Bearer token)
  → chat router → get_current_user (JWT validation)
  → Groq LLM (chat reply)
  → alert_agent.detect_suicide_risk() (parallel/after)
  → If risk: alert_service.trigger_alert() → ADB → Phone call
  → Reply returned to frontend → MessageBubble
```

---

## Layer Responsibilities

| Layer | Responsibility |
|-------|----------------|
| **Frontend** | UI, routing, auth state, media devices, localStorage |
| **Routers** | HTTP handling, request validation, dependency injection |
| **Auth** | JWT creation/validation, password hashing |
| **Models/Schemas** | Data shape, validation |
| **Agents** | LLM-based logic (risk detection) |
| **Services** | External integrations (ADB) |
| **Database** | Persistence (users) |

---

## Design Patterns

### Dependency Injection (FastAPI)

- `Depends(get_db)` – injects DB session
- `Depends(get_current_user)` – injects authenticated user for protected routes

### Context + Hooks (React)

- `MediaDevicesContext` – shared mic/camera/speaker state
- `useMediaDevices` – hook to access and control media devices

### Two-Layer Risk Detection

1. **Client-side**: Immediate UI feedback via phrase matching
2. **Server-side**: LLM classification for alerts and ADB trigger

### Stateless API

- JWT in `Authorization` header; no server-side session storage
- Chat history stored client-side in `localStorage`

---

## Tech Stack Summary

| Component | Technology |
|-----------|------------|
| Frontend | React 19, Vite 7, React Router 7, Tailwind CSS 4 |
| Backend | FastAPI, Uvicorn |
| Database | SQLAlchemy, SQLite (PostgreSQL-ready) |
| Auth | JWT (python-jose), bcrypt |
| LLM | Groq (llama-3.1-8b-instant) |
| Emergency | ADB (Android Debug Bridge) |

---

## CORS Configuration

Backend allows:

- `http://localhost:5173`
- `http://127.0.0.1:5173`

Add more origins in `main.py` if needed (e.g. production frontend URL).
