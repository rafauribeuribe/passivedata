from sqlalchemy import create_engine, Column, String, DateTime, Integer, Boolean, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime
from typing import Generator

from .config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    display_name = Column(String)
    department = Column(String)
    job_title = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class EmailEdge(Base):
    """Un email entre dos personas = una arista en la red"""
    __tablename__ = "email_edges"
    id = Column(String, primary_key=True)
    sender = Column(String, index=True)
    recipient = Column(String, index=True)
    sent_at = Column(DateTime, index=True)
    hour_of_day = Column(Integer)   # 0-23
    day_of_week = Column(Integer)   # 0=lunes, 6=domingo
    has_attachments = Column(Boolean, default=False)
    importance = Column(String)
    extracted_at = Column(DateTime, default=datetime.utcnow)


class CalendarEdge(Base):
    """Una reunión entre dos personas = una arista en la red"""
    __tablename__ = "calendar_edges"
    id = Column(String, primary_key=True)
    organizer = Column(String, index=True)
    participant = Column(String, index=True)
    start_at = Column(DateTime, index=True)
    duration_minutes = Column(Integer)
    hour_of_day = Column(Integer)
    day_of_week = Column(Integer)
    is_online = Column(Boolean, default=False)
    is_recurring = Column(Boolean, default=False)
    extracted_at = Column(DateTime, default=datetime.utcnow)


class ExtractionJob(Base):
    """Registro de jobs de extracción"""
    __tablename__ = "extraction_jobs"
    id = Column(String, primary_key=True)
    job_type = Column(String)         # emails, calendar
    status = Column(String)           # running, done, error
    users_processed = Column(Integer, default=0)
    records_found = Column(Integer, default=0)
    error_message = Column(String)
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
