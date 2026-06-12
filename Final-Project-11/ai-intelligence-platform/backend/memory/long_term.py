from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from config import settings


@dataclass
class MemoryRecord:
    key: str
    value: dict


class LongTermMemoryStore:
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

    def put(self, namespace: tuple[str, str], key: str, value: dict) -> None:
        data = self._read()
        bucket = data.setdefault("/".join(namespace), {})
        bucket[key] = value
        self._write(data)

    def search(self, namespace: tuple[str, str]) -> list[MemoryRecord]:
        data = self._read()
        bucket = data.get("/".join(namespace), {})
        return [MemoryRecord(key=key, value=value) for key, value in bucket.items()]

    def delete(self, namespace: tuple[str, str], key: str) -> None:
        data = self._read()
        bucket = data.get("/".join(namespace), {})
        if key in bucket:
            del bucket[key]
            self._write(data)


store = LongTermMemoryStore(settings.memory_store_file)
