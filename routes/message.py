from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from datetime import datetime
from app.database import get_session
from app.auth.auth import get_current_active_user, User
from app.utils.whatsapp_helper import send_whatsapp_message
from app.models.message import Message, MessageCreate

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("/")
def send_message(
    message_data: MessageCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
):
    print("Incoming message data:", message_data)
    print("Current user (sender):", current_user.id)

    if message_data.receiver_id == current_user.id:
        raise HTTPException(status_code=400, detail="Receiver has no phone number on file")
    receiver = session.get(User, message_data.receiver_id)
    print("Fetched receiver:", receiver)

    if not receiver :
        raise HTTPException(status_code=404, detail="Receiver not found")
    if not receiver.phone_number:
        raise HTTPException(status_code=400, detail="Receiver has no phone number on file")

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

    try:

        print(f"Sending WhatsApp message to {receiver.phone_number}...")
        sid = send_whatsapp_message(
            to=receiver.phone_number,
            body=new_message.body
        )
        print("WhatsApp SID:", sid)

    except Exception as e:
        print("Failed to send WhatsApp message:", e)
        raise HTTPException(status_code=500, detail="Failed to send WhatsApp message.")

    return new_message