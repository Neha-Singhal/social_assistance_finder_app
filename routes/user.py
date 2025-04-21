from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from app.models.user import User, UserCreate, UserPublic, UserUpdate
from app.database import get_session

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/users/", response_model=UserPublic)
def create_user(user: UserCreate, session: Session=Depends(get_session)):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/users/", response_model=list[UserPublic])
def read_users(
        session: Session = Depends(get_session),
        offset: int = 0,
        limit: int = 100,
):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


@router.get("/users/{user_id}", response_model=UserPublic)
def read_user(user_id: int, session: Session =Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@router.patch("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserUpdate, session: Session= Depends(get_session)):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db

@router.delete("/users/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok":True}


