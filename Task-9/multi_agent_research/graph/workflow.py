from langgraph.graph import (
    StateGraph,
    START,
    END
)

from graph.state import (
    ResearchState
)

from graph.nodes import (
    supervisor_node,
    researcher_node,
    analyst_node,
    writer_node,
    end_node
)

builder = StateGraph(
    ResearchState
)


builder.add_node(
    "supervisor",
    supervisor_node
)

builder.add_node(
    "researcher",
    researcher_node
)

builder.add_node(
    "analyst",
    analyst_node
)

builder.add_node(
    "writer",
    writer_node
)

builder.add_node(
    "end_node",
    end_node
)

builder.add_edge(
    START,
    "supervisor"
)

builder.add_edge(
    "end_node",
    END
)
graph = builder.compile()
