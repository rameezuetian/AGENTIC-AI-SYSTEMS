from langgraph.graph import StateGraph  , START  , END

from graph.state import EssayState

from graph.node import (
    writer_node,
    critic_node
)
def should_continue(state):

    score = state["score"]

    iteration = state["iteration"]

    print(
        f"\nCurrent Score: {score}"
    )

    print(
        f"Current Iteration: {iteration}"
    )

    if score >= 7:

        print(
            "\nEssay Accepted!"
        )

        return END

    if iteration >= 5:

        print(
            "\nMaximum Iterations Reached!"
        )

        return END

    print(
        "\nEssay Needs Improvement..."
    )

    return "writer"

builder = StateGraph(EssayState)

builder.add_node('writer', writer_node)
builder.add_node('critic', critic_node)

builder.add_edge(START , 'writer')
builder.add_edge('writer' ,'critic')
builder.add_conditional_edges('critic' , should_continue)


graph = builder.compile()