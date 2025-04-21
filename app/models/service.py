from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional



class ServiceBase(SQLModel):
    name: str


class Service(ServiceBase, table=True):
    id: int = Field(default=None, primary_key=True)


class ServiceCreate(ServiceBase):
    pass

class ServiceRead(ServiceBase):
    id: int

class ServiceUpdate(SQLModel):
    name: Optional[str] = None


