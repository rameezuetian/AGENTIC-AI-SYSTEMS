from typing_extensions import TypedDict


class AgentState(TypedDict):

    question: str

    user_id: str

    retrieved_docs: list

    analysis: str

    answer: str

    sources: list

    next_agent: str

    safety_decision: str