"""MCP client helpers for connecting to local MCP servers."""

import asyncio
import logging
from typing import Optional, Any

from mcp import ClientSession
from mcp.client.stdio import StdioClientTransport

logger = logging.getLogger(__name__)


class MCPClient:
    """Helper class for MCP client connections."""

    def __init__(self, server_name: str, command: list[str]):
        """Initialize MCP client.
        
        Args:
            server_name: Name of the server (for logging)
            command: Command to start the server
        """
        self.server_name = server_name
        self.command = command
        self.session: Optional[ClientSession] = None
        self.transport: Optional[StdioClientTransport] = None

    async def connect(self) -> bool:
        """Connect to MCP server.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Create stdio transport
            self.transport = StdioClientTransport(self.command)
            self.session = ClientSession(self.transport)
            
            # Initialize the connection
            await self.session.initialize()
            
            logger.info(f"Connected to {self.server_name} MCP server")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to {self.server_name}: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from MCP server."""
        if self.session:
            await self.session.close()
            logger.info(f"Disconnected from {self.server_name}")

    async def call_tool(self, tool_name: str, **kwargs) -> Any:
        """Call a tool on the MCP server.
        
        Args:
            tool_name: Name of the tool to call
            **kwargs: Arguments to pass to the tool
            
        Returns:
            Tool result
        """
        if not self.session:
            raise RuntimeError(f"Not connected to {self.server_name}")

        try:
            result = await self.session.call_tool(tool_name, kwargs)
            return result
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            raise

    async def list_tools(self) -> list[dict]:
        """List available tools on the server.
        
        Returns:
            List of tool definitions
        """
        if not self.session:
            raise RuntimeError(f"Not connected to {self.server_name}")

        try:
            response = await self.session.list_tools()
            return response.tools if response else []
        except Exception as e:
            logger.error(f"Error listing tools: {e}")
            return []

    async def list_resources(self) -> list[dict]:
        """List available resources on the server.
        
        Returns:
            List of resource definitions
        """
        if not self.session:
            raise RuntimeError(f"Not connected to {self.server_name}")

        try:
            response = await self.session.list_resources()
            return response.resources if response else []
        except Exception as e:
            logger.error(f"Error listing resources: {e}")
            return []


class MCPClientManager:
    """Manages multiple MCP client connections."""

    def __init__(self):
        """Initialize the manager."""
        self.clients: dict[str, MCPClient] = {}

    def register_client(self, name: str, server_name: str, command: list[str]) -> None:
        """Register a new MCP client.
        
        Args:
            name: Client identifier
            server_name: Server name
            command: Command to start the server
        """
        self.clients[name] = MCPClient(server_name, command)
        logger.info(f"Registered MCP client: {name}")

    async def connect_all(self) -> dict[str, bool]:
        """Connect all registered clients.
        
        Returns:
            Dictionary mapping client names to connection status
        """
        results = {}
        tasks = []
        
        for name, client in self.clients.items():
            tasks.append((name, client.connect()))
        
        for name, task in tasks:
            results[name] = await task
        
        return results

    async def disconnect_all(self) -> None:
        """Disconnect all clients."""
        tasks = [client.disconnect() for client in self.clients.values()]
        await asyncio.gather(*tasks)

    def get_client(self, name: str) -> Optional[MCPClient]:
        """Get a specific client.
        
        Args:
            name: Client identifier
            
        Returns:
            MCPClient instance or None
        """
        return self.clients.get(name)


# Global client manager instance
manager = MCPClientManager()
