from datetime import datetime
from typing import List, Dict
from adapters.database.repository import ECGRepository
# from adapters.database.ecg_mapper import ECGMapper
from adapters.database.utils import signal_to_string, string_to_signal
from adapters.database.models import ECG, Lead
from adapters.tasks.tasks import AbstractBackgroundTask
import uuid


class ECGService:

    """
    Service class for ECG operations
    """

    def __init__(self, repository: ECGRepository,
                 background_task: AbstractBackgroundTask) -> None:
        """
        :param repository: ECG repository instance
        :param background_task: Background task instance to compute insights
        asynchronously
        """
        self.repository = repository
        self.background_task = background_task

    def get(self, ecg_id: str) -> ECG:
        """
        Retrieve an ECG by ID
        :param ecg_id: ECG ID (uuid)
        """

        ecg_model = self.repository.get(ecg_id)

        for lead in ecg_model.leads:
            lead.signal = string_to_signal(lead.signal)

        if ecg_model is None:
            return None

        # return ECGMapper.to_domain_model(ecg_model)
        return ecg_model

    def process(self, leads: List[Dict]) -> str:
        """
        Save an ECG to the repository
        :param leads: List of lead data
        """

        # Create Lead instances from incoming lead data
        leads = [
            Lead(name=lead['name'], signal=signal_to_string(lead['signal']),
                 num_samples=lead.get('num_samples'))
            for lead in leads
        ]

        # Create an ECG instance
        ecg = ECG(ecg_id=uuid.uuid4().hex, date=datetime.now(), leads=leads)

        self.repository.save(ecg)

        # Add a background task to compute insights
        self.background_task.add_task(self.compute_insights, ecg.ecg_id)

        return ecg.ecg_id

    def compute_insights(self, ecg_id: str) -> None:
        """
        Compute insights for an ECG
        :param ecg: ECG instance
        """

        print(f"Computing insights for ECG {ecg_id}")
        ecg = self.repository.get(ecg_id)

        # Compute zero crossings for each lead and save it to the DB
        for lead in ecg.leads:
            lead.zero_crossings = 0

            signal = string_to_signal(lead.signal)
            for i in range(1, len(signal)):
                if signal[i - 1] * signal[i] < 0:
                    lead.zero_crossings += 1

        self.repository.save(ecg)
