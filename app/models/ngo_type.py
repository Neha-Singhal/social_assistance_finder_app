from enum import Enum
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional


class NGOCategory(str, Enum):
    Human_Rights_NGOs = "Human_Rights_NGOs"
    Environmental_NGOs = "Environmental_NGOs"
    Social_Welfare_NGOs = "Social_Welfare_NGOs"
    Development_NGOs = "Development_NGOs"
    Relief_and_Recovery_NGOs = "Relief_and_Recovery_NGOs"
    Advocacy_NGO = "Advocacy_NGO"


class NGOTypeBase(SQLModel):
    ngo_id : int
    type : NGOCategory


class NgoType(NGOTypeBase, table=True):
    id: int = Field(default=None, primary_key=True)
    ngo_id: int = Field(foreign_key="user.id")
    type: NGOCategory

class NGOTypeCreate(NGOTypeBase):
    pass


class NGOTypeRead(NGOTypeBase):
    id: int


class NGOTypeUpdate(SQLModel):
    type: Optional[NGOCategory] = None


