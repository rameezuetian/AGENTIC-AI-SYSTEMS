import sqlite3

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)


def show_history(
    graph,
    config
):

    state = graph.get_state(config)

    if not state.values:

        print(
            "\nNo conversation history found."
        )

        return

    messages = state.values.get(
        "messages",
        []
    )

    print(
        "\n" +
        "=" * 60
    )

    print(
        "CONVERSATION HISTORY"
    )

    print(
        "=" * 60
    )

    for message in messages:

        if isinstance(
            message,
            HumanMessage
        ):

            print(
                f"\nUSER: {message.content}"
            )

        elif isinstance(
            message,
            AIMessage
        ):

            print(
                f"\nBOT: {message.content}"
            )


def show_checkpoints(
    graph,
    config
):

    print(
        "\nCHECKPOINT HISTORY\n"
    )

    for checkpoint in graph.get_state_history(
        config
    ):

        print(
            checkpoint
        )


def list_threads():

    try:

        conn = sqlite3.connect(
            "chat_history.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT DISTINCT thread_id
            FROM checkpoints
            """
        )

        rows = cursor.fetchall()

        conn.close()

        print(
            "\n" +
            "=" * 60
        )

        print(
            "ACTIVE THREADS"
        )

        print(
            "=" * 60
        )

        if not rows:

            print(
                "\nNo threads found."
            )

            return

        for row in rows:

            print(
                f"- {row[0]}"
            )

    except Exception as e:

        print(
            f"\nError: {e}"
        )