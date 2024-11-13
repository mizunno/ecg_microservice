import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock
from datetime import datetime
from uuid import uuid4
from base64 import b64encode
from main import app
from adapters.api.schemas import ECGRequestSchema, LeadRequestSchema, LeadResponseSchema
from adapters.api.dependencies import get_ecg_service, get_auth_service
from adapters.database.models import User, UserRole

client = TestClient(app)


@pytest.fixture
def mock_ecg_service():
    mock_service = Mock()
    app.dependency_overrides[get_ecg_service] = lambda: mock_service
    yield mock_service
    app.dependency_overrides = {}


@pytest.fixture
def mock_auth_service():
    mock_service = Mock()
    app.dependency_overrides[get_auth_service] = lambda: mock_service
    yield mock_service
    app.dependency_overrides = {}


@pytest.fixture
def user_auth_headers():
    return {"Authorization": f"Basic {b64encode(b'testuser:password123').decode()}"}


@pytest.fixture
def admin_auth_headers():
    return {"Authorization": f"Basic {b64encode(b'admin:adminpass').decode()}"}


@pytest.fixture
def mock_user():
    return User(id=1, username="testuser", role=UserRole.USER)


@pytest.fixture
def mock_admin():
    return User(id=2, username="admin", role=UserRole.ADMIN)


def test_get_ecg_success(
    mock_ecg_service, mock_auth_service, mock_user, user_auth_headers
):
    # Prepare mock authentication
    mock_auth_service.authenticate_user.return_value = mock_user

    # Prepare mock ECG retrieval
    ecg_id = str(uuid4())
    mock_ecg_service.get.return_value = Mock(
        ecg_id=ecg_id,
        date=datetime.now(),
        user_id=mock_user.id,
        leads=[
            LeadResponseSchema(name="I", signal=[1, -1, 2, -2], num_samples=4),
            LeadResponseSchema(name="II", signal=[3, -3, 4, -4], num_samples=4),
        ],
    )

    response = client.get(f"/ecg/{ecg_id}", headers=user_auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["ecg_id"] == ecg_id
    assert len(data["leads"]) == 2


def test_get_ecg_unauthorized(mock_ecg_service):
    ecg_id = str(uuid4())
    response = client.get(f"/ecg/{ecg_id}")

    assert response.status_code == 401


def test_get_ecg_wrong_user(
    mock_ecg_service, mock_auth_service, mock_user, user_auth_headers
):
    # Prepare mock authentication
    mock_auth_service.authenticate_user.return_value = mock_user

    # Prepare mock ECG retrieval with different user_id
    ecg_id = str(uuid4())
    mock_ecg_service.get.return_value = Mock(
        ecg_id=ecg_id,
        date=datetime.now(),
        # Different user_id
        user_id=999,
        leads=[],
    )

    response = client.get(f"/ecg/{ecg_id}", headers=user_auth_headers)

    assert response.status_code == 404


def test_upload_ecg_success(
    mock_ecg_service, mock_auth_service, mock_user, user_auth_headers
):
    # Prepare mock authentication
    mock_auth_service.authenticate_user.return_value = mock_user

    ecg_id = str(uuid4())
    mock_ecg_service.process.return_value = ecg_id

    ecg_data = ECGRequestSchema(
        leads=[
            LeadRequestSchema(name="I", signal=[1, -1, 2, -2], num_samples=4),
            LeadRequestSchema(name="II", signal=[3, -3, 4, -4], num_samples=4),
        ]
    )

    response = client.post(
        "/ecg/", json=ecg_data.model_dump(), headers=user_auth_headers
    )

    assert response.status_code == 201
    assert response.json() == {"ecg_id": ecg_id}

    mock_ecg_service.process.assert_called_once_with(
        leads=[lead.model_dump() for lead in ecg_data.leads], user_id=mock_user.id
    )


def test_create_user_admin_success(mock_auth_service, mock_admin, admin_auth_headers):
    # Prepare mock authentication
    mock_auth_service.authenticate_user.return_value = mock_admin

    user = User(id=3, username="newuser", role=UserRole.USER)

    # Prepare mock user creation
    mock_auth_service.create_user.return_value = user

    response = client.post(
        "/users/",
        json={"username": user.username, "password": "password123"},
        headers=admin_auth_headers,
    )

    assert response.status_code == 201


def test_create_user_unauthorized(mock_auth_service, mock_user, user_auth_headers):
    # Prepare mock authentication with a normal user
    mock_auth_service.authenticate_user.return_value = mock_user

    response = client.post(
        "/users/",
        json={"username": "newuser", "password": "password123"},
        headers=user_auth_headers,
    )

    assert response.status_code == 403
