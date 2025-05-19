from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from datetime import datetime

if TYPE_CHECKING:
    from .support_request import SupportRequest
    from .ngo_service import NGOService
    from .ngo_type import NGOType

class UserType(str, Enum):
    user = "user"
    ngo = "ngo"

class UserBase(SQLModel):
    name: str = Field(index=True)
    email: Optional[str] = Field(default=None, index=True, unique=True)
    location: str
    user_type: UserType
    phone_number: Optional[str] = Field(default=None)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Support requests created by user
    support_requests: List["SupportRequest"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "foreign_keys": "[SupportRequest.user_id]"}
    )

    # Support requests assigned to NGO
    assigned_requests: List["SupportRequest"] = Relationship(
        back_populates="ngo",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "foreign_keys": "[SupportRequest.ngo_id]"}
    )

    # Services offered by this NGO
    ngo_services: List["NGOService"] = Relationship(
        back_populates="ngo",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "foreign_keys": "[NGOService.ngo_id]"}
    )

    ngo_type: Optional["NGOType"] = Relationship(
        back_populates="ngo",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "primaryjoin": "User.id==foreign(NGOType.ngo_id)",
            "uselist": False
        }
    )



# --- SCHEMA MODELS ---

class UserCreate(UserBase):
    password: str

class UserPublic(UserBase):
    id: int

class UserUpdate(UserBase):
    name: Optional[str] = None
    location: Optional[str] = None
    password: Optional[str] = None

# --- AUTH ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None