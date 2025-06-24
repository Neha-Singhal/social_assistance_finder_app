import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.main import app
from app.database import engine


@pytest.fixture
def session():
    with Session(engine) as session:
        yield session

client = TestClient(app)

