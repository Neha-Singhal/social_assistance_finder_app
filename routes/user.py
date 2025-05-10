from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from typing import Annotated
from app.auth.auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, authenticate_user
from app.models.support_request import SupportRequest, SupportRequestRead
from app.models.user import User, UserCreate, UserPublic, UserUpdate
from app.database import get_session
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import Token
from app.auth.auth import get_password_hash, oauth2_scheme, get_current_user
from typing import List

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserPublic)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        name=user.name,
        password=hashed_password,
        user_type=user.user_type,
        location=user.location,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/", response_model=list[UserPublic])
def read_users(session: Session = Depends(get_session), offset: int = 0, limit: int = 100):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.get("/{user_id}", response_model=UserPublic)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserPublic)
def update_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_id: int,
    user: UserUpdate,
    session: Session = Depends(get_session)
):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db


@router.delete("/{user_id}",response_model=UserPublic)
def delete_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_id: int,
    session: Session = Depends(get_session)
):
    user_db = session.get(User, user_id)
    if not user_db:
         raise HTTPException(status_code=404, detail="User not found")
    session.delete(user_db)
    session.commit()
    return user_db


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session)
):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me/", response_model=UserPublic)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/support/{user_id}", response_model=list[SupportRequestRead])
def get_support_requests_by_user(user_id: int, session:Session = Depends(get_session)):
    return session.exec(
        select(SupportRequest).where(SupportRequest.user_id == user_id)
    ).all()


@router.get("/support/{user_id}/{ngo_id}",response_model=List[SupportRequestRead])
def get_user_support_request_for_ngo(user_id: int, ngo_id: int,
                                     session: Session = Depends(get_session)):
    return session.exec(
        select(SupportRequest).where(
            SupportRequest.user_id == user_id ,
            SupportRequest.ngo_id == ngo_id
        )
    ).all()
