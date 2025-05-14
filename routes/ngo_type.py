from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from app.models.ngo_service import NGOService
from app.models.ngo_type import NGOType, NGOTypeRead, NGOTypeUpdate
from app.database import get_session
from app.auth.auth import get_current_user
from app.models.service import  Service,ServiceRead
from app.models.user import User

router = APIRouter(prefix="/ngo-types", tags=["NGO Types"])


@router.post("/", response_model=NGOTypeRead)
def create_ngo_type(
    ngo_type: NGOType,
    session: Session = Depends(get_session),
):
    new_ngo_type = NGOType(**ngo_type.dict())
    session.add(new_ngo_type)
    session.commit()
    session.refresh(new_ngo_type)
    return new_ngo_type


@router.get("/", response_model=List[NGOTypeRead])
def read_all_ngo_types(session: Session = Depends(get_session)):
    ngo_types = session.exec(select(NGOType)).all()
    return ngo_types


@router.get("/{ngo_type_id}", response_model=NGOTypeRead)
def read_ngo_type(ngo_type_id: int, session: Session = Depends(get_session)):
    ngo_type = session.get(NGOType, ngo_type_id)
    if not ngo_type:
        raise HTTPException(status_code=404, detail="NGO Type not found")
    return ngo_type


@router.patch("/{ngo_type_id}", response_model=NGOTypeRead)
def update_ngo_type(
    ngo_type_id: int,
    ngo_type_update: NGOTypeUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    ngo_type = session.get(NGOType, ngo_type_id)
    if not ngo_type:
        raise HTTPException(status_code=404, detail="NGO Type not found")
    update_data = ngo_type_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(ngo_type, key, value)

    session.add(ngo_type)
    session.commit()
    session.refresh(ngo_type)

    return ngo_type


@router.delete("/{ngo_type_id}")
def delete_ngo_type(
    ngo_type_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    ngo_type = session.get(NGOType, ngo_type_id)
    if not ngo_type:
        raise HTTPException(status_code=404, detail="NGO Type not found")
    session.delete(ngo_type)
    session.commit()
    return {"ok": True}


