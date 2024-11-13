from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class LeadRequestSchema(BaseModel):
    name: str
    signal: List[int]
    num_samples: Optional[int] = None


class LeadResponseSchema(BaseModel):
    name: str
    signal: List[int]
    num_samples: Optional[int] = None
    zero_crossings: Optional[int] = None


class ECGRequestSchema(BaseModel):
    leads: List[LeadRequestSchema]


class ECGResponseSchema(BaseModel):
    ecg_id: str
    date: datetime
    leads: List[LeadResponseSchema]


class ZeroCrossingSchema(BaseModel):
    name: str
    zero_crossings: int


class ECGInsightResponseSchema(BaseModel):
    leads: List[ZeroCrossingSchema]


class UserCreate(BaseModel):
    username: str
    password: str
