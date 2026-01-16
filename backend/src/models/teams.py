"""
Teams Chat Metadata Model - Metadata de chats de Microsoft Teams
"""
from sqlalchemy import Column, String, DateTime, Boolean, Integer
from datetime import datetime

from src.core.database import Base


class TeamsMessageMetadata(Base):
    """Modelo de metadata de mensajes de Teams"""

    __tablename__ = "teams_message_metadata"

    # Identificador único
    id = Column(String, primary_key=True, index=True)  # Message ID de Microsoft Graph

    # Chat/Canal
    chat_id = Column(String, index=True, nullable=False)
    chat_type = Column(String, nullable=False)  # oneOnOne, group, meeting, channel

    # Remitente
    sender_email = Column(String, index=True, nullable=False)
    sender_name = Column(String, nullable=True)

    # Participante/Receptor (para chats 1:1)
    participant_email = Column(String, index=True, nullable=True)
    participant_name = Column(String, nullable=True)

    # Información temporal
    created_datetime = Column(DateTime, index=True, nullable=False)
    last_modified_datetime = Column(DateTime, nullable=True)

    # Metadata del mensaje (sin contenido)
    message_type = Column(String, nullable=True)  # message, systemEventMessage, etc.
    has_attachments = Column(Boolean, default=False)
    attachment_count = Column(Integer, default=0)

    # Reacciones y respuestas
    has_reactions = Column(Boolean, default=False)
    reply_count = Column(Integer, default=0)

    # Importancia
    importance = Column(String, nullable=True)  # normal, high, urgent

    # Información de equipo/canal (si aplica)
    team_id = Column(String, nullable=True, index=True)
    channel_id = Column(String, nullable=True, index=True)

    # Control
    extracted_at = Column(DateTime, default=datetime.utcnow)
    extracted_by = Column(String, nullable=True)

    def __repr__(self):
        return f"<TeamsMessage {self.sender_email} in {self.chat_type} at {self.created_datetime}>"
