from fastapi import FastAPI
from adapters.api.ecg_router import router as ecg_router
from adapters.database.orm import engine
from adapters.database.models import Base


app = FastAPI()
app.include_router(ecg_router)

Base.metadata.create_all(bind=engine)
