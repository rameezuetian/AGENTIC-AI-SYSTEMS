from langgraph.graph import (
    StateGraph,
    START,
    END
)

from langgraph.checkpoint.sqlite import (
    SqliteSaver
)

from graph.state import ChatState

from graph.nodes import chatbot


builder = StateGraph(ChatState)

builder.add_node(
    "chatbot",
    chatbot
)

builder.add_edge(
    START,
    "chatbot"
)

builder.add_edge(
    "chatbot",
    END
)

memory = SqliteSaver.from_conn_string(
    "chat_history.db"
)

graph = builder.compile(
    checkpointer=memory
)