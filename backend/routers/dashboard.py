from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import HistoryItem
from backend.utils import decode_token, oauth2_scheme
from typing import Optional, List

router = APIRouter()

@router.get("", summary="List saved items (search + image)")
def list_items(
    item_type: Optional[str] = Query(None, description="search|image"),
    q: Optional[str] = Query(None, description="filter by keyword"),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    user_id = int(decode_token(token))
    qry = db.query(HistoryItem).filter(HistoryItem.user_id == user_id)
    if item_type:
        qry = qry.filter(HistoryItem.item_type == item_type)
    if q:
        qry = qry.filter(HistoryItem.query.ilike(f"%{q}%"))
    items = qry.order_by(HistoryItem.created_at.desc()).all()
    return {"items": items}

@router.delete("/{item_id}", summary="Delete an item")
def delete_item(item_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user_id = int(decode_token(token))
    item = db.query(HistoryItem).filter(HistoryItem.id == item_id, HistoryItem.user_id == user_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item); db.commit()
    return {"ok": True}
