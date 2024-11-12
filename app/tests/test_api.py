import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock
from datetime import datetime
from uuid import uuid4
from main import app
from adapters.api.schemas import ECGRequestSchema, LeadSchema
from adapters.api.dependencies import get_ecg_service

# Create the FastAPI test client
client = TestClient(app)


@pytest.fixture
def mock_ecg_service():
    mock_service = Mock()
    app.dependency_overrides[get_ecg_service] = lambda: mock_service
    yield mock_service
    app.dependency_overrides = {}


def test_get_ecg_success(mock_ecg_service):
    # Prepare the ECGService mock response and request data
    ecg_id = str(uuid4())
    mock_ecg_service.get.return_value = Mock(
        ecg_id=ecg_id,
        date=datetime.now(),
        leads=[
            LeadSchema(name="I", signal=[1, -1, 2, -2], num_samples=4),
            LeadSchema(name="II", signal=[3, -3, 4, -4], num_samples=4)
        ]
    )

    # Simulate a GET request to the /ecg/{ecg_id} endpoint
    response = client.get(f"/ecg/{ecg_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["ecg_id"] == ecg_id
    assert len(data["leads"]) == 2
    assert data["leads"][0]["name"] == "I"
    assert data["leads"][0]["signal"] == [1, -1, 2, -2]
    assert data["leads"][0]["num_samples"] == 4


def test_get_ecg_not_found(mock_ecg_service):
    # Prepare the ECGService mock to return None
    mock_ecg_service.get.return_value = None
    ecg_id = str(uuid4())

    # Simulate a GET request to the /ecg/{ecg_id} endpoint
    response = client.get(f"/ecg/{ecg_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "ECG not found"}


def test_get_ecg_insights_success(mock_ecg_service):
    # Prepare the ECGService mock response and request data
    ecg_id = str(uuid4())
    mock_ecg_service.get.return_value = Mock(
        ecg_id=ecg_id,
        date=datetime.now(),
        leads=[
            LeadSchema(name="I", signal=[1, -1, 2, -2],
                       num_samples=4, zero_crossings=3),
            LeadSchema(name="II", signal=[
                       3, -3, 4, -4], num_samples=4, zero_crossings=3)
        ]
    )

    # Simulate a GET request to the /ecg/{ecg_id} endpoint
    response = client.get(f"/ecg/{ecg_id}/insights")

    assert response.status_code == 200
    data = response.json()
    assert len(data["leads"]) == 2
    assert data["leads"][0]["name"] == "I"
    assert data["leads"][0]["zero_crossings"] == 3
    assert data["leads"][1]["name"] == "II"
    assert data["leads"][1]["zero_crossings"] == 3


def test_upload_ecg_success(mock_ecg_service):
    # Prepare the ECGService mock to return an ECG ID
    ecg_id = str(uuid4())
    mock_ecg_service.process.return_value = ecg_id
    ecg_data = ECGRequestSchema(
        leads=[
            LeadSchema(name="I", signal=[1, -1, 2, -2], num_samples=4),
            LeadSchema(name="II", signal=[3, -3, 4, -4], num_samples=4)
        ]
    )

    # Simulate a POST request to the /ecg/ endpoint
    response = client.post("/ecg/", json=ecg_data.model_dump())

    assert response.status_code == 201
    assert response.json() == {"ecg_id": ecg_id}


def test_upload_ecg_failure(mock_ecg_service):
    # Prepare the ECGService mock to raise an exception
    mock_ecg_service.process.side_effect = Exception("Test exception")
    ecg_data = ECGRequestSchema(
        leads=[
            LeadSchema(name="I", signal=[1, -1, 2, -2], num_samples=4),
            LeadSchema(name="II", signal=[3, -3, 4, -4], num_samples=4)
        ]
    )

    # Simulate a POST request to the /ecg/ endpoint
    response = client.post("/ecg/", json=ecg_data.model_dump())

    assert response.status_code == 500
    assert response.json() == {"detail": "Failed to upload ECG data"}
