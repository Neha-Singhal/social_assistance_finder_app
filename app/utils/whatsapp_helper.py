from twilio.rest import Client
from app.utils.config import settings

# Initialize Twilio client with credentials from settings
client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def send_whatsapp_message(to_number: str, body: str) -> str:
    """
    Sends a WhatsApp message using Twilio.

    Args:
        to_number (str): The recipient's phone number, with or without 'whatsapp:' prefix.
        body (str): The text message to send.

    Returns:
        str: The Twilio message SID.
    """
    if not to_number or not body:
        raise ValueError("Both 'to_number' and 'body' must be provided.")

    full_to = to_number if to_number.startswith("whatsapp:") else f"whatsapp:{to_number}"

    message = client.messages.create(
        body=body,
        from_=settings.TWILIO_WHATSAPP_NUMBER,
        to=full_to
    )
    return message.sid