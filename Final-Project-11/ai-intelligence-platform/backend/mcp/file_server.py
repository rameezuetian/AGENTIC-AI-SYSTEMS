"""MCP file server for managing file operations."""

import asyncio
import logging
import os
from pathlib import Path
from typing import Any, Optional

from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ToolResult,
)

logger = logging.getLogger(__name__)


class FileServer:
    """MCP server for file operations."""

    def __init__(self, base_path: str = "./data"):
        """Initialize file server.
        
        Args:
            base_path: Base directory for file operations
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.server = Server("file-server")
        self._setup_tools()

    def _setup_tools(self) -> None:
        """Setup available tools."""
        self.server.register_tool(
            Tool(
                name="read_file",
                description="Read contents of a file",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Relative path to file",
                        }
                    },
                    "required": ["path"],
                },
            ),
            self.read_file,
        )

        self.server.register_tool(
            Tool(
                name="write_file",
                description="Write contents to a file",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Relative path to file",
                        },
                        "content": {
                            "type": "string",
                            "description": "File content",
                        },
                    },
                    "required": ["path", "content"],
                },
            ),
            self.write_file,
        )

        self.server.register_tool(
            Tool(
                name="list_files",
                description="List files in a directory",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Relative path to directory",
                        }
                    },
                    "required": ["path"],
                },
            ),
            self.list_files,
        )

        self.server.register_tool(
            Tool(
                name="delete_file",
                description="Delete a file",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Relative path to file",
                        }
                    },
                    "required": ["path"],
                },
            ),
            self.delete_file,
        )

    async def read_file(self, path: str) -> ToolResult:
        """Read a file.
        
        Args:
            path: Relative file path
            
        Returns:
            File contents
        """
        try:
            full_path = self._validate_path(path)
            
            if not full_path.exists():
                return ToolResult(
                    content=[TextContent(type="text", text=f"File not found: {path}")]
                )
            
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            return ToolResult(
                content=[TextContent(type="text", text=content)]
            )
        except Exception as e:
            logger.error(f"Error reading file {path}: {e}")
            return ToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")]
            )

    async def write_file(self, path: str, content: str) -> ToolResult:
        """Write to a file.
        
        Args:
            path: Relative file path
            content: Content to write
            
        Returns:
            Success message
        """
        try:
            full_path = self._validate_path(path)
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            logger.info(f"Wrote file: {path}")
            return ToolResult(
                content=[TextContent(type="text", text=f"File written: {path}")]
            )
        except Exception as e:
            logger.error(f"Error writing file {path}: {e}")
            return ToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")]
            )

    async def list_files(self, path: str = ".") -> ToolResult:
        """List files in a directory.
        
        Args:
            path: Relative directory path
            
        Returns:
            List of files
        """
        try:
            full_path = self._validate_path(path)
            
            if not full_path.is_dir():
                return ToolResult(
                    content=[TextContent(type="text", text=f"Not a directory: {path}")]
                )
            
            files = []
            for item in sorted(full_path.iterdir()):
                if item.is_file():
                    files.append(f"  {item.name}")
                else:
                    files.append(f"  {item.name}/")
            
            content = "\n".join(files) if files else "Empty directory"
            return ToolResult(
                content=[TextContent(type="text", text=content)]
            )
        except Exception as e:
            logger.error(f"Error listing files {path}: {e}")
            return ToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")]
            )

    async def delete_file(self, path: str) -> ToolResult:
        """Delete a file.
        
        Args:
            path: Relative file path
            
        Returns:
            Success message
        """
        try:
            full_path = self._validate_path(path)
            
            if not full_path.exists():
                return ToolResult(
                    content=[TextContent(type="text", text=f"File not found: {path}")]
                )
            
            full_path.unlink()
            logger.info(f"Deleted file: {path}")
            return ToolResult(
                content=[TextContent(type="text", text=f"File deleted: {path}")]
            )
        except Exception as e:
            logger.error(f"Error deleting file {path}: {e}")
            return ToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")]
            )

    def _validate_path(self, path: str) -> Path:
        """Validate and sanitize file path.
        
        Args:
            path: Relative file path
            
        Returns:
            Validated absolute path
            
        Raises:
            ValueError: If path is invalid or outside base directory
        """
        full_path = (self.base_path / path).resolve()
        
        # Security check: ensure path is within base_path
        if not str(full_path).startswith(str(self.base_path)):
            raise ValueError(f"Access denied: path outside base directory")
        
        return full_path

    async def run(self, host: str = "localhost", port: int = 3001) -> None:
        """Run the server.
        
        Args:
            host: Server host
            port: Server port
        """
        logger.info(f"Starting file server on {host}:{port}")
        # This would be implemented with actual server framework
        await asyncio.sleep(3600)  # Run for 1 hour


async def start_file_server(base_path: str = "./data") -> None:
    """Start the file server.
    
    Args:
        base_path: Base directory for file operations
    """
    server = FileServer(base_path)
    await server.run()


if __name__ == "__main__":
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    base_path = sys.argv[1] if len(sys.argv) > 1 else "./data"
    asyncio.run(start_file_server(base_path))
