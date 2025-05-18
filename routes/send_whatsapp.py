from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from twilio.rest import Client
import os
import requests
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Twilio setup
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
client = Client(account_sid, auth_token)

# Gemini setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1/models/{GEMINI_MODEL}:generateContent"


class MessageSchema(BaseModel):
    to: str
    body: str


class AIMessageRequest(BaseModel):
    to: str
    prompt: str  # The question or message for Gemini


def send_whatsapp_message(to: str, body: str) -> str:
    message = client.messages.create(
        body=body,
        from_="whatsapp:+14155238886",
        to=f"whatsapp:{to}"
    )
    return message.sid


@router.post("/send-whatsapp")
def send_message(payload: MessageSchema):
    try:
        sid = send_whatsapp_message(payload.to, payload.body)
        return {"status": "sent", "message_sid": sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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

