from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.messages import (
    AIMessage,
    SystemMessage,
)

from memory.store import store

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3
)


PERSONAL_PATTERNS = [
    "i prefer",
    "i like",
    "my deadline",
    "my favorite",
    "i work with",
    "i am learning",
    "i use",
]


def memory_extraction_node(
    state,
    config,
):

    user_id = config["configurable"]["user_id"]

    latest_message = state["messages"][-1]

    if not hasattr(
        latest_message,
        "content"
    ):
        return {}

    content = latest_message.content.lower()

    for pattern in PERSONAL_PATTERNS:

        if pattern in content:

            memory_key = str(
                abs(hash(content))
            )

            store.put(
                namespace=(
                    "users",
                    user_id
                ),
                key=memory_key,
                value={
                    "fact": content
                }
            )

            print(
                f"\n[Memory Stored] {content}"
            )

            break

    return {}

def summarization_node(state):

    messages = state["messages"]

    if len(messages) <= 10:
        return {}

    old_messages = messages[:-10]

    text = "\n".join(
        [
            msg.content
            for msg in old_messages
            if hasattr(msg, "content")
        ]
    )

    prompt = f"""
    Summarize this conversation briefly:

    {text}
    """

    summary = llm.invoke(
        prompt
    )

    return {
        "summary":
        summary.content
    }
    
    
def chat_node(
    state,
    config
):

    user_id = config["configurable"]["user_id"]

    memories = store.search(
        namespace=(
            "users",
            user_id
        )
    )

    memory_text = "\n".join(
        [
            item.value["fact"]
            for item in memories
        ]
    )

    summary = state.get(
        "summary",
        ""
    )

    system_prompt = f"""
You are a helpful AI assistant.

Known user facts:

{memory_text}

Conversation summary:

{summary}

Use these facts when relevant.
"""

    trimmed_messages = (
        state["messages"][-10:]
    )

    response = llm.invoke(
        [
            SystemMessage(
                content=system_prompt
            )
        ]
        +
        trimmed_messages
    )

    return {
        "messages": [
            AIMessage(
                content=response.content
            )
        ]
    }
