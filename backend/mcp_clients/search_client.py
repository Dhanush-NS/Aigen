import json
import logging
from typing import List, Dict, Any, Optional

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

logger = logging.getLogger(__name__)

class MCPSearchClient:
    """MCP client for DuckDuckGo search over HTTP"""

    def __init__(self):
        self.url = "https://server.smithery.ai/@nickclyde/duckduckgo-mcp-server/mcp"

    async def connect(self):
        try:
            async with streamablehttp_client(self.url) as (read, write, _):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools = await session.list_tools()
                    logger.info(f"Search MCP connected, tools: {[t.name for t in tools.tools]}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect MCP HTTP server: {e}")
            return False

    async def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        try:
            async with streamablehttp_client(self.url) as (read, write, _):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool(
                        "duckduckgo_search",
                        arguments={"query": query, "max_results": max_results}
                    )
                    if result.content and len(result.content) > 0:
                        search_data = json.loads(result.content[0].text)
                        return search_data.get("results", [])
            return []
        except Exception as e:
            logger.error(f"MCP search failed: {e}")
            raise Exception(f"MCP search failed: {str(e)}")

    async def disconnect(self):
        # no persistent session anymore
        return
