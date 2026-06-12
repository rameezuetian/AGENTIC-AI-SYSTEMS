from memory.memory_extractor import extract_memory


def memory_agent(state: dict) -> dict:
    extract_memory(state["question"], state["user_id"])
    return {}
