from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from twilio.rest import Client
import os
import requests
from dotenv import load_dotenv
from sqlmodel import Session, select
from app.database import get_session
from app.models import User

load_dotenv()

router = APIRouter()

# Twilio setup
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")

if not all([account_sid, auth_token, whatsapp_number]):
    raise RuntimeError("Missing Twilio credentials in environment variables.")

client = Client(account_sid, auth_token)

# Gemini setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1/models/{GEMINI_MODEL}:generateContent"
if not GEMINI_API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY in environment variables.")

# -----Request Models------
class MessageSchema(BaseModel):
    to: str  # Could be a phone number or user email depending on implementation
    body: str

class AIMessageRequest(BaseModel):
    to: str  # Could be a user identifier
    prompt: str


# ----- Utilities -----
def send_whatsapp_message(to: str, body: str) -> str:
    if not to or not body:
        raise ValueError("Both 'to' and 'body' must be provided.")

    full_to = to if to.startswith("whatsapp:") else f"whatsapp:{to}"

    message = client.messages.create(
        body=body,
        from_=whatsapp_number,
        to=full_to
    )
    return message.sid


def ask_gemini(user_prompt: str) -> str:
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": user_prompt}
                ]
            }
        ]
    }

    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)

    if response.status_code == 200:
        try:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception:
            return "Sorry, Gemini returned an unexpected response."
    else:
        return f"Gemini error {response.status_code}: {response.text}"


# ----- Routes -----
@router.post("/send-whatsapp")
def send_message(payload: MessageSchema):
    try:
        sid = send_whatsapp_message(payload.to, payload.body)
        return {"status": "sent", "message_sid": sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


