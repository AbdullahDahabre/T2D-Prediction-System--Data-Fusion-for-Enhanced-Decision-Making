from fastapi import APIRouter, Request
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")  # store key in .env file

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant specialized in Type 2 Diabetes."},
                {"role": "user", "content": request.message}
            ],
            temperature=0.7,
            max_tokens=300,
        )
        reply = response.choices[0].message["content"].strip()
        return {"response": reply}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}