"""MCP search server for document search and retrieval."""

import asyncio
import logging
from typing import Any, Optional

from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ToolResult,
)

logger = logging.getLogger(__name__)


class SearchServer:
    """MCP server for search operations."""

    def __init__(self, vectorstore=None, document_store=None):
        """Initialize search server.
        
        Args:
            vectorstore: Vector store instance for similarity search
            document_store: Document store for document retrieval
        """
        self.vectorstore = vectorstore
        self.document_store = document_store
        self.server = Server("search-server")
        self._setup_tools()

    def _setup_tools(self) -> None:
        """Setup available search tools."""
        self.server.register_tool(
            Tool(
                name="semantic_search",
                description="Search documents using semantic similarity",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query",
                        },
                        "top_k": {
                            "type": "integer",
                            "description": "Number of results to return",
                            "default": 5,
                        },
                    },
                    "required": ["query"],
                },
            ),
            self.semantic_search,
        )

        self.server.register_tool(
            Tool(
                name="keyword_search",
                description="Search documents using keyword matching",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search keywords",
                        },
                        "top_k": {
                            "type": "integer",
                            "description": "Number of results to return",
                            "default": 5,
                        },
                    },
                    "required": ["query"],
                },
            ),
            self.keyword_search,
        )

        self.server.register_tool(
            Tool(
                name="get_document",
                description="Get full document by ID",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_id": {
                            "type": "string",
                            "description": "Document ID",
                        }
                    },
                    "required": ["doc_id"],
                },
            ),
            self.get_document,
        )

        self.server.register_tool(
            Tool(
                name="list_documents",
                description="List all available documents",
                inputSchema={
                    "type": "object",
                    "properties": {}
                },
            ),
            self.list_documents,
        )

    async def semantic_search(
        self, query: str, top_k: int = 5
    ) -> ToolResult:
        """Perform semantic search.
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            Search results
        """
        try:
            if not self.vectorstore:
                return ToolResult(
                    content=[TextContent(
                        type="text",
                        text="Vectorstore not configured"
                    )]
                )

            results = await self._semantic_search_impl(query, top_k)
            
            formatted_results = []
            for i, result in enumerate(results, 1):
                formatted_results.append(
                    f"{i}. {result.get('content', '')}\n"
                    f"   Score: {result.get('score', 0):.3f}\n"
                    f"   Source: {result.get('source', 'Unknown')}"
                )
            
            content = "\n".join(formatted_results) if formatted_results else "No results found"
            return ToolResult(
                content=[TextContent(type="text", text=content)]
            )
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return ToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")]
            )

    async def keyword_search(
        self, query: str, top_k: int = 5
    ) -> ToolResult:
        """Perform keyword search.
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            Search results
        """
        try:
            if not self.document_store:
                return ToolResult(
                    content=[TextContent(
                        type="text",
                        text="Document store not configured"
                    )]
                )

            results = await self._keyword_search_impl(query, top_k)
            
            formatted_results = []
            for i, result in enumerate(results, 1):
                formatted_results.append(
                    f"{i}. {result.get('content', '')}\n"
                    f"   Source: {result.get('source', 'Unknown')}"
                )
            
            content = "\n".join(formatted_results) if formatted_results else "No results found"
            return ToolResult(
                content=[TextContent(type="text", text=content)]
            )
        except Exception as e:
            logger.error(f"Error in keyword search: {e}")
            return ToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")]
            )

    async def get_document(self, doc_id: str) -> ToolResult:
        """Get a document by ID.
        
        Args:
            doc_id: Document ID
            
        Returns:
            Document content
        """
        try:
            if not self.document_store:
                return ToolResult(
                    content=[TextContent(
                        type="text",
                        text="Document store not configured"
                    )]
                )

            doc = await self._get_document_impl(doc_id)
            
            if not doc:
                return ToolResult(
                    content=[TextContent(
                        type="text",
                        text=f"Document not found: {doc_id}"
                    )]
                )
            
            return ToolResult(
                content=[TextContent(type="text", text=doc)]
            )
        except Exception as e:
            logger.error(f"Error getting document {doc_id}: {e}")
            return ToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")]
            )

    async def list_documents(self) -> ToolResult:
        """List all documents.
        
        Returns:
            List of document IDs
        """
        try:
            if not self.document_store:
                return ToolResult(
                    content=[TextContent(
                        type="text",
                        text="Document store not configured"
                    )]
                )

            docs = await self._list_documents_impl()
            
            content = "\n".join(f"  - {doc}" for doc in docs) if docs else "No documents found"
            return ToolResult(
                content=[TextContent(type="text", text=content)]
            )
        except Exception as e:
            logger.error(f"Error listing documents: {e}")
            return ToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")]
            )

    # Implementation methods - to be connected with actual vectorstore/docstore
    async def _semantic_search_impl(
        self, query: str, top_k: int
    ) -> list[dict]:
        """Perform actual semantic search.
        
        Args:
            query: Search query
            top_k: Number of results
            
        Returns:
            List of results
        """
        # Would be implemented with actual vectorstore
        return []

    async def _keyword_search_impl(
        self, query: str, top_k: int
    ) -> list[dict]:
        """Perform actual keyword search.
        
        Args:
            query: Search query
            top_k: Number of results
            
        Returns:
            List of results
        """
        # Would be implemented with actual document store
        return []

    async def _get_document_impl(self, doc_id: str) -> Optional[str]:
        """Get document by ID.
        
        Args:
            doc_id: Document ID
            
        Returns:
            Document content or None
        """
        # Would be implemented with actual document store
        return None

    async def _list_documents_impl(self) -> list[str]:
        """List all document IDs.
        
        Returns:
            List of document IDs
        """
        # Would be implemented with actual document store
        return []

    async def run(self, host: str = "localhost", port: int = 3002) -> None:
        """Run the server.
        
        Args:
            host: Server host
            port: Server port
        """
        logger.info(f"Starting search server on {host}:{port}")
        await asyncio.sleep(3600)  # Run for 1 hour


async def start_search_server(vectorstore=None, document_store=None) -> None:
    """Start the search server.
    
    Args:
        vectorstore: Vector store instance
        document_store: Document store instance
    """
    server = SearchServer(vectorstore, document_store)
    await server.run()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    asyncio.run(start_search_server())
