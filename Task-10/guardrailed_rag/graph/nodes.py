from langchain_google_genai import ChatGoogleGenerativeAI

from rag.retriever import retriever


INJECTION_PATTERNS = [
    "ignore previous",
    "ignore instructions",
    "system prompt",
    "developer message",
    "reveal hidden",
]


llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


def input_guardrail_node(state):
    question = state["question"].lower()

    for pattern in INJECTION_PATTERNS:
        if pattern in question:
            return {"guardrail_decision": "blocked_injection"}

    docs = retriever.invoke(state["question"])
    if len(docs) == 0:
        return {"guardrail_decision": "blocked_off_topic"}

    return {"guardrail_decision": "pass"}


def rejection_node(state):
    return {
        "answer": (
            "Sorry, your request was blocked because it appears unsafe or "
            "unrelated to the course documents."
        )
    }


def guardrail_router(state):
    if state["guardrail_decision"] == "pass":
        return "retrieve"
    return "reject"


def retrieve_node(state):
    docs = retriever.invoke(state["question"])
    sources = [doc.metadata.get("source", "Unknown") for doc in docs]

    return {
        "retrieved_docs": docs,
        "sources": sources,
    }


def generate_node(state):
    context = "\n\n".join(doc.page_content for doc in state["retrieved_docs"])
    prompt = f"""Answer ONLY using the provided context.

Context:
{context}

Question:
{state["question"]}
"""
    response = llm.invoke(prompt)
    return {"answer": response.content}


def output_guardrail_node(state):
    context = " ".join(doc.page_content.lower() for doc in state["retrieved_docs"])
    answer = state["answer"]
    grounded = False

    for word in answer.lower().split():
        if word in context:
            grounded = True
            break

    if not grounded:
        return {
            "answer": "[WARNING: POSSIBLE HALLUCINATION]\n\n" + answer,
            "guardrail_decision": "flagged",
        }

    return {"guardrail_decision": "pass"}
