from sqlmodel import SQLModel,Field, select, create_engine
from typing import Optional
from datetime import datetime


class SupportRequestBase(SQLModel):
    user_id : int = Field(foreign_key="user.id")
    ngo_id : int = Field(foreign_key="user.id")
    comment: Optional[str] = None


class SupportRequest(SupportRequestBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class SupportRequestCreate(SupportRequestBase):
    pass


class SupportRequestRead(SupportRequestBase):
    id: int
    created_at: datetime
    updated_at: datetime


class SupportRequestUpdate(SQLModel):
    comment: Optional[str] = None
