from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import config

engine = create_engine(config.DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
