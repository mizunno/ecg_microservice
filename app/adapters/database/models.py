from enum import Enum
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.USER)


class ECG(Base):
    __tablename__ = "ecgs"

    id = Column(Integer, primary_key=True, index=True)
    ecg_id = Column(String, unique=True, nullable=False)
    date = Column(DateTime(timezone=False))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    leads = relationship("Lead", back_populates="ecg")
    user = relationship("User")


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    ecg_id = Column(String, ForeignKey("ecgs.ecg_id"))
    name = Column(String)
    num_samples = Column(Integer, nullable=True)
    signal = Column(String, nullable=False)
    zero_crossings = Column(Integer, nullable=True)
    ecg = relationship("ECG", back_populates="leads")
