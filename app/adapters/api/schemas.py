from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class LeadSchema(BaseModel):
    name: str
    signal: List[int]
    num_samples: Optional[int] = None


class ECGRequestSchema(BaseModel):
    leads: List[LeadSchema]


class ECGResponseSchema(BaseModel):
    ecg_id: str
    date: datetime
    leads: List[LeadSchema]
