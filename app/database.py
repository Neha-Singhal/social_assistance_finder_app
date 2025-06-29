from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, Session

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

#create db
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


