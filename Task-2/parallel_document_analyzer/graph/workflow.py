from langgraph.graph import StateGraph , START , END
from graph.state  import DocumentState

from graph.node import (
    load_document,
    summarize_document,
    extract_topics,
    analyze_sentiment,
    merge_results
)

builder = StateGraph(DocumentState)


builder.add_node("load_document"  , load_document)
builder.add_node("summary" , summarize_document)
builder.add_node("Extract_topics" , extract_topics)
builder.add_node("Analyze" , analyze_sentiment)
builder.add_node("merge_results" , merge_results)


builder.add_edge(START , "load_document")
builder.add_edge("load_document" , "summary")
builder.add_edge("load_document" , "Extract_topics")
builder.add_edge("load_document", "Analyze")
builder.add_edge("summary" , "merge_results")
builder.add_edge("Extract_topics" , "merge_results")
builder.add_edge("Analyze" , "merge_results")


builder.add_edge("merge_results" ,END)

graph = builder.compile()


# print(graph.get_graph().draw_mermaid())