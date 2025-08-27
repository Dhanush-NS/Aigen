# backend/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User
from backend.utils import create_access_token, hash_password, verify_password
from pydantic import BaseModel, EmailStr, Field

router = APIRouter()

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=80)
    email: EmailStr
    password: str = Field(..., min_length=6)

@router.post("/register", summary="Register a new user")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    # Check if email already exists
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username already exists
    if db.query(User).filter(User.username == req.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create new user - FIXED: using correct function name
    user = User(
        username=req.username, 
        email=req.email, 
        hashed_password=hash_password(req.password)  # Fixed: was get_hash_password
    )
    
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"message": "User registered successfully", "user_id": user.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Registration failed")

@router.post("/login", summary="Login user")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Find user by email (form_data.username contains email)
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(str(user.id))
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }