from langchain_core.messages import (
    HumanMessage,
)

from graph.workflow import graph

from utils.memory_utils import (
    show_memories,
)

thread_id = input(
    "Thread ID: "
)

user_id = input(
    "User ID: "
)

config = {
    "configurable": {
        "thread_id": thread_id,
        "user_id": user_id,
    }
}


def load_long_term_memories():

    print(
        "\nLoading Long-Term Memories...\n"
    )

    if user_id:
        show_memories(user_id)


load_long_term_memories()

print(
    "\nCommands:"
)

print("/memories")
print("/exit")

while True:

    user_input = input(
        "\nYou: "
    )

    if user_input == "/exit":
        break

    if user_input == "/memories":

        show_memories(
            user_id
        )

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
        f"\nAssistant: {ai_message.content}"
    )
