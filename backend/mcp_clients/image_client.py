import json
import logging
from typing import Dict, Any, Optional

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

logger = logging.getLogger(__name__)

class MCPImageClient:
    """MCP client for Flux image generation"""

    def __init__(self):
        self.url = "https://server.smithery.ai/@falahgs/flux-imagegen-mcp-server/mcp"

    async def connect(self):
        try:
            async with streamablehttp_client(self.url) as (read, write, _):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools = await session.list_tools()
                    logger.info(f"Image MCP connected, tools: {[t.name for t in tools.tools]}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect MCP Image server: {e}")
            return False

    async def generate_image(
        self,
        prompt: str,
        width: int,
        height: int,
        steps: int,
        guidance: float
    ) -> Dict[str, Any]:
        try:
            async with streamablehttp_client(self.url) as (read, write, _):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool(
                        "flux_imagegen",
                        arguments={
                            "prompt": prompt,
                            "width": width,
                            "height": height,
                            "steps": steps,
                            "guidance": guidance
                        }
                    )
                    if result.content and len(result.content) > 0:
                        return json.loads(result.content[0].text)
            logger.error("MCP returned no content")
            return {}
        except Exception as e:
            logger.error(f"MCP image generation failed: {e}")
            raise Exception(f"MCP image generation failed: {str(e)}")

    async def disconnect(self):
        # no persistent session anymore
        return
