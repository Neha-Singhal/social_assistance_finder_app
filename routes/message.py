from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from datetime import datetime

from app.database import get_session
from app.auth.auth import get_current_active_user, User
from app.models.message import Message, MessageCreate
from .send_whatsapp import send_whatsapp_message, MessageSchema
from app.utils.whatsapp_helper import send_whatsapp_message

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("/")
def send_message(
    message_data: MessageCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    if message_data.receiver_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot send a message to yourself")

    new_message = Message(
        sender_id=current_user.id,
        receiver_id=message_data.receiver_id,
        body=message_data.body,
        via="whatsapp",
        timestamp=datetime.utcnow()
    )

    session.add(new_message)
    session.commit()
    session.refresh(new_message)

    # Send WhatsApp message
    try:
        send_whatsapp_message(MessageSchema(
            to=str(new_message.receiver_id),  # Replace with phone lookup logic
            body=new_message.body
        ))
    except Exception as e:
        print("Failed to send WhatsApp message:", e)

    return new_message