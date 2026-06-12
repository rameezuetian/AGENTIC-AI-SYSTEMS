from safety.input_guardrail import check_input


def safety_agent(state: dict) -> dict:
    safe, reason = check_input(state["question"])
    return {
        "safe": safe,
        "safety_decision": reason,
    }
