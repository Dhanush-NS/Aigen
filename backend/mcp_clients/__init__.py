import logging
from .search_client import MCPSearchClient
from .image_client import MCPImageClient
from .fallbacks import fallback_search, fallback_image_generation

logger = logging.getLogger(__name__)

# No API keys required
search_client: MCPSearchClient = MCPSearchClient()
image_client: MCPImageClient = MCPImageClient()

async def init_mcp_clients() -> bool:
    ok = True
    try:
        await search_client.connect()
        logger.info("Search MCP client connected")
    except Exception as e:
        logger.error(f"Search MCP client failed: {e}")
        ok = False

    try:
        await image_client.connect()
        logger.info("Image MCP client connected")
    except Exception as e:
        logger.error(f"Image MCP client failed: {e}")
        ok = False
    return ok

async def cleanup_mcp_clients():
    # Nothing to disconnect, since sessions are per-request
    return
