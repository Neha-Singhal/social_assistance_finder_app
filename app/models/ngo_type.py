from enum import Enum
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .user import User

class NGOCategory(str, Enum):
    Human_Rights_NGOs = "Human_Rights_NGOs"
    Environmental_NGOs = "Environmental_NGOs"
    Social_Welfare_NGOs = "Social_Welfare_NGOs"
    Development_NGOs = "Development_NGOs"
    Relief_and_Recovery_NGOs = "Relief_and_Recovery_NGOs"
    Advocacy_NGO = "Advocacy_NGO"

class NGOTypeBase(SQLModel):
    type: NGOCategory

class NGOType(NGOTypeBase, table=True):
    __tablename__ = "ngo_types"
    id: Optional[int] = Field(default=None, primary_key=True)
    ngo_id: int = Field(foreign_key="users.id", ondelete="CASCADE")
    type: NGOCategory
    ngo: Optional["User"] = Relationship(back_populates="ngo_type")

class NGOTypeCreate(NGOTypeBase):
    ngo_id: int

class NGOTypeRead(NGOTypeBase):
    id: int
    ngo_id: int

class NGOTypeUpdate(SQLModel):
    type: Optional[NGOCategory] = None