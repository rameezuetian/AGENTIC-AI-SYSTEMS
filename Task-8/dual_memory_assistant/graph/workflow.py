from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langgraph.checkpoint.sqlite import (
    SqliteSaver
)

from graph.state import (
    AssistantState
)

from graph.nodes import (
    memory_extraction_node,
    summarization_node,
    chat_node,
)

builder = StateGraph(
    AssistantState
)

builder.add_node(
    "memory_extraction",
    memory_extraction_node
)

builder.add_node(
    "summarization",
    summarization_node
)

builder.add_node(
    "chat",
    chat_node
)

builder.add_edge(
    START,
    "memory_extraction"
)

builder.add_edge(
    "memory_extraction",
    "summarization"
)

builder.add_edge(
    "summarization",
    "chat"
)

builder.add_edge(
    "chat",
    END
)

memory = SqliteSaver.from_conn_string(
    "chat_history.db"
)

graph = builder.compile(
    checkpointer=memory
)
