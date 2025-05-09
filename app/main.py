from fastapi import FastAPI
from app.database import create_db_and_tables, SessionDep
from app.auth import auth
from routes import user , ngo_type, service, ngo_service, support_request


app = FastAPI(
    title="Social Assistance Finder API",  # your project name
    description="An API to connect needy users with NGOs offering support services.",
    version="1.0.0",
    docs_url="/docs",
)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(ngo_type.router)
app.include_router(service.router)
app.include_router(ngo_service.router)
app.include_router(support_request.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()









