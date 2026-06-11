from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

from langgraph.types import Command

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0
)

def supervisor_node(state):

    next_agent = state.get(
        "next_agent",
        "researcher"
    )

    if next_agent == "researcher":

        return Command(
            goto="researcher"
        )

    elif next_agent == "analyst":

        return Command(
            goto="analyst"
        )

    elif next_agent == "writer":

        return Command(
            goto="writer"
        )

    else:

        return Command(
            goto="end_node"
        )
        
        
def researcher_node(state):

    print(
        "\n[Web Researcher Running]"
    )

    prompt = f"""
Research this topic:

{state['topic']}

Provide:
- Key facts
- Important trends
- Relevant statistics
"""

    result = llm.invoke(
        prompt
    )

    print(
        "\n[Web Researcher Output]\n"
    )

    print(
        result.content
    )

    trace = state["trace"]

    trace.append(
        "Supervisor -> Web Researcher"
    )

    return Command(
        update={
            "research_output":
            result.content,

            "trace":
            trace,

            "next_agent":
            "analyst"
        },
        goto="supervisor"
    )
    
    
def analyst_node(state):

    print(
        "\n[Data Analyst Running]"
    )

    prompt = f"""
Analyze this research.

Focus on:

- Numbers
- Statistics
- Trends

Research:

{state['research_output']}
"""

    result = llm.invoke(
        prompt
    )

    print(
        "\n[Data Analyst Output]\n"
    )

    print(
        result.content
    )

    trace = state["trace"]

    trace.append(
        "Supervisor -> Data Analyst"
    )

    return Command(
        update={
            "analysis_output":
            result.content,

            "trace":
            trace,

            "next_agent":
            "writer"
        },
        goto="supervisor"
    )
    
def writer_node(state):

    print(
        "\n[Report Writer Running]"
    )

    prompt = f"""
Create a professional report.

Topic:
{state['topic']}

Research:
{state['research_output']}

Analysis:
{state['analysis_output']}
"""

    result = llm.invoke(
        prompt
    )

    print(
        "\n[Report Writer Output]\n"
    )

    print(
        result.content
    )

    trace = state["trace"]

    trace.append(
        "Supervisor -> Report Writer"
    )

    return Command(
        update={
            "report_output":
            result.content,

            "trace":
            trace,

            "next_agent":
            "done"
        },
        goto="supervisor"
    )
    
def end_node(state):

    print(
        "\n[Workflow Complete]"
    )

    return state
