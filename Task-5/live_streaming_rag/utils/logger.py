from pathlib import Path
from datetime import datetime


def log_chat(
    thread_id,
    user_message,
    bot_message,
):

    logs_dir = Path("logs")

    logs_dir.mkdir(
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    file_path = (
        logs_dir /
        f"{thread_id}_{timestamp}.txt"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            f"THREAD ID: {thread_id}\n\n"
        )

        file.write(
            f"USER:\n{user_message}\n\n"
        )

        file.write(
            f"BOT:\n{bot_message}\n"
        )

    return file_path
