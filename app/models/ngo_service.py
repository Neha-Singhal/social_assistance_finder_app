from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional


class NGOServiceBase(SQLModel):
    ngo_id : int
    service_id: int

class NGOService(NGOServiceBase, table=True):
    id : int = Field(default= None, primary_key= True)


class NGOServiceCreate(NGOServiceBase):
    pass


class NGOServiceRead(NGOServiceBase):
    id: int


class NGOServiceUpdate(NGOServiceBase):
    ngo_id : int | None = None
    service_id : int | None = None
