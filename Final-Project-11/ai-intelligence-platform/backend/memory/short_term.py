from __future__ import annotations

import json
from pathlib import Path

from config import settings


class SessionStore:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        if not self.file_path.exists():
            self.file_path.write_text("{}", encoding="utf-8")

    def _read(self) -> dict:
        return json.loads(self.file_path.read_text(encoding="utf-8"))

    def _write(self, data: dict) -> None:
        self.file_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=True),
            encoding="utf-8",
        )

    def append_message(self, thread_id: str, role: str, content: str) -> None:
        data = self._read()
        thread = data.setdefault(thread_id, [])
        thread.append({"role": role, "content": content})
        self._write(data)

    def get_thread(self, thread_id: str) -> list[dict]:
        return self._read().get(thread_id, [])

    def list_threads(self) -> dict:
        return self._read()

    def delete_thread(self, thread_id: str) -> None:
        data = self._read()
        if thread_id in data:
            del data[thread_id]
            self._write(data)


memory = SessionStore(settings.session_store_file)
