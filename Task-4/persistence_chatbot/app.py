from langchain_core.messages import (
    HumanMessage
)

from graph.workflow import graph

from utils.db_utils import (
    show_history,
    list_threads
)


def main():

    thread_id = input(
        "\nEnter Thread ID: "
    ).strip()

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    print(
        "\nLoading Conversation..."
    )

    show_history(
        graph,
        config
    )

    print(
        "\nAvailable Commands:"
    )

    print("/history")
    print("/threads")
    print("/exit")

    while True:

        user_input = input(
            "\nYou: "
        ).strip()

        if user_input.lower() == "/exit":

            print(
                "\nGoodbye!"
            )

            break

        if user_input.lower() == "/history":

            show_history(
                graph,
                config
            )

            continue

        if user_input.lower() == "/threads":

            list_threads()

            continue

        if not user_input:

            continue

        result = graph.invoke(
            {
                "messages": [
                    HumanMessage(
                        content=user_input
                    )
                ]
            },
            config=config
        )

        ai_message = result[
            "messages"
        ][-1]

        print(
            f"\nBot: {ai_message.content}"
        )


if __name__ == "__main__":
    main()