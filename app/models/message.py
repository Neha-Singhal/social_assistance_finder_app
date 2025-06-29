from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MessageCreate(BaseModel):
    receiver_id: int
    body: str


# This is the message class
class Message(SQLModel, table=True):
    __tablename__ = "messages"
    id: int = Field(default=None, primary_key=True)
    sender_id: int = Field(foreign_key="users.id")
    receiver_id: int = Field(foreign_key="users.id")
    body: str
    via: str = "whatsapp"
    timestamp: datetime = Field(default_factory=datetime.utcnow)