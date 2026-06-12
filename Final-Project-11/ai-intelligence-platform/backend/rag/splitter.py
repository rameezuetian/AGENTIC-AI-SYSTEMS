from __future__ import annotations


def split_documents(documents: list[dict], chunk_size: int = 900, overlap: int = 150) -> list[dict]:
    chunks: list[dict] = []

    for document in documents:
        text = document["page_content"]
        metadata = document["metadata"]
        start = 0
        index = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            chunks.append(
                {
                    "page_content": chunk_text,
                    "metadata": {
                        **metadata,
                        "chunk_index": index,
                    },
                }
            )
            if end >= len(text):
                break
            start = max(end - overlap, start + 1)
            index += 1

    return chunks
