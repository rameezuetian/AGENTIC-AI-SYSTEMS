from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0
)
def planner_node(state):

    prompt = f"""
    Create a structured action plan
    for this task:

    {state['task']}

    Return a numbered plan.
    """

    response = llm.invoke(prompt)

    return {
        "plan": response.content
    }
    

def executor_node(state):

    plan = state["plan"]

    result = f"""
EXECUTION RESULT

Approved Plan Executed:

{plan}

Status:
SUCCESS
"""

    print("\nExecuting Plan...\n")

    return {
        "execution_result": result
    }