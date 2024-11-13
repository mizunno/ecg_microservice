from fastapi import APIRouter, Depends, status
from adapters.api.schemas import UserCreate
from adapters.api.dependencies import get_auth_service, verify_admin
from adapters.database.models import User
from services.auth_service import AuthService


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    admin: User = Depends(verify_admin),
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Only admins can create new users
    """

    user = auth_service.create_user(user_data.username, user_data.password)
    return {
        "message": f"User {user.username} with role {user.role} created successfully"
    }
