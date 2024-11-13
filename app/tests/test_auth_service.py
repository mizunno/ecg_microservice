import pytest
from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials
from adapters.database.repository import UserRepository
from services.auth_service import AuthService
from adapters.database.models import UserRole


class MockUserRepository(UserRepository):
    """
    Mock implementation of User repository
    that stores users in a dictionary
    """

    def __init__(self):
        self.users = {}

    def save(self, user):
        self.users[user.username] = user
        return user

    def get(self, username):
        return self.users.get(username)


@pytest.fixture
def user_repository():
    return MockUserRepository()


@pytest.fixture
def auth_service(user_repository):
    return AuthService(user_repository)


@pytest.fixture
def test_user(auth_service):
    """Create a test user and store in repository"""
    return auth_service.create_user(
        username="testuser", password="password123", role=UserRole.USER
    )


@pytest.fixture
def test_admin(auth_service):
    """Create a test admin and store in repository"""
    return auth_service.create_user(
        username="admin", password="adminpass", role=UserRole.ADMIN
    )


def test_create_user_success(auth_service):
    username = "newuser"
    password = "password123"

    user = auth_service.create_user(username, password)

    assert user.username == username
    assert user.role == UserRole.USER
    assert auth_service.verify_password(password, user.hashed_password)


def test_create_user_duplicate_username(auth_service, test_user):
    with pytest.raises(HTTPException) as exc_info:
        auth_service.create_user(test_user.username, "newpassword")

    assert exc_info.value.status_code == 400
    assert "Username already registered" in str(exc_info.value.detail)


def test_create_admin_user(auth_service):
    username = "newadmin"
    password = "adminpass"

    admin = auth_service.create_user(
        username=username, password=password, role=UserRole.ADMIN
    )

    assert admin.username == username
    assert admin.role == UserRole.ADMIN
    assert auth_service.verify_password(password, admin.hashed_password)


def test_authenticate_user_success(auth_service, test_user):
    credentials = HTTPBasicCredentials(
        username=test_user.username, password="password123"
    )

    authenticated_user = auth_service.authenticate_user(credentials)

    assert authenticated_user.username == test_user.username
    assert authenticated_user.role == test_user.role


def test_authenticate_user_wrong_password(auth_service, test_user):
    credentials = HTTPBasicCredentials(
        username=test_user.username, password="wrongpassword"
    )

    with pytest.raises(HTTPException) as exc_info:
        auth_service.authenticate_user(credentials)

    assert exc_info.value.status_code == 401
    assert "Invalid credentials" in str(exc_info.value.detail)


def test_authenticate_nonexistent_user(auth_service):
    credentials = HTTPBasicCredentials(username="nonexistent", password="password123")

    with pytest.raises(HTTPException) as exc_info:
        auth_service.authenticate_user(credentials)

    assert exc_info.value.status_code == 401
    assert "Invalid credentials" in str(exc_info.value.detail)


def test_get_user(auth_service, test_user):
    user = auth_service.get_user(test_user.username)
    assert user.username == test_user.username
    assert user.role == test_user.role


def test_get_nonexistent_user(auth_service):
    user = auth_service.get_user("nonexistent")
    assert user is None


def test_verify_password(auth_service):
    password = "testpassword"
    hashed = auth_service.get_password_hash(password)

    assert auth_service.verify_password(password, hashed)
    assert not auth_service.verify_password("wrongpassword", hashed)
