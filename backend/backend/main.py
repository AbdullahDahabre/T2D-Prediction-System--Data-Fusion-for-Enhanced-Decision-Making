from fastapi import FastAPI, Depends, HTTPException, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import json
import numpy as np
import uvicorn
import openai
from routers.dashboard import router as dashboard_router  

# ───── Routers and Local Modules ─────
from routers.users import router as users_router
from predict_t2d import router as predict_t2d_router
from database import get_db, init_db
from schemas import (
    Token,
    UserOut,
    UserCreate,
    PredictionInput,
    ChatGptPredictionInput,
    ChatGptPredictionResponse,
)
from auth import authenticate_user, create_access_token, register_user
from models import User as DBUser
from database_utils import save_patient_data_and_prediction  

# ───── Load Environment Variables ─────
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_client = openai.OpenAI(api_key=openai_api_key)

# ───── FastAPI App Initialization ─────
app = FastAPI()

# ───── Enable CORS ─────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ───── Initialize Database ─────
init_db()

# ───── OAuth2 Token Setup ─────
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# ───── Auth Routes ─────
@app.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = register_user(user, db)
    return new_user

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    result = authenticate_user(db, form_data.username, form_data.password)
    if result == "email_not_found":
        raise HTTPException(status_code=401, detail="Email is not registered.")
    if result == "wrong_password":
        raise HTTPException(status_code=401, detail="Incorrect password.")
    user = result
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/user/me", response_model=UserOut)
def get_user_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from auth import get_current_user
    return get_current_user(token, db)

# ───── Include Routers ─────
app.include_router(users_router)
app.include_router(predict_t2d_router)
app.include_router(dashboard_router)  
# ───── Root Endpoint ─────
@app.get("/")
def read_root():
    return {"message": "Backend is running. Visit /docs for Swagger UI."}

# ───── OpenAI Chat Endpoint ─────
class ChatRequest(BaseModel):
    messages: list

@app.post("/chatapi")
async def chat_api(request: ChatRequest):
    try:
        system_prompt = {
            "role": "system",
            "content": (
                "You are ReemAI, a highly focused medical assistant trained exclusively to answer questions about "
                "Type 2 Diabetes (T2D). You must only respond to questions related to T2D, such as its causes, risk factors, "
                "symptoms, diagnosis, treatment options, medications, monitoring, prevention, lifestyle, or ongoing research. "
                "You must also respond to the message requiring you to generate a preventive lifesyle plan or a treatment plan based of some features, You can respond to greetings"
                "If the user asks a question that is not related to T2D, you must politely but firmly respond with: "
                "'I'm only able to help with Type 2 Diabetes-related questions. Please ask me something about T2D.'"
            )
        }
        full_messages = [system_prompt] + request.messages

        response = openai_client.chat.completions.create(
            model="ft:gpt-3.5-turbo-1106:personal:reemai-t2d-guardrails2:BUvwBF3G",
            messages=full_messages,
            max_tokens=300,
            temperature=0.7,
        )
        reply = response.choices[0].message.content.strip()
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ───── Save Result Endpoint ─────
class SaveResultRequest(BaseModel):
    formData: dict
    prediction: str
    confidence: float

@app.post("/save-result")
async def save_result(request: SaveResultRequest):
    try:
        save_patient_data_and_prediction(
            request.formData,
            request.prediction,
            request.confidence
        )
        return {"message": "Data saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ───── Run Locally ─────
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)