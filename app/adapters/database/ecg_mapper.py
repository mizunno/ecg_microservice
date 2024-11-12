from domain.ecg import ECG, Lead
from adapters.database.models import ECGModel, LeadModel
from adapters.database.utils import string_to_signal, signal_to_string


class ECGMapper:

    """
    Mapper class (serializer) for ECG domain and database models
    """

    @staticmethod
    def to_db_model(ecg: ECG) -> ECGModel:
        return ECGModel(
            ecg_id=ecg.id_,
            date=ecg.date,
            leads=[
                LeadModel(
                    signal=signal_to_string(lead.signal),
                    name=lead.name,
                    num_samples=lead.num_samples,
                )
                for lead in ecg.leads
            ]
        )

    @staticmethod
    def to_domain_model(ecg_model: ECGModel) -> ECG:
        return ECG(
            id_=ecg_model.ecg_id,
            date=ecg_model.date,
            leads=[
                Lead(
                    name=lead_model.name,
                    signal=string_to_signal(lead_model.signal),
                    num_samples=lead_model.num_samples
                )
                for lead_model in ecg_model.leads
            ]
        )
