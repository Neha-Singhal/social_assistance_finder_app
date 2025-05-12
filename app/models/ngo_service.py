from sqlmodel import SQLModel, Field,Relationship, Session, create_engine, select
from typing import Optional,TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.service import Service


class NGOServiceBase(SQLModel):
    ngo_id : int = Field(foreign_key="user.id")
    service_id: int = Field(foreign_key="service.id")


class NGOService(NGOServiceBase, table=True):
    id : int = Field(default= None, primary_key= True)


class NGOServiceCreate(NGOServiceBase):
    pass


class NGOServiceRead(NGOServiceBase):
    id: int


class NGOServiceUpdate(NGOServiceBase):
    ngo_id : int | None = None
    service_id : int | None = None
