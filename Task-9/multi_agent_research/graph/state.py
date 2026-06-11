from typing_extensions import TypedDict


class ResearchState(TypedDict):

    topic: str

    research_output: str

    analysis_output: str

    report_output: str

    trace: list[str]

    next_agent: str
