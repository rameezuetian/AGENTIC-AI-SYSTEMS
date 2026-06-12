from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Load local environment variables from .env if present
load_dotenv(dotenv_path=BASE_DIR / ".env")



@dataclass(frozen=True)
class Settings:
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    chroma_db_dir: Path = BASE_DIR / os.getenv("CHROMA_DB_DIR", "vectorstore")
    upload_dir: Path = BASE_DIR / os.getenv("UPLOAD_DIR", "uploads")
    log_dir: Path = BASE_DIR / os.getenv("LOG_DIR", "logs")
    memory_store_file: Path = BASE_DIR / "memory" / "memory_store.json"
    session_store_file: Path = BASE_DIR / "memory" / "sessions.json"
    vectorstore_file: Path = BASE_DIR / os.getenv("CHROMA_DB_DIR", "vectorstore") / "documents.json"


settings = Settings()

for directory in (
    settings.chroma_db_dir,
    settings.upload_dir,
    settings.log_dir,
    settings.memory_store_file.parent,
):
    directory.mkdir(parents=True, exist_ok=True)
