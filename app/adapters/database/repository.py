from abc import ABC, abstractmethod
from typing import Optional
from adapters.database.models import ECG
from sqlalchemy.orm import Session


class ECGRepository(ABC):

    """
    Abstract class for ECG repository
    """

    @abstractmethod
    def save(self, ecg: ECG):
        pass

    @abstractmethod
    def get(self, uuid: str) -> Optional[ECG]:
        pass


class DatabaseECGRepository(ECGRepository):

    """
    Database implementation of ECG repository
    """

    def __init__(self, db_session: Session):
        """
        :param db_session: Database session
        """
        self.db_session = db_session

    def save(self, ecg: ECG):
        """
        :param ecg: ECG database model
        """
        self.db_session.add(ecg)
        self.db_session.commit()

    def get(self, ecg_id: str) -> Optional[ECG]:
        """
        :param ecg_id: ECG ID (uuid)
        """
        return self.db_session.query(ECG).filter(
            ECG.ecg_id == ecg_id).first()
