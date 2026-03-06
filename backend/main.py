from contextlib import asynccontextmanager
from agents.emotion_agent import initialize_models as initialize_emotion_models
from agents.chat_agent import initialize_model as initialize_chat_model

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routers import auth, chat_router

from dotenv import load_dotenv
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    initialize_emotion_models()
    initialize_chat_model()
    yield


app = FastAPI(title="MindCare API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router, prefix="/api")
app.include_router(chat_router.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "MindCare API", "docs": "/docs"}
