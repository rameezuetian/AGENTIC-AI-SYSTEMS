from rag.retriever import retrieve


def retriever_agent(state: dict) -> dict:
    documents = retrieve(state["question"])
    return {
        "retrieved_docs": documents,
        "sources": [
            document.get("metadata", {}).get("source", "Unknown")
            for document in documents
        ],
    }
