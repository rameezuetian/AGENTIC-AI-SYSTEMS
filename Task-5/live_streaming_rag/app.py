import asyncio

from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

from graph.workflow import graph

from utils.db_utils import (
    show_history,
    list_threads
)

from utils.logger import (
    log_chat
)

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
)


async def stream_response(
    thread_id,
    user_message,
    config,
):
    """
    Streams tokens from Gemini
    and saves final response.
    """

    print(
        "\n[Retrieving...]"
    )

    await asyncio.sleep(0.1)

    print(
        "[Generating...]\n"
    )

    response_text = ""

    try:

        async for chunk in llm.astream(
            user_message
        ):

            token = chunk.content

            response_text += token

            print(
                token,
                end="",
                flush=True
            )

        print("\n")

    except Exception as e:

        print(
            f"\nStreaming Error: {e}"
        )

        return

    graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content=user_message
                ),
                AIMessage(
                    content=response_text
                )
            ]
        },
        config=config
    )

    log_chat(
        thread_id,
        user_message,
        response_text
    )


async def main():

    thread_id = input(
        "\nEnter Thread ID: "
    ).strip()

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    print(
        "\nLoading History..."
    )

    show_history(
        graph,
        config
    )

    print(
        "\nCommands:"
    )

    print("/history")
    print("/threads")
    print("/exit")

    while True:

        user_input = input(
            "\nYou: "
        ).strip()

        if (
            user_input.lower()
            == "/exit"
        ):
            break

        if (
            user_input.lower()
            == "/history"
        ):
            show_history(
                graph,
                config
            )
            continue

        if (
            user_input.lower()
            == "/threads"
        ):
            list_threads()
            continue

        if not user_input:
            continue

        await stream_response(
            thread_id,
            user_input,
            config
        )

    print(
        "\nGoodbye!"
    )


if __name__ == "__main__":

    asyncio.run(
        main()
    )
