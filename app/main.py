from fastapi import FastAPI
from adapters.api.ecg_router import router as ecg_router


app = FastAPI()
app.include_router(ecg_router)
