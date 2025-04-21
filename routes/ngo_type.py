from typing import List
from fastapi import APIRouter,Depends, HTTPException
from sqlmodel import select, Session
from app.models.ngo_type import NgoType , NGOCategory
from app.database import get_session

router = APIRouter(prefix="/ngo-types" , tags=["NGO Types"])


@router.post("/NgoType/", response_model=NgoType)
def create_ngo_type(ngo_type:NgoType, session: Session = Depends(get_session)):
    session.add(ngo_type)
    session.commit()
    session.refresh(ngo_type)
    return ngo_type


@router.get("/NgoType/")
def read_all_ngo_types(session: Session = Depends(get_session)):
    ngo_types = session.exec(select(NgoType)).all()
    return ngo_types


@router.get("/NgoType/{ngo_type_id}")
def read_ngo_type(ngo_type_id:int, session:Session = Depends(get_session)):
    ngo_type = session.get(NgoType, ngo_type_id)
    if not ngo_type:
        raise HTTPException(status_code=404, detail="NGO Type not found")
    return ngo_type

@router.delete("/NgoType/{ngo_type_id}")
def delete_ngo_type(ngo_type_id: int, session:Session = Depends(get_session)):
    ngo_type = session.get(NgoType, ngo_type_id)
    if not ngo_type:
        raise HTTPException(status_code=404, detail="NGO Type not found")
    session.delete(ngo_type)
    session.commit()
    return {"ok": True}



