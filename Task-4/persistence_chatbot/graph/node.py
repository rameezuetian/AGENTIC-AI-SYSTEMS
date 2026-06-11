from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.messages import AIMessage


load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7
)


def chatbot(state):

    print(
        f"\nMessages in History: "
        f"{len(state['messages'])}"
    )

    response = llm.invoke(
        state["messages"]
    )

    return {
        "messages": [
            AIMessage(
                content=response.content
            )
        ]
    }