from twilio.rest import Client
from app.utils.config import settings

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def send_whatsapp_message(to_number: str, body: str) -> str:
    full_to = to_number if to_number.startswith("whatsapp:") else f"whatsapp:{to_number}"
    message = client.messages.create(
        body=body,
        from_=settings.TWILIO_WHATSAPP_NUMBER,
        to=full_to
    )
    return message.sid