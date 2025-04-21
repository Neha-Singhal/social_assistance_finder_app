from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.database import get_session
from app.models.user import User, UserCreate, UserPublic
from app.auth.hashing import hash_password, verify_password

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter(tags=["Authentication"])


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/signup", response_model=UserPublic)
def signup(user: UserCreate, session: Session = Depends(get_session)):
    user_in_db = session.exec(select(User).where(User.email == user.email)).first()
    if user_in_db:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    new_user = User(**user.dict(exclude={"password"}), password=hashed_pw)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.post("/login")
def login(email: str, password: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}