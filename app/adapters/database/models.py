from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class ECG(Base):
    __tablename__ = 'ecgs'

    id = Column(Integer, primary_key=True, index=True)
    ecg_id = Column(String, unique=True, nullable=False)
    date = Column(DateTime(timezone=False))
    leads = relationship("Lead", back_populates="ecg")


class Lead(Base):
    __tablename__ = 'leads'

    id = Column(Integer, primary_key=True, index=True)
    ecg_id = Column(String, ForeignKey('ecgs.ecg_id'))
    name = Column(String)
    num_samples = Column(Integer, nullable=True)
    signal = Column(String, nullable=False)
    zero_crossings = Column(Integer, nullable=True)
    ecg = relationship("ECG", back_populates="leads")
