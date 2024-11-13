import pytest
from adapters.database.repository import ECGRepository
from adapters.tasks.tasks import AbstractBackgroundTask
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


class MockBackgroundTask(AbstractBackgroundTask):
    """
    Mock implementation of background task
    """

    def add_task(self, task, *args, **kwargs):
        task(*args, **kwargs)


@pytest.fixture
def mock_ecg_repository():
    return MockECGRepository()


@pytest.fixture
def mock_background_task():
    return MockBackgroundTask()


@pytest.fixture
def ecg_service(mock_ecg_repository, mock_background_task):
    return ECGService(mock_ecg_repository, mock_background_task)


def test_ecg_service_process(ecg_service):
    leads = [
        {"name": "I", "signal": [1, 2, 3]},
        {"name": "II", "signal": [-1, 1, 2], "num_samples": 3},
    ]

    ecg_id = ecg_service.process(leads, user_id=1)

    # We get an instance of the ECG Database model
    ecg = ecg_service.repository.get(ecg_id)

    assert ecg.ecg_id == ecg_id
    assert ecg.leads[0].name == "I"
    assert ecg.leads[0].signal == "1,2,3"
    assert ecg.leads[0].zero_crossings == 0
    assert ecg.leads[1].name == "II"
    assert ecg.leads[1].signal == "-1,1,2"
    assert ecg.leads[1].zero_crossings == 1
    assert ecg.leads[0].num_samples is None
    assert ecg.leads[1].num_samples == 3


def test_ecg_service_get(ecg_service):
    leads = [
        {"name": "I", "signal": [1, 2, 3]},
        {"name": "II", "signal": [-1, 1, 2], "num_samples": 3},
    ]

    ecg_id = ecg_service.process(leads, user_id=1)

    ecg = ecg_service.get(ecg_id)

    assert ecg.ecg_id == ecg_id
    assert ecg.leads[0].name == "I"
    assert ecg.leads[0].signal == [1, 2, 3]
    assert ecg.leads[1].name == "II"
    assert ecg.leads[1].signal == [-1, 1, 2]
    assert ecg.leads[0].num_samples is None
    assert ecg.leads[1].num_samples == 3
