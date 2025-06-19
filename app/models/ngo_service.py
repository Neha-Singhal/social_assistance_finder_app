from sqlmodel import SQLModel, Field,Relationship, Session, create_engine, select
from typing import TYPE_CHECKING,Optional,List
if TYPE_CHECKING:
    from .user import User
    from .support_request import SupportRequest
    from .service import Service
    from .ngo_service import NGOService
    from .ngo_type import NGOType

class NGOServiceBase(SQLModel):
    ngo_id : int = Field(foreign_key="user.id", ondelete="CASCADE")
    service_id: int = Field(foreign_key="services.id", ondelete="CASCADE")



class NGOService(NGOServiceBase, table=True):
    __tablename__ = "ngo_services"
    id : int = Field(default= None, primary_key= True)

    ngo: "User" = Relationship(
        back_populates="ngo_services",
        sa_relationship_kwargs={"foreign_keys": "[NGOService.ngo_id]"}

    )

    service: "Service" = Relationship(back_populates="ngo_services")



class NGOServiceCreate(NGOServiceBase):
    pass


class NGOServiceRead(NGOServiceBase):
    id: int


class NGOServiceUpdate(NGOServiceBase):
    ngo_id : int | None = None
    service_id : int | None = None
