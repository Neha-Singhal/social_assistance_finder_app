from typing import List
from click import prompt
from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.sql.functions import current_user
from sqlmodel import select, Session
from app.auth.auth import User, get_current_active_user
from app.database import get_session
from app.models.support_request import SupportRequest, SupportRequestRead, SupportRequestCreate, SupportRequestUpdate
from app.gemini_helper import ask_gemini


router = APIRouter(prefix="/support-request", tags=["Support Requests"])


@router.get("/recommend-support")
def recommend_service():
    prompt = "Suggest mental health support NGOs in Berlin."
    recommendation = ask_gemini(prompt)
    return {"recommendation": recommendation}


@router.post("/", response_model=SupportRequestRead)
def create_support_request(
    support_request: SupportRequestCreate,
        session: Session = Depends(get_session),
        current_user: User = Depends(get_current_active_user),
):
    prompt = f"A user needs support. Comment: {support_request.comment or 'No comment provided.'}"
    gemini_response = ask_gemini(prompt)

    new_request = SupportRequest(**support_request.dict(),
                   gemini_response = gemini_response,
                   created_by=current_user.id)

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
    current_user:User = Depends(get_current_active_user),
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
def delete_support_request(request_id: int,
                           session: Session = Depends(get_session),
                           current_user: User = Depends(get_current_active_user),
):
    request = session.get(SupportRequest, request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Support request not found")
    if request. user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this request")
    session.delete(request)
    session.commit()
    return {"message":" Request deleted successfully"}

