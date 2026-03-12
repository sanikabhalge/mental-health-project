from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from database import init_db

from routers import chat
from routers import auth


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="MindCare API",
    lifespan=lifespan
)


# ---------------- CORS ---------------- #

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- ROUTERS ---------------- #

# Chat endpoints
app.include_router(chat.router)

# Auth endpoints
app.include_router(auth.router, prefix="/api")


# ---------------- ROOT ---------------- #

@app.get("/")
def root():
    return {
        "message": "MindCare API",
        "docs": "/docs"
    }