from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from langgraph.checkpoint.sqlite import SqliteSaver

from graph.state import ChatState
from graph.nodes import (
    retrieve_node,
    generate_node,
)

builder = StateGraph(ChatState)

builder.add_node(
    "retrieve",
    retrieve_node
)

builder.add_node(
    "generate",
    generate_node
)

builder.add_edge(
    START,
    "retrieve"
)

builder.add_edge(
    "retrieve",
    "generate"
)

builder.add_edge(
    "generate",
    END
)

memory = SqliteSaver.from_conn_string(
    "chat_history.db"
)

graph = builder.compile(
    checkpointer=memory
)
