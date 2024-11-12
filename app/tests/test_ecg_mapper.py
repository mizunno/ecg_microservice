import pytest
from domain.ecg import ECG, Lead
from adapters.database.models import ECGModel, LeadModel
from adapters.database.utils import signal_to_string, string_to_signal
from datetime import datetime
from uuid import uuid4
from adapters.database.ecg_mapper import ECGMapper


def test_to_db_model():
    ecg_id = uuid4()
    date = datetime.now()
    leads = [
        Lead(name="Lead1", signal=[1, -1, 2, -2], num_samples=4),
        Lead(name="Lead2", signal=[3, -3, 4, -4], num_samples=4)
    ]
    ecg = ECG(id_=ecg_id, date=date, leads=leads)
    
    ecg_model = ECGMapper.to_db_model(ecg)
    
    assert ecg_model.ecg_id == ecg_id
    assert ecg_model.date == date
    assert len(ecg_model.leads) == 2
    for lead, lead_model in zip(ecg.leads, ecg_model.leads):
        assert lead_model.name == lead.name
        assert lead_model.num_samples == lead.num_samples
        assert lead_model.signal == signal_to_string(lead.signal)


def test_to_domain_model():
    ecg_id = uuid4()
    date = datetime.now()
    leads = [
        LeadModel(name="Lead1", signal=signal_to_string([1, -1, 2, -2]), num_samples=4),
        LeadModel(name="Lead2", signal=signal_to_string([3, -3, 4, -4]), num_samples=4)
    ]
    ecg_model = ECGModel(ecg_id=ecg_id, date=date, leads=leads)
    
    ecg = ECGMapper.to_domain_model(ecg_model)
    
    assert ecg.id_ == ecg_id
    assert ecg.date == date
    assert len(ecg.leads) == 2
    for lead, lead_model in zip(ecg.leads, ecg_model.leads):
        assert lead.name == lead_model.name
        assert lead.num_samples == lead_model.num_samples
        assert lead.signal == string_to_signal(lead_model.signal)
