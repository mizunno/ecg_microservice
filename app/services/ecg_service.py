from datetime import datetime
from typing import List, Dict
from domain.ecg import ECG, Lead
from adapters.database.repository import ECGRepository
from adapters.database.ecg_mapper import ECGMapper
import uuid


class ECGService:

    """
    Service class for ECG operations
    """

    def __init__(self, repository: ECGRepository):
        """
        :param repository: ECG repository instance
        """
        self.repository = repository

    def get(self, ecg_id: str) -> ECG:
        """
        Retrieve an ECG by ID
        :param ecg_id: ECG ID (uuid)
        """

        ecg_model = self.repository.get(ecg_id)
        if ecg_model is None:
            return None

        return ECGMapper.to_domain_model(ecg_model)

    def process(self, leads: List[Dict]) -> str:
        """
        Save an ECG to the repository
        :param leads: List of lead data
        """

        # Create Lead instances from incoming lead data
        leads = [
            Lead(name=lead['name'], signal=lead['signal'],
                 num_samples=lead.get('num_samples'))
            for lead in leads
        ]

        # Create an ECG instance
        ecg = ECG(id_=uuid.uuid4().hex, date=datetime.now(), leads=leads)

        # Convert the ECG domain model to the database model and save
        ecg_model = ECGMapper.to_db_model(ecg)
        self.repository.save(ecg_model)

        return ecg.id_
