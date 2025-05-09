from typing import List
from fastapi import APIRouter,Depends, HTTPException
from sqlmodel import select, Session
from app.models.ngo_service import NGOService
from app.database import get_session
from app.models.ngo_service import NGOService,NGOServiceCreate, NGOServiceRead, NGOServiceUpdate
from app.auth.auth import get_current_user
from app.models.user import User

router =APIRouter(prefix="/ngo_service",tags=["ngo_service"])

@router.post("/",response_model= NGOServiceRead)
def create_ngo_service(data:NGOServiceCreate,
                       session:Session = Depends(get_session),
                       current_user: User = Depends(get_current_user),
):
    db_entry = NGOService(**data.dict())
    session.add(db_entry)
    session.commit()
    session.refresh(db_entry)
    return db_entry


@router.get("/",response_model=list[NGOServiceRead])
def get_all_ngo_service(session:Session =Depends(get_session)):
    return session.exec(select(NGOService)).all()


@router.get("/{entry_id}",response_model=NGOServiceRead)
def get_ngo_service(entry_id: int, session: Session = Depends(get_session)):
    entry = session.get(NGOService, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="NGO service not found")
    return entry


@router.patch("/{entry_id}",response_model=NGOServiceRead)
def update_ngo_service(entry_id: int, update_data: NGOServiceUpdate,
                       session: Session = Depends(get_session),
                       current_user: User = Depends(get_current_user),
):
    entry = session.get(NGOService, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="NGO service not found")
    """Only the owner NGO can update"""
    if entry.ngo_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this entry.")

    entry.sqlmodel_update(update_data.model_dump(exclude_unset=True))
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry


@router.delete("/{entry_id}")
def delete_ngo_service(entry_id: int,
                       session: Session = Depends(get_session),
                       current_user: User = Depends(get_current_user),
):
    entry = session.get(NGOService, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="NGO service not found")
    if entry.ngo_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this entry.")

    session.delete(entry)
    session.commit()
    return {"ok":True}


@router.get("/by_service/{service_id}", response_model=List[NGOServiceRead])
def get_ngos_by_services(service_id: int,session: Session = Depends(get_session)):
    return session.exec(select(NGOService).where(NGOService.service_id == service_id )).all()



