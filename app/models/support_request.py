from sqlmodel import SQLModel,Field, select, create_engine, Relationship
from typing import Optional,List,TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.user import User

class SupportRequestBase(SQLModel):
    user_id : int = Field(foreign_key="user.id")
    ngo_id : int = Field(foreign_key="user.id")
    comment: Optional[str] = None


class SupportRequest(SupportRequestBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user : Optional["User"] = Relationship(back_populates="support_requests")
    ngo : Optional["User"] = Relationship(back_populates= "assigned_requests")


class SupportRequestCreate(SupportRequestBase):
    pass


class SupportRequestRead(SupportRequestBase):
    id: int
    created_at: datetime
    updated_at: datetime


class SupportRequestUpdate(SQLModel):
    comment: Optional[str] = None
