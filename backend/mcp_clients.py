# import asyncio
# import json
# import logging
# from typing import List, Dict, Any, Optional
# from urllib.parse import urlencode

# from modelcontextprotocol import ClientSession
# from modelcontextprotocol.client.streamable_http import streamablehttp_client

# logger = logging.getLogger(__name__)

# class MCPSearchClient:
#     """MCP client for DuckDuckGo search over HTTP"""

#     def __init__(self, api_key: str):
#         self.session: Optional[ClientSession] = None
#         self.api_key = api_key
#         self.url = None

#     async def connect(self):
#         """Connect to DuckDuckGo MCP HTTP server"""
#         try:
#             base_url = "https://server.smithery.ai/@nickclyde/duckduckgo-mcp-server/mcp"
#             params = {"api_key": self.api_key}
#             self.url = f"{base_url}?{urlencode(params)}"

#             self.read, self.write, _ = await streamablehttp_client(self.url)
#             self.session = ClientSession(self.read, self.write)
#             await self.session.initialize()

#             logger.info("Connected to DuckDuckGo MCP HTTP server")
#             return True
#         except Exception as e:
#             logger.error(f"Failed to connect MCP HTTP server: {e}")
#             return False

#     async def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
#         """Perform DuckDuckGo search via MCP server"""
#         if not self.session:
#             if not await self.connect():
#                 raise Exception("Could not connect to DuckDuckGo MCP server")

#         try:
#             result = await self.session.call_tool(
#                 "duckduckgo_search",
#                 arguments={"query": query, "max_results": max_results}
#             )

#             if result.content and len(result.content) > 0:
#                 search_data = json.loads(result.content[0].text)
#                 return search_data.get("results", [])

#             return []
#         except Exception as e:
#             logger.error(f"MCP search failed: {e}")
#             raise Exception(f"MCP search failed: {str(e)}")

#     async def disconnect(self):
#         if self.session:
#             await self.session.close()
#             self.session = None


# # Singleton instance (use your real API key here)
# search_client = MCPSearchClient(api_key="e7d0355b-057f-4676-a1b1-f6599d221dc5")
