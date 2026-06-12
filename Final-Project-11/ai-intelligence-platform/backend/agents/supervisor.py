PIPELINE = ["memory", "safety", "retriever", "analyst", "writer"]


def supervisor_agent(state: dict) -> list[str]:
    if state.get("safe", True):
        return PIPELINE
    return ["memory", "safety", "reject"]
