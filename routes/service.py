from typing import List
from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import session
from sqlmodel import select, Session
from app.models import service
from app.models.service import Service ,ServiceRead, ServiceCreate, ServiceUpdate
from app.database import get_session
from app.auth.auth import get_current_user
from app.models.support_request import SupportRequest, SupportRequestRead
from app.models.user import User

router = APIRouter(prefix="/services" , tags=["Services"])



@router.post("/ServiceRead", response_model=ServiceRead)
def create_service(service:ServiceCreate, session: Session = Depends(get_session)):
    db_service = Service(**service.dict())
    session.add(db_service)
    session.commit()
    session.refresh(db_service)
    return db_service

@router.get("/ServiceRead",response_model=list[ServiceRead])
def read_service(service_id: int,session: Session =Depends(get_session)):
    return session.exec(select(Service)).all()


@router.put("/service/{service_id}",response_model=ServiceRead)
def update_service(service_id: int,service_update: ServiceUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    service = session.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    service_data = service_update.model_dump(exclude_unset=True)
    for key, value in service_data.items():
        setattr(service, key, value)
    session.add(service)
    session.commit()
    session.refresh(service)
    return service


@router.delete("/service/{service_id}")
def delete_service(service_id: int,
                   session: Session = Depends(get_session),
                   current_user: User = Depends(get_current_user),
):
    service = session.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    session.delete(service)
    session.commit()
    return {"ok": True}



@router.get("/support/{request_id}", response_model=SupportRequestRead)
def get_support_request(request_id: int, session: Session = Depends(get_session)):
    request = session.get(SupportRequest, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Support request not found")
    return request




