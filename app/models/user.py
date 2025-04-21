from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime

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
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    password: str

class UserPublic(UserBase):
    id : int

class UserUpdate(UserBase):
    name: str | None = None
    location :str | None = None
    password : str | None = None


