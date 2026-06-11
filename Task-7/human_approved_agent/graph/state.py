from typing_extensions import TypedDict


class AgentState(TypedDict):

    task: str

    plan: str

    decision: str

    execution_result: str

    edited_plan: str
