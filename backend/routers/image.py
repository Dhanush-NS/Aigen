# backend/routers/image.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import HistoryItem
from backend.utils import decode_token, oauth2_scheme
from backend.mcp_clients import image_client, fallback_image_generation
from pydantic import BaseModel, Field
from typing import Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class ImageRequest(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=500, description="Text prompt for image generation")
    width: Optional[int] = Field(1024, ge=256, le=2048, description="Image width")
    height: Optional[int] = Field(1024, ge=256, le=2048, description="Image height") 
    steps: Optional[int] = Field(20, ge=10, le=50, description="Generation steps")
    guidance: Optional[float] = Field(7.5, ge=1.0, le=20.0, description="Guidance scale")

@router.post("", summary="Generate image using MCP Flux server")
async def generate_image(
    req: ImageRequest, 
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
):
    """
    Generate image using MCP Flux ImageGen server with fallback
    """
    user_id = int(decode_token(token))
    
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Image prompt cannot be empty")
    
    image_data = {}
    generation_method = "unknown"
    
    try:
        # Try MCP image generation first
        logger.info(f"Attempting MCP image generation for: {req.prompt[:50]}...")
        
        image_data = await image_client.generate_image(
            prompt=req.prompt,
            width=req.width,
            height=req.height,
            steps=req.steps,
            guidance=req.guidance
        )
        generation_method = "mcp"
        logger.info(f"MCP image generation successful")
        
    except Exception as e:
        logger.warning(f"MCP image generation failed: {e}, falling back to Pollinations")
        
        try:
            # Fallback to Pollinations API
            image_data = fallback_image_generation(req.prompt)
            generation_method = "fallback"
            logger.info(f"Fallback image generation successful")
            
        except Exception as fallback_error:
            logger.error(f"Both MCP and fallback image generation failed: {fallback_error}")
            raise HTTPException(
                status_code=500,
                detail="Image generation service temporarily unavailable"
            )
    
    # Normalize response format
    normalized_data = {
        "prompt": req.prompt,
        "image_url": image_data.get("image_url"),
        "image_data": image_data.get("image_data"),  # base64 if available
        "generation_method": generation_method,
        "metadata": {
            **image_data.get("metadata", {}),
            "generation_id": image_data.get("generation_id"),
            "requested_params": {
                "width": req.width,
                "height": req.height,
                "steps": req.steps,
                "guidance": req.guidance
            }
        }
    }
    
    # Validate that we got an image URL
    if not normalized_data["image_url"]:
        raise HTTPException(
            status_code=500,
            detail="Image generation completed but no image URL received"
        )
    
    # Save to database
    try:
        item = HistoryItem(
            item_type="image", 
            query=req.prompt, 
            data=normalized_data, 
            user_id=user_id
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        
        logger.info(f"Saved image history item {item.id}")
        
    except Exception as db_error:
        logger.error(f"Failed to save image history: {db_error}")
        # Don't fail the request if we can't save to DB
        db.rollback()
    
    return {
        "id": item.id if 'item' in locals() else None,
        "prompt": req.prompt,
        "image_url": normalized_data["image_url"],
        "generation_method": generation_method,
        "metadata": normalized_data["metadata"]
    }