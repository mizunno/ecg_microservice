from fastapi import FastAPI
from adapters.api.ecg_router import router as ecg_router
from adapters.api.user_router import router as user_router
from adapters.database.orm import engine, create_admin_user
from adapters.database.models import Base
from core.config import config

app = FastAPI()
app.include_router(ecg_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)
create_admin_user()
