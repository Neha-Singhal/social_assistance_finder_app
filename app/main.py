import auth
from fastapi import FastAPI
from app.database import create_db_and_tables, SessionDep
from routes import user , ngo_type, service, ngo_service, support_request
from app.auth import auth


app = FastAPI(title="Social Assistance Finder API")
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(ngo_type.router)
app.include_router(service.router)
app.include_router(ngo_service.router)
app.include_router(support_request.router)
@app.on_event("startup")
def on_startup():
    create_db_and_tables()









