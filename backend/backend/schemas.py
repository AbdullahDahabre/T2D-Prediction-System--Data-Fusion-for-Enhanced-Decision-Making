## Pydantic models

# schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    role: str | None = None

# 🔐 Used for user registration input
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "doctor"

# ✅ Used when reading user info (excluding password)
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        orm_mode = True

# 🔑 Used for login input
class LoginRequest(BaseModel):
    username: str
    password: str

# 🔁 Token response model
class Token(BaseModel):
    access_token: str
    token_type: str

# Used for /predict input
class PredictionInput(BaseModel):
    feature1: float
    feature2: float
    feature3: float

# 🔮 Used for ChatGPT-mediated predictions
class ChatGptPredictionInput(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    family_history: Optional[bool] = None
    glucose_level: Optional[float] = None
    blood_pressure: Optional[str] = None
    additional_notes: Optional[str] = None
    
# 🔄 ChatGPT prediction response
class ChatGptPredictionResponse(BaseModel):
    prediction: Any
    confidence: Optional[float] = None
    insights: str
    recommendations: Optional[List[str]] = None