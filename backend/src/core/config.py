"""
Configuración de la aplicación
Carga variables de entorno y configuración global
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Configuración de la aplicación"""

    # Microsoft Graph App Registration
    MICROSOFT_CLIENT_ID: str
    MICROSOFT_CLIENT_SECRET: str
    MICROSOFT_TENANT_ID: str
    REDIRECT_URI: str = "http://localhost:8000/auth/callback"

    # Microsoft Graph API
    GRAPH_API_ENDPOINT: str = "https://graph.microsoft.com/v1.0"
    SCOPES: str = "User.Read,Mail.Read,Calendars.Read,Chat.Read,User.ReadBasic.All"

    # Database
    DATABASE_URL: str = "sqlite:///./passivedata.db"

    # Application Settings
    SECRET_KEY: str
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True

    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"

    # Data Export Settings
    MAX_EMAILS_PER_USER: int = 1000
    MAX_CALENDAR_EVENTS_PER_USER: int = 1000
    MAX_CHAT_MESSAGES_PER_USER: int = 1000
    DATA_RETENTION_DAYS: int = 90

    # Authority for MSAL
    @property
    def AUTHORITY(self) -> str:
        return f"https://login.microsoftonline.com/{self.MICROSOFT_TENANT_ID}"

    @property
    def SCOPE_LIST(self) -> List[str]:
        """Convierte string de scopes a lista"""
        return [f"https://graph.microsoft.com/.default"]

    class Config:
        env_file = ".env"
        case_sensitive = True


# Instancia global de configuración
settings = Settings()
