import pytest
from adapters.database.repository import ECGRepository
from services.ecg_service import ECGService


class MockECGRepository(ECGRepository):

    """
    Mock implementation of ECG repository that
    stores ECGs in memory
    """

    def __init__(self):
        self.ecgs = {}

    def save(self, ecg):
        self.ecgs[ecg.ecg_id] = ecg

    def get(self, uuid):
        return self.ecgs.get(uuid)


@pytest.fixture
def mock_ecg_repository():
    return MockECGRepository()


@pytest.fixture
def ecg_service(mock_ecg_repository):
    return ECGService(mock_ecg_repository)


def test_ecg_service_process(ecg_service):
    leads = [
        {"name": "I", "signal": [1, 2, 3]},
        {"name": "II", "signal": [4, 5, 6], "num_samples": 3},
    ]

    ecg_id = ecg_service.process(leads)

    # We get an instance of the ECG Database model
    ecg = ecg_service.repository.get(ecg_id)

    assert ecg.ecg_id == ecg_id
    assert ecg.leads[0].name == "I"
    assert ecg.leads[0].signal == "1,2,3"
    assert ecg.leads[1].name == "II"
    assert ecg.leads[1].signal == "4,5,6"
    assert ecg.leads[0].num_samples is None
    assert ecg.leads[1].num_samples == 3


def test_ecg_service_get(ecg_service):
    leads = [
        {"name": "I", "signal": [1, 2, 3]},
        {"name": "II", "signal": [4, 5, 6], "num_samples": 3},
    ]

    ecg_id = ecg_service.process(leads)

    # We get an instance of the ECG domain model
    ecg = ecg_service.get(ecg_id)

    assert ecg.id_ == ecg_id
    assert ecg.leads[0].name == "I"
    assert ecg.leads[0].signal == [1, 2, 3]
    assert ecg.leads[1].name == "II"
    assert ecg.leads[1].signal == [4, 5, 6]
    assert ecg.leads[0].num_samples is None
    assert ecg.leads[1].num_samples == 3
