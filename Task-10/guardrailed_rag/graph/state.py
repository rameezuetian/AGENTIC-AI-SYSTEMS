from typing_extensions import TypedDict


class RAGState(TypedDict):

    question: str

    retrieved_docs: list

    answer: str

    sources: list

    guardrail_decision: str
