"""
User Model - Usuarios de la organización
"""
from sqlalchemy import Column, String, DateTime, Boolean
from datetime import datetime

from src.core.database import Base


class User(Base):
    """Modelo de usuario de la organización"""

    __tablename__ = "users"

    # Campos principales
    id = Column(String, primary_key=True, index=True)  # User ID de Microsoft Graph
    email = Column(String, unique=True, index=True, nullable=False)
    display_name = Column(String, nullable=True)
    job_title = Column(String, nullable=True)
    department = Column(String, nullable=True)

    # Control de acceso
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Tokens de autenticación (encriptados)
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    token_expires_at = Column(DateTime, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<User {self.email}>"
