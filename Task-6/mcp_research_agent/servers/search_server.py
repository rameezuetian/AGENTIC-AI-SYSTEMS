import json

from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "SearchServer"
)


@mcp.tool()
def search_web(query: str) -> str:

    file_path = Path(
        "data/mock_search_results.json"
    )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    query = query.lower()

    results = data.get(
        query,
        ["No search results found."]
    )

    return "\n".join(results)


if __name__ == "__main__":
    mcp.run()
