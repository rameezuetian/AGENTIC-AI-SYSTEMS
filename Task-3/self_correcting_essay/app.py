from graph.workflow import graph

from utils.logger import (
    save_essay_logs
)

topic = input("\n Enter Essay Topic")

initial_state = {

    "topic": topic,

    "essay": "",

    "score": 0,

    "feedback": "",

    "iteration": 0,

    "logs": []
}

result = graph.invoke(
    initial_state
)

print(
    "\n" +
    "=" * 70
)

print(
    "FINAL ESSAY"
)

print(
    "=" * 70
)

print(
    result["essay"]
)

print(
    f"\nFINAL SCORE: {result['score']}"
)

log_file = save_essay_logs(
    result
)

print(
    f"\nLogs saved to: {log_file}"
)