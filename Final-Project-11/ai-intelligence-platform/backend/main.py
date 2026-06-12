from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.chat import router as chat_router
from api.chat_stream import router as chat_stream_router
from api.memory import router as memory_router
from api.sessions import router as sessions_router
from api.upload import router as upload_router


app = FastAPI(title="AI Intelligence Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(chat_stream_router, prefix="/api")
app.include_router(memory_router, prefix="/api")
app.include_router(sessions_router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "Backend running",
        "status": "ok",
    }


@app.get("/api/status")
def system_status():
    from config import settings
    key = settings.google_api_key
    gemini_connected = bool(key and key != "YOUR_GOOGLE_API_KEY")
    return {
        "status": "ok",
        "gemini_connected": gemini_connected,
        "model": "gemini-1.5-flash" if gemini_connected else "Local Heuristics",
    }

