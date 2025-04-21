from typing import List
import service
from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import session
from sqlmodel import select, Session
from app.models.service import Service ,ServiceRead, ServiceCreate, ServiceUpdate
from app.database import get_session

router = APIRouter(prefix="/service" , tags=["Services"])



@router.post("/ServiceRead/", response_model=ServiceRead)
def create_service(service:ServiceCreate, session: Session = Depends(get_session)):
    db_service = Service(**service.dict())
    session.add(db_service)
    session.commit()
    session.refresh(db_service)
    return db_service

@router.get("/ServiceRead",response_model=list[ServiceRead])
def read_service(session: Session =Depends(get_session)):
    return session.exec(select(Service)).all()

@router.get("/ServiceRead/{service_id}",response_model=ServiceRead)
def read_service(service_id:int, session = Depends(get_session)):
    return  session.exec(select(service)).all()

@router.get("/service/{service_id}")
def update_service(service_id: int,service_update: ServiceUpdate,
    session: Session = Depends(get_session),
):
    service = session.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    service_data = service_update.model_dump(exclude_unset=True)
    service.sqlmodel_update(service_data)
    session.add(service)
    session.commit()
    session.refresh(service)
    return service

@router.delete("/service/{service_id}")
def delete_service(service_id: int, session: Session = Depends(get_session)):
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    session.delete(service)
    session.commit()
    return {"ok": True}





