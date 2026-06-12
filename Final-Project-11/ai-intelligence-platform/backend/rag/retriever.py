from __future__ import annotations

import re

from rag.chroma_manager import get_vectorstore


def _tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9]+", text.lower()))


def retrieve(query: str, k: int = 4) -> list[dict]:
    query_tokens = _tokenize(query)
    documents = get_vectorstore().all_documents()

    if not documents:
        return []

    scored: list[tuple[int, dict]] = []
    for document in documents:
        content_tokens = _tokenize(document.get("page_content", ""))
        score = len(query_tokens.intersection(content_tokens))
        if score > 0:
            scored.append((score, document))

    if not scored:
        return documents[:k]

    scored.sort(key=lambda item: item[0], reverse=True)
    return [document for _, document in scored[:k]]
