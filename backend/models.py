from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="user")
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship("HistoryItem", back_populates="owner", cascade="all,delete-orphan")

class HistoryItem(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    item_type = Column(String(20), nullable=False)  # "search" | "image"
    query = Column(Text, nullable=False)
    data = Column(JSON, nullable=False)             # normalized payload
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="items")
