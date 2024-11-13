from fastapi import Depends, BackgroundTasks, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from adapters.database.repository import DatabaseECGRepository, DatabaseUserRepository
from services.ecg_service import ECGService
from services.auth_service import AuthService
from adapters.database.orm import get_db
from adapters.database.models import UserRole


security = HTTPBasic()


def get_ecg_service(
    background_task: BackgroundTasks, db: Session = Depends(get_db)
) -> ECGService:
    ecg_repository = DatabaseECGRepository(db)
    return ECGService(ecg_repository, background_task)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    user_repository = DatabaseUserRepository(db)
    return AuthService(user_repository)


def verify_admin(
    auth_service: AuthService = Depends(get_auth_service),
    credentials: HTTPBasicCredentials = Depends(security),
):
    user = auth_service.authenticate_user(credentials)
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required"
        )
    return user


def verify_user(
    auth_service: AuthService = Depends(get_auth_service),
    credentials: HTTPBasicCredentials = Depends(security),
):
    return auth_service.authenticate_user(credentials)
