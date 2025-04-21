from fastapi import APIRouter,Depends, HTTPException
from sqlmodel import select, Session
from app.models.ngo_service import NGOService
from app.database import get_session
from app.models.ngo_service import NGOService,NGOServiceCreate, NGOServiceRead, NGOServiceUpdate


router =APIRouter(prefix="/ngo_service",tags=["ngo_service"])

@router.post("/ngo_service/",response_model= NGOServiceRead)
def create_ngo_service(data:NGOServiceCreate, session:Session = Depends(get_session)):
    db_entry = NGOService(**data.dict())
    session.add(db_entry)
    session.commit()
    session.refresh(db_entry)
    return db_entry

@router.get("/ngo_service/",response_model=list[NGOServiceRead])
def get_all_ngo_service(session:Session =Depends(get_session)):
    return session.exec(select(NGOService)).all()

@router.get("/ngo_service/{entry_id}",response_model=NGOServiceRead)
def get_ngo_service(entry_id: int, session: Session = Depends(get_session)):
    entry = session.get(NGOService, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="NGO service not found")
    return entry

@router.patch("/ngo_service/{entry_id}",response_model=NGOServiceRead)
def update_ngo_service(entry_id: int, update_data: NGOServiceUpdate, session: Session = Depends(get_session)):
    entry = session.get(NGOService, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="NGO service not found")
    entry.sqlmodel_update(update_data.model_dump(exclude_unset=True))
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry

@router.delete("/ngo_service/{entry_id}")
def delete_ngo_service(entry_id: int, session: Session = Depends(get_session)):
    entry = session.get(NGOService, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="NGO service not found")
    session.delete(entry)
    session.commit()
    return {"ok":True}



