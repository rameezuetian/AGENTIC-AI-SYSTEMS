from pathlib import Path
from datetime import datetime


def save_report(trace, report):

    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    file_path = logs_dir / f"{timestamp}.txt"

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "=== EXECUTION TRACE ===\n\n"
        )

        for step in trace:

            file.write(
                f"{step}\n"
            )

        file.write(
            "\n\n=== FINAL REPORT ===\n\n"
        )

        file.write(report)

    return file_path