import json
from datetime import datetime
from pathlib import Path


def save_session(state) -> None:
    logs_dir = Path("logs")
    logs_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = logs_dir / f"session_{timestamp}.json"

    serializable_state = {
        "question": state.get("question"),
        "answer": state.get("answer"),
        "sources": state.get("sources", []),
        "guardrail_decision": state.get("guardrail_decision"),
    }

    log_file.write_text(
        json.dumps(serializable_state, indent=2),
        encoding="utf-8",
    )
