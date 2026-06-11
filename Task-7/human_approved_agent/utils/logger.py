from pathlib import Path
from datetime import datetime

def save_log(state):

    logs_dir = Path("logs")

    logs_dir.mkdir(
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    file_path = (
        logs_dir /
        f"{timestamp}.txt"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            f"TASK:\n{state['task']}\n\n"
        )

        f.write(
            f"ORIGINAL PLAN:\n"
            f"{state['plan']}\n\n"
        )

        f.write(
            f"DECISION:\n"
            f"{state['decision']}\n\n"
        )

        f.write(
            f"EDITED PLAN:\n"
            f"{state['edited_plan']}\n\n"
        )

        f.write(
            f"EXECUTION RESULT:\n"
            f"{state['execution_result']}"
        )

    return file_path
