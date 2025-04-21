from typing import List
from fastapi import APIRouter,Depends, HTTPException
from sqlmodel import select, Session
from app.database import get_session
from app.models.support_request import SupportRequest, SupportRequestRead, SupportRequestCreate, SupportRequestUpdate


router = APIRouter(prefix="/support-request", tags=["Support Requests"])


@router.post("/", response_model=SupportRequestRead)
def create_support_request(
    support_request: SupportRequestCreate, session: Session = Depends(get_session)
):
    new_request = SupportRequest(**support_request.dict())
    session.add(new_request)
    session.commit()
    session.refresh(new_request)
    return new_request


@router.get("/{request_id}", response_model=SupportRequestRead)
def get_support_request(request_id: int, session: Session = Depends(get_session)):
    request = session.get(SupportRequest, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Support request not found")
    return request


@router.patch("/{request_id}", response_model=SupportRequestRead)
def update_support_request(
    request_id: int,
    update_data: SupportRequestUpdate,
    session: Session = Depends(get_session),
):
    db_request = session.get(SupportRequest, request_id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Support request not found")
    update_fields = update_data.model_dump(exclude_unset=True)
    db_request.sqlmodel_update(update_fields)
    session.add(db_request)
    session.commit()
    session.refresh(db_request)
    return db_request


@router.delete("/{request_id}")
def delete_support_request(request_id: int, session: Session = Depends(get_session)):
    request = session.get(SupportRequest, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Support request not found")
    session.delete(request)
    session.commit()
    return {"ok": True}