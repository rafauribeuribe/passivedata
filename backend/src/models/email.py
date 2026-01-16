"""
Email Metadata Model - Metadata de correos electrónicos
"""
from sqlalchemy import Column, String, DateTime, Integer, Boolean
from datetime import datetime

from src.core.database import Base


class EmailMetadata(Base):
    """Modelo de metadata de correos electrónicos"""

    __tablename__ = "email_metadata"

    # Identificador único
    id = Column(String, primary_key=True, index=True)  # Message ID de Microsoft Graph

    # Remitente y destinatarios
    sender_email = Column(String, index=True, nullable=False)
    sender_name = Column(String, nullable=True)

    # Destinatarios principales
    recipient_email = Column(String, index=True, nullable=False)
    recipient_name = Column(String, nullable=True)

    # Información temporal
    sent_datetime = Column(DateTime, index=True, nullable=False)
    received_datetime = Column(DateTime, nullable=True)

    # Metadata del mensaje (sin contenido)
    subject_hash = Column(String, nullable=True)  # Hash del subject para privacidad
    has_attachments = Column(Boolean, default=False)
    importance = Column(String, nullable=True)  # Low, Normal, High

    # Información adicional
    conversation_id = Column(String, nullable=True, index=True)
    is_read = Column(Boolean, default=False)

    # Categorías
    categories = Column(String, nullable=True)  # JSON string de categorías

    # Control
    extracted_at = Column(DateTime, default=datetime.utcnow)
    extracted_by = Column(String, nullable=True)  # User que extrajo los datos

    def __repr__(self):
        return f"<EmailMetadata {self.sender_email} -> {self.recipient_email} at {self.sent_datetime}>"
