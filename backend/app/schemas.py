from pydantic import BaseModel, EmailStr
from typing import Optional, List

# ----- USER SCHEMAS -----

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # plaintext; will be hashed before storing
    role: str  # "doctor" or "admin"

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    model_config = {
        "from_attributes": True
    }

# ----- AUTH -----

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

# ----- PATIENT SCHEMAS -----

class PatientCreate(BaseModel):
    name: str
    gender: str
    dob: str  # consider using date type in future

class PatientOut(PatientCreate):
    id: int

    model_config = {
        "from_attributes": True
    }

# ----- PREDICTION SCHEMAS -----

class PredictionCreate(BaseModel):
    patient_name: str
    glucose: float
    bmi: float
    age: int
    patient_id: int

class PredictionOut(PredictionCreate):
    id: int
    result: str
    confidence: float
    created_by_id: int

    model_config = {
        "from_attributes": True
    }

class VitalsCreate(BaseModel):
    patient_id: int
    heart_rate: int
    temperature: float
    steps: int
    timestamp: str  # or datetime, but string is fine for now

class VitalsOut(VitalsCreate):
    id: int

    model_config = {
        "from_attributes": True
    }
