import pytest
from domain.ecg import ECG, Lead
from datetime import datetime


# Test cases for Lead class
@pytest.mark.parametrize("name, signal, expected_zero_crossings", [
    # 4 zero crossings
    ("I", [1, -1, 1, -1, 1], 4),
    # No zero crossings
    ("II", [0, 0, 0, 0], 0),
    # 3 zero crossings
    ("III", [1, 1, -1, -1, 1, -1], 3),
    # 1 zero crossing
    ("aVR", [-1, -1, -1, 1, 1, 1], 1),
    # 3 zero crossings, including zero value
    ("aVL", [1, -1, 0, 1, -1], 3),
])
def test_count_zero_crossings(name, signal, expected_zero_crossings):
    lead = Lead(name=name, signal=signal)
    assert lead.count_zero_crossings() == expected_zero_crossings


# Test cases for ECG class
def test_get_zero_crossings():
    lead1 = Lead(name="I", signal=[1, -1, 1, -1, 1])   # 4 zero crossings
    lead2 = Lead(name="II", signal=[1, 1, -1, -1, 1])  # 2 zero crossings
    lead3 = Lead(name="III", signal=[0, 0, 0])         # 0 zero crossings

    ecg = ECG(id_="12345", date=datetime.now(), leads=[lead1, lead2, lead3])

    expected_zero_crossings = {
        "I": 4,
        "II": 2,
        "III": 0
    }
    assert ecg.get_zero_crossings() == expected_zero_crossings
