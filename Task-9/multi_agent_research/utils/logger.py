from pathlib import Path

from datetime import datetime

def save_report(
    state
):

    Path(
        "logs"
    ).mkdir(
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    file_path = (
        Path("logs")
        /
        f"{timestamp}.txt"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            f"TOPIC\n\n"
        )

        f.write(
            state["topic"]
        )

        f.write(
            "\n\n"
        )

        f.write(
            "=" * 60
        )

        f.write(
            "\nTRACE\n\n"
        )

        for step in state["trace"]:

            f.write(
                step + "\n"
            )

        f.write(
            "\n\n"
        )

        f.write(
            "=" * 60
        )

        f.write(
            "\nFINAL REPORT\n\n"
        )

        f.write(
            state["report_output"]
        )

    return file_path
