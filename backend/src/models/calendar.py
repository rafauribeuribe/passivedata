"""
Calendar Event Metadata Model - Metadata de eventos de calendario
"""
from sqlalchemy import Column, String, DateTime, Integer, Boolean
from datetime import datetime

from src.core.database import Base


class CalendarEventMetadata(Base):
    """Modelo de metadata de eventos de calendario"""

    __tablename__ = "calendar_event_metadata"

    # Identificador único
    id = Column(String, primary_key=True, index=True)  # Event ID de Microsoft Graph

    # Organizador
    organizer_email = Column(String, index=True, nullable=False)
    organizer_name = Column(String, nullable=True)

    # Participante (una fila por cada participante)
    participant_email = Column(String, index=True, nullable=False)
    participant_name = Column(String, nullable=True)
    participant_response = Column(String, nullable=True)  # accepted, declined, tentative, none

    # Información temporal
    start_datetime = Column(DateTime, index=True, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=True)

    # Metadata del evento (sin contenido)
    subject_hash = Column(String, nullable=True)  # Hash del subject para privacidad
    is_online_meeting = Column(Boolean, default=False)
    is_cancelled = Column(Boolean, default=False)
    is_recurring = Column(Boolean, default=False)

    # Ubicación (solo si es presencial)
    location_type = Column(String, nullable=True)  # online, office, external, etc.

    # Importancia
    importance = Column(String, nullable=True)  # low, normal, high

    # Control
    extracted_at = Column(DateTime, default=datetime.utcnow)
    extracted_by = Column(String, nullable=True)

    def __repr__(self):
        return f"<CalendarEvent {self.organizer_email} with {self.participant_email} at {self.start_datetime}>"
