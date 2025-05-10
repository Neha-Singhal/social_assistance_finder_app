from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List,TYPE_CHECKING
from enum import Enum
from datetime import datetime

if TYPE_CHECKING:
    from app.models.ngo_service import NGOService
    from app.models.support_request import SupportRequest


class UserType(str, Enum):
    user = "user"
    ngo = "ngo"

class UserBase(SQLModel):
    name: str = Field(index=True)
    email: Optional[str] = Field(default=None, index=True, unique=True)
    location: str
    user_type: UserType

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password : str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    support_requests: List["SupportRequest"] = Relationship(back_populates="user",sa_relationship_kwargs={"foreign_keys": "[SupportRequest.user_id]"}
)
    assigned_requests : List["SupportRequest"] =Relationship(back_populates="ngo",sa_relationship_kwargs={"foreign_keys": "[SupportRequest.ngo_id]"}
)
    ngo_services: List["NGOService"] = Relationship(back_populates="ngo")
    ngo_types: List["NgoType"]=Relationship(back_populates="ngo")


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id : int


class UserUpdate(UserBase):
    name: str | None = None
    location :str | None = None
    password : str | None = None



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None



