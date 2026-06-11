import asyncio

from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

from langchain_mcp_adapters.client import (
    MultiServerMCPClient
)

from langchain_mcp_adapters.tools import (
    load_mcp_tools
)

from langgraph.prebuilt import (
    create_react_agent
)

from utils.logger import (
    save_trace
)

load_dotenv()


async def main():

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0
    )

    client = MultiServerMCPClient(
        {
            "search": {
                "command": "python",
                "args": [
                    "servers/search_server.py"
                ],
                "transport": "stdio"
            },
            "files": {
                "command": "python",
                "args": [
                    "servers/file_server.py"
                ],
                "transport": "stdio"
            }
        }
    )

    tools = await load_mcp_tools(
        client
    )

    agent = create_react_agent(
        llm,
        tools
    )

    question = input(
        "\nResearch Question: "
    )

    trace = []

    print(
        "\nRunning Agent...\n"
    )

    result = await agent.ainvoke(
        {
            "messages": [
                (
                    "user",
                    question
                )
            ]
        }
    )

    messages = result["messages"]

    for msg in messages:

        if hasattr(
            msg,
            "tool_calls"
        ) and msg.tool_calls:

            for call in msg.tool_calls:

                trace.append(
                    f"TOOL CALL:\n"
                    f"{call['name']}\n"
                    f"ARGS:\n"
                    f"{call['args']}"
                )

                print(
                    "\nTOOL CALL:"
                )

                print(
                    call["name"]
                )

                print(
                    call["args"]
                )

        if msg.type == "tool":

            trace.append(
                f"TOOL RESULT:\n"
                f"{msg.content}"
            )

            print(
                "\nRESULT:"
            )

            print(
                msg.content
            )

    final_answer = (
        messages[-1].content
    )

    print(
        "\n" +
        "=" * 60
    )

    print(
        "FINAL ANSWER"
    )

    print(
        "=" * 60
    )

    print(
        final_answer
    )

    log_file = save_trace(
        question,
        trace,
        final_answer
    )

    print(
        f"\nTrace saved to: {log_file}"
    )


if __name__ == "__main__":
    asyncio.run(main())
