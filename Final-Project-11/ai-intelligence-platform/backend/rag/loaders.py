from __future__ import annotations

import csv
from pathlib import Path


def load_document(file_path: str) -> list[dict]:
    path = Path(file_path)
    ext = path.suffix.lower()

    if ext == ".txt":
        content = path.read_text(encoding="utf-8", errors="ignore")
    elif ext == ".csv":
        with path.open("r", encoding="utf-8", errors="ignore", newline="") as handle:
            reader = csv.reader(handle)
            rows = [" | ".join(row) for row in reader]
        content = "\n".join(rows)
    elif ext == ".pdf":
        content = (
            "PDF upload saved successfully. Text extraction is not enabled in this local mode, "
            "so retrieval will use the filename as context."
        )
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    return [
        {
            "page_content": content,
            "metadata": {
                "source": path.name,
                "path": str(path),
            },
        }
    ]
