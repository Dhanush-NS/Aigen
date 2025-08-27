from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import HistoryItem
from backend.utils import decode_token, oauth2_scheme
from backend.mcp_clients import search_client, fallback_search
import asyncio
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("", summary="Search the web using MCP DuckDuckGo server")
async def search(
    q: str, 
    max_results: int = 5,
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
):
    """
    Perform web search using MCP DuckDuckGo server with fallback
    """
    user_id = int(decode_token(token))
    
    if not q.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
    
    results = []
    search_method = "unknown"
    
    try:
        # Try MCP search first
        logger.info(f"Attempting MCP search for: {q}")
        results = await search_client.search(q, max_results)
        search_method = "mcp"
        logger.info(f"MCP search successful, got {len(results)} results")
        
    except Exception as e:
        logger.warning(f"MCP search failed: {e}, falling back to direct search")
        
        try:
            # Fallback to direct DuckDuckGo search
            results = fallback_search(q, max_results)
            search_method = "fallback"
            logger.info(f"Fallback search successful, got {len(results)} results")
            
        except Exception as fallback_error:
            logger.error(f"Both MCP and fallback search failed: {fallback_error}")
            raise HTTPException(
                status_code=500, 
                detail="Search service temporarily unavailable"
            )
    
    # Normalize results format
    normalized_results = []
    for r in results:
        normalized_results.append({
            "title": r.get("title", "No title"),
            "body": r.get("body", r.get("snippet", "No description")),
            "href": r.get("href", r.get("url", "#"))
        })
    
    # Save to database
    try:
        payload = {
            "results": normalized_results,
            "search_method": search_method,
            "query_metadata": {
                "max_results": max_results,
                "results_count": len(normalized_results)
            }
        }
        
        item = HistoryItem(
            item_type="search", 
            query=q, 
            data=payload, 
            user_id=user_id
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        
        logger.info(f"Saved search history item {item.id}")
        
    except Exception as db_error:
        logger.error(f"Failed to save search history: {db_error}")
        # Don't fail the request if we can't save to DB
        db.rollback()
    
    return {
        "id": item.id if 'item' in locals() else None,
        "query": q,
        "results": normalized_results,
        "search_method": search_method,
        "total_results": len(normalized_results)
    }