from uuid import uuid4

from langgraph.graph import END, START, StateGraph

from graph.nodes import (
    generate_node,
    guardrail_router,
    input_guardrail_node,
    output_guardrail_node,
    rejection_node,
    retrieve_node,
)
from graph.state import RAGState


builder = StateGraph(RAGState)

builder.add_node("input_guardrail", input_guardrail_node)
builder.add_node("retrieve", retrieve_node)
builder.add_node("generate", generate_node)
builder.add_node("output_guardrail", output_guardrail_node)
builder.add_node("reject", rejection_node)

builder.add_edge(START, "input_guardrail")
builder.add_conditional_edges(
    "input_guardrail",
    guardrail_router,
    {
        "retrieve": "retrieve",
        "reject": "reject",
    },
)
builder.add_edge("retrieve", "generate")
builder.add_edge("generate", "output_guardrail")
builder.add_edge("output_guardrail", END)
builder.add_edge("reject", END)

graph = builder.compile()

session_id = uuid4().hex[:8]
config = {
    "run_name": f"RAG_Session_{session_id}",
    "tags": ["rag", "guardrail"],
    "metadata": {"session": session_id},
}
