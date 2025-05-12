from sqlmodel import SQLModel,Field,Relationship
from typing import Optional, List,TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.ngo_service import NGOService


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


