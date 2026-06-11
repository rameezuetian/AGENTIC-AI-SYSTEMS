from pathlib import Path
from datetime import datetime


def save_essay_logs(state):

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
            "=" * 70 +
            "\nSELF CORRECTING ESSAY WRITER\n" +
            "=" * 70 +
            "\n\n"
        )

        file.write(
            f"TOPIC:\n{state['topic']}\n\n"
        )

        file.write(
            "=" * 70 +
            "\nITERATION LOGS\n" +
            "=" * 70 +
            "\n"
        )

        for log in state["logs"]:

            file.write(log)

            file.write("\n")

        file.write(
            "\n" +
            "=" * 70 +
            "\nFINAL ACCEPTED ESSAY\n" +
            "=" * 70 +
            "\n\n"
        )

        file.write(state["essay"])

        file.write("\n\n")

        file.write(
            f"FINAL SCORE: {state['score']}\n"
        )

    return file_path