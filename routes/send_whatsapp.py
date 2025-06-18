from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
router = APIRouter()

# ----- Environment Variables -----
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1/models/{GEMINI_MODEL}:generateContent"

TWILIO_ENABLED = all([account_sid, auth_token, whatsapp_number])
GEMINI_ENABLED = bool(GEMINI_API_KEY)


# ----- Request Models -----
class MessageSchema(BaseModel):
    to: str  # Could be a phone number or user email
    body: str


class AIMessageRequest(BaseModel):
    to: str
    prompt: str


# ----- Utilities -----
def send_whatsapp_message(to: str, body: str) -> str:
    if not TWILIO_ENABLED:
        raise RuntimeError("Twilio is not configured properly in environment variables.")
    if not to or not body:
        raise ValueError("Both 'to' and 'body' must be provided.")

    client = Client(account_sid, auth_token)
    full_to = to if to.startswith("whatsapp:") else f"whatsapp:{to}"

    message = client.messages.create(
        body=body,
        from_=whatsapp_number,
        to=full_to
    )
    return message.sid


def ask_gemini(user_prompt: str) -> str:
    if not GEMINI_ENABLED:
        return "Gemini is not configured."

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