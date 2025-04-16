from sqlalchemy import Column, INTEGER, String, Enum, DateTime
from datetime import datetime
from .database import Base
import enum

class UserType(enum.Enum):
    user = "user"
    ngo = "ngo"

class User(Base):
    __tablename__ = "users"

    id = Column(INTEGER, primary_key=True, index=True)
    name= Column(String)
    email = Column(String, unique=True)
    password  = Column(String)
    location = Column(String)
    user_type = Column(Enum(UserType))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



