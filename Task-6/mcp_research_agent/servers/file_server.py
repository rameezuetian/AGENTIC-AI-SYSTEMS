from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "FileServer"
)

ALLOWED_DIR = Path(
    "data/documents"
).resolve()


@mcp.tool()
def read_file(path: str) -> str:

    target = (
        ALLOWED_DIR / path
    ).resolve()

    if not str(target).startswith(
        str(ALLOWED_DIR)
    ):
        return "Access denied."

    if not target.exists():
        return "File not found."

    with open(
        target,
        "r",
        encoding="utf-8"
    ) as f:
        return f.read()


if __name__ == "__main__":
    mcp.run()
