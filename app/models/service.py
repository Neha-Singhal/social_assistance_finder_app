from sqlmodel import SQLModel,Field,Relationship
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .user import User
    from .support_request import SupportRequest
    from .service import Service
    from .ngo_service import NGOService
    from .ngo_type import NGOType

class ServiceBase(SQLModel):
    name: str


class Service(ServiceBase, table=True):
    __tablename__ = "services"
    id: int = Field(default=None, primary_key=True)

    ngo_services: List["NGOService"] = Relationship(back_populates="service", cascade_delete=True)



class ServiceCreate(ServiceBase):
    pass

class ServiceRead(ServiceBase):
    id: int

class ServiceUpdate(SQLModel):
    name: Optional[str] = None


