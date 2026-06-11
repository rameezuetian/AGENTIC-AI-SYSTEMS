# 🚀 LangChain vs LangGraph — Complete Study Notes

---

# 📖 Introduction

When building AI applications, two popular frameworks are:

* **LangChain**
* **LangGraph**

Although both are closely related, they solve different problems.

Think of them like this:

```text
LangChain = Straight Road

LangGraph = Road Network / Google Maps
```

LangChain is ideal for sequential workflows, while LangGraph is designed for complex, stateful AI agents.

---

# 1️⃣ What is LangChain?

**LangChain** is a framework for building applications powered by Large Language Models (LLMs).

It provides components for:

* Prompt Engineering
* LLM Integration
* Chains
* Tools
* Agents
* Memory
* Retrieval-Augmented Generation (RAG)

---

## LangChain Workflow

```text
User Input
     ↓
Prompt Template
     ↓
LLM
     ↓
Output
```

---

## Example

```python
chain = prompt | llm

response = chain.invoke({
    "question": "What is Artificial Intelligence?"
})
```

---

# 2️⃣ Chains in LangChain

A **Chain** is a sequence of operations executed one after another.

## Structure

```text
Input
 ↓
Step 1
 ↓
Step 2
 ↓
Step 3
 ↓
Output
```

---

## Example

```text
Question
 ↓
Retriever
 ↓
LLM
 ↓
Answer
```

This is the foundation of most RAG applications.

---

# 3️⃣ Tools in LangChain

Tools allow LLMs to interact with external systems.

Examples include:

| Tool        | Purpose                   |
| ----------- | ------------------------- |
| Calculator  | Mathematical calculations |
| Search API  | Search the web            |
| Weather API | Weather information       |
| Database    | Query data                |
| Python REPL | Execute code              |

---

## Example Tool

```python
from langchain.tools import tool

@tool
def multiply(a: int, b: int):
    return a * b
```

---

# 4️⃣ Agents in LangChain

Agents can:

* Think
* Reason
* Decide
* Choose tools
* Execute actions

---

## Agent Flow

```text
User Query
      ↓
Agent Thinks
      ↓
Chooses Tool
      ↓
Gets Result
      ↓
Final Answer
```

---

## Example

User:

```text
What is 250 × 450?
```

Agent:

```text
Need calculator
      ↓
Call Tool
      ↓
Get Result
      ↓
Respond
```

---

# 5️⃣ What is LangGraph?

LangGraph is a framework built on top of LangChain.

It is designed for:

* Stateful Workflows
* Multi-Agent Systems
* Cyclic Execution
* Human-in-the-Loop Applications
* Advanced AI Agents

---

## Graph-Based Architecture

```text
        A
       / \
      B   C
       \ /
        D
```

Unlike LangChain, execution is not restricted to a straight line.

---

# 6️⃣ Why LangGraph Exists

LangChain works well for:

```text
A → B → C → D
```

But real-world agents require:

* Memory
* Loops
* Retry Logic
* Decision Making
* Branching
* Multiple Agents

---

## Example

```text
Generate Answer
       ↓
Review Answer
       ↓
Good?
  ↓ Yes      ↓ No
 Finish    Improve
               ↓
         Generate Again
```

This cycle is difficult in traditional chains.

LangGraph solves this problem naturally.

---

# 7️⃣ LangChain vs LangGraph

| Feature             | LangChain  | LangGraph |
| ------------------- | ---------- | --------- |
| Structure           | Linear     | Graph     |
| Flow                | Sequential | Dynamic   |
| Loops               | Limited    | Native    |
| State Management    | Basic      | Advanced  |
| Multi-Agent Support | Difficult  | Excellent |
| Complex Workflows   | Limited    | Excellent |
| Human Approval      | Difficult  | Easy      |
| Retry Logic         | Manual     | Built-In  |

---

## Visual Comparison

### LangChain

```text
Input
 ↓
A
 ↓
B
 ↓
C
 ↓
Output
```

---

### LangGraph

```text
Input
 ↓
A
 ↓
Decision
 ↙     ↘
B       C
 \     /
   D
   ↓
Output
```

---

# 8️⃣ StateGraph — Core Primitive

The central component of LangGraph is:

```python
StateGraph
```

It acts as the graph builder and execution manager.

---

## Creating a StateGraph

```python
from langgraph.graph import StateGraph

graph = StateGraph(MyState)
```

---

## Responsibilities

StateGraph manages:

* Nodes
* Edges
* Shared State
* Execution Flow

---

# 9️⃣ State Schema

State is shared memory used by all nodes.

A schema defines what information can be stored.

Typically created using:

```python
TypedDict
```

---

## Example

```python
from typing import TypedDict

class AgentState(TypedDict):
    question: str
    answer: str
```

---

## State Example

```python
{
    "question": "What is AI?",
    "answer": ""
}
```

---

# 🔟 Nodes

Nodes are Python functions.

Each node:

* Reads state
* Performs work
* Returns updated state

---

## Example Node

```python
def generate_answer(state):

    question = state["question"]

    answer = llm.invoke(question)

    return {
        "answer": answer
    }
```

---

## Node Lifecycle

```text
Shared State
      ↓
Node Executes
      ↓
Updated State
```

---

## Before

```python
{
    "question": "What is AI?"
}
```

---

## After

```python
{
    "question": "What is AI?",
    "answer": "Artificial Intelligence is..."
}
```

---

# 1️⃣1️⃣ Edges

Edges connect nodes.

They define execution order.

---

## Example

```python
graph.add_edge(
    "generate",
    "review"
)
```

---

## Visualization

```text
Generate
    ↓
Review
```

---

# 1️⃣2️⃣ Conditional Edges

Conditional edges enable decision-making.

---

## Example

```python
graph.add_conditional_edges(
    "review",
    route_function
)
```

---

## Route Function

```python
def route_function(state):

    if state["score"] > 8:
        return "finish"

    return "retry"
```

---

## Flow

```text
Review
   ↓
Score?
 ↓      ↓
Good   Bad
 ↓      ↓
End   Retry
```

---

# 1️⃣3️⃣ When to Use LangChain

Choose LangChain for:

### ✅ Chatbots

```text
User → LLM → Response
```

### ✅ Summarization

```text
Document → LLM → Summary
```

### ✅ Translation

```text
Input → LLM → Output
```

### ✅ Basic RAG

```text
Question
 ↓
Retriever
 ↓
LLM
 ↓
Answer
```

---

# 1️⃣4️⃣ When to Use LangGraph

Choose LangGraph for:

### ✅ Multi-Agent Systems

```text
Research Agent
      ↓
Writer Agent
      ↓
Reviewer Agent
```

---

### ✅ Self-Correcting Agents

```text
Generate
 ↓
Review
 ↓
Bad?
 ↓
Retry
```

---

### ✅ Human Approval Workflows

```text
Generate Report
 ↓
Human Review
 ↓
Approve?
```

---

### ✅ Complex Tool Calling

```text
Think
 ↓
Search Tool
 ↓
Think
 ↓
Database Tool
 ↓
Answer
```

---

# 1️⃣5️⃣ Compiling a Graph

Before execution, the graph must be compiled.

---

## Syntax

```python
workflow = graph.compile()
```

---

## What Compile Does

```text
Validate Nodes
      +
Validate Edges
      +
Prepare Execution Engine
```

---

# 1️⃣6️⃣ Invoking a Graph

After compilation:

```python
result = workflow.invoke({
    "question": "What is AI?"
})
```

---

## Execution

```text
Input State
      ↓
Node A
      ↓
Node B
      ↓
Node C
      ↓
Final State
```

---

## Output

```python
{
    "question": "What is AI?",
    "answer": "Artificial Intelligence..."
}
```

---

# 1️⃣7️⃣ Complete LangGraph Example

```python
from typing import TypedDict
from langgraph.graph import StateGraph

class State(TypedDict):
    question: str
    answer: str

def generate(state):
    return {
        "answer":
        f"Answer for {state['question']}"
    }

graph = StateGraph(State)

graph.add_node(
    "generate",
    generate
)

graph.set_entry_point(
    "generate"
)

graph.set_finish_point(
    "generate"
)

workflow = graph.compile()

result = workflow.invoke({
    "question": "What is AI?"
})

print(result)
```

---

# 🎯 Interview Quick Revision

## LangChain

* Framework for LLM applications
* Uses Chains, Tools, Agents
* Best for linear workflows

---

## LangGraph

* Built on top of LangChain
* Uses graph-based execution
* Best for complex AI agents

---

## StateGraph

* Core LangGraph component
* Manages nodes, edges, and state

---

## State

* Shared memory across all nodes

---

## Node

* Python function
* Reads and updates state

---

## Edge

* Connects nodes
* Defines execution order

---

## Conditional Edge

* Dynamically decides next node

---

## graph.compile()

* Converts graph into executable workflow

---

## graph.invoke()

* Runs the graph

---

# 🧠 Memory Trick

```text
LangChain = Sequential Pipeline

LangGraph = Stateful Agent Workflow
```

OR

```text
LangChain = Road

LangGraph = Google Maps
```

LangGraph can:

✔ Remember State
✔ Make Decisions
✔ Retry Tasks
✔ Use Multiple Agents
✔ Loop Until Success

while LangChain mainly follows a straight sequence of steps.

---

# 🚀 Final Summary

| LangChain            | LangGraph          |
| -------------------- | ------------------ |
| Linear Workflow      | Graph Workflow     |
| Chains               | Nodes & Edges      |
| Simple Pipelines     | Complex Agents     |
| Sequential Execution | Dynamic Execution  |
| Limited State        | Shared State       |
| RAG Applications     | Agentic AI Systems |

### Rule of Thumb

```text
Simple AI App?
→ Use LangChain

Complex Stateful Agent?
→ Use LangGraph
```
