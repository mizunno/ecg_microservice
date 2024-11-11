from pydantic import BaseModel
from typing import List, Optional


class LeadRequest(BaseModel):
    name: str
    signal: List[int]
    num_samples: Optional[int] = None


class ECGRequest(BaseModel):
    leads: List[LeadRequest]
