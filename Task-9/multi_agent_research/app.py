from graph.workflow import (
    graph
)

from utils.logger import (
    save_report
)

topic = input(
    "\nEnter Research Topic:\n"
)

initial_state = {

    "topic":
    topic,

    "research_output":
    "",

    "analysis_output":
    "",

    "report_output":
    "",

    "trace":
    [],

    "next_agent":
    "researcher"
}
result = graph.invoke(
    initial_state
)
print(
    "\n" +
    "=" * 60
)

print(
    "FINAL REPORT"
)

print(
    "=" * 60
)

print(
    result[
        "report_output"
    ]
)
print(
    "\n" +
    "=" * 60
)

print(
    "FINAL REPORT"
)

print(
    "=" * 60
)

print(
    result[
        "report_output"
    ]
)
