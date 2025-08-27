from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any, List
from datetime import datetime

# Auth
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    email: EmailStr
    password: str = Field(min_length=6)

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Dashboard
class HistoryCreate(BaseModel):
    item_type: str  # "search" or "image"
    query: str
    data: Any

class HistoryOut(BaseModel):
    id: int
    item_type: str
    query: str
    data: Any
    created_at: datetime
    class Config:
        from_attributes = True

class HistoryList(BaseModel):
    items: List[HistoryOut]
