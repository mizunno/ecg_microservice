from fastapi import Depends, BackgroundTasks
from sqlalchemy.orm import Session
from adapters.database.repository import DatabaseECGRepository
from services.ecg_service import ECGService
from adapters.database.orm import get_db


def get_ecg_service(background_task: BackgroundTasks, db: Session = Depends(get_db)) -> ECGService:
    ecg_repository = DatabaseECGRepository(db)
    return ECGService(ecg_repository, background_task)
