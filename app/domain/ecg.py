from datetime import datetime
from typing import List, Optional


class Lead:

    """
    Class representing a lead (I, II, III, aVR, aVL, ...) in an ECG.
    A lead is a specific viewpoint of the heart's electrical activity,
    captured from electrodes placed on the skin at standardized positions
    on the body.
    """

    def __init__(self, name: str, signal: List[int], num_samples: Optional[int] = None):
        """
        :param name: Name of the lead
        :param signal: List of integers representing the signal
        :param num_samples: Size of the signal (This value might not always be present)
        """

        self.name = name
        self.num_samples = num_samples
        self.signal = signal

    def count_zero_crossings(self) -> int:
        """
        Calculate the number of zero crossings in the signal.
        Zero crossing occurs when the sign of consecutive values changes.
        """
        zero_crossings = 0

        for i in range(1, len(self.signal)):
            if (self.signal[i - 1] <= 0 and self.signal[i] > 0) or (self.signal[i - 1] >= 0 and self.signal[i] < 0):
                zero_crossings += 1
        return zero_crossings


class ECG:

    """
    Class representing an ECG (electrocardiogram)
    """

    def __init__(self, id_: str, date: datetime, leads: List[Lead]):
        """
        :param id: Unique identifier for the ECG
        :param date: Datetime of creation
        :param leads: List of Leads
        """
        self.id_ = id_
        self.date = date
        self.leads = leads

    def get_zero_crossings(self) -> dict:
        """
        Return the number of times each ECG channel crosses zero.
        """
        return {lead.name: lead.count_zero_crossings() for lead in self.leads}
