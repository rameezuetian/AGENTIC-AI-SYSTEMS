from __future__ import annotations

import json
from pathlib import Path

from config import settings


class LocalVectorStore:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        if not self.file_path.exists():
            self.file_path.write_text("[]", encoding="utf-8")

    def _read(self) -> list[dict]:
        return json.loads(self.file_path.read_text(encoding="utf-8"))

    def _write(self, records: list[dict]) -> None:
        self.file_path.write_text(
            json.dumps(records, indent=2, ensure_ascii=True),
            encoding="utf-8",
        )

    def add_documents(self, chunks: list[dict]) -> None:
        records = self._read()
        records.extend(chunks)
        self._write(records)

    def delete_document(self, filename: str) -> None:
        records = self._read()
        filtered = [r for r in records if r.get("metadata", {}).get("source") != filename]
        self._write(filtered)

    def all_documents(self) -> list[dict]:
        return self._read()


def get_vectorstore() -> LocalVectorStore:
    return LocalVectorStore(settings.vectorstore_file)

