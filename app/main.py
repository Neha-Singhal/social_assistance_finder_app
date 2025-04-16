from fastapi import FastAPI
from .database import engine
from .import models

app = FastAPI()
#create tables
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Welcome to  Social Assistance Finder API"}