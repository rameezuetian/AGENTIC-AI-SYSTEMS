def reject_agent(state: dict) -> dict:
    return {
        "answer": "Request blocked by safety policy.",
        "sources": [],
    }
