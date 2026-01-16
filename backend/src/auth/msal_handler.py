"""
MSAL Handler - Manejo de autenticación con Microsoft Graph
"""
import msal
from typing import Optional, Dict
from datetime import datetime, timedelta

from src.core.config import settings


class MSALHandler:
    """Handler para autenticación con Microsoft Graph usando MSAL"""

    def __init__(self):
        """Inicializar MSAL Confidential Client"""
        self.client_app = msal.ConfidentialClientApplication(
            settings.MICROSOFT_CLIENT_ID,
            authority=settings.AUTHORITY,
            client_credential=settings.MICROSOFT_CLIENT_SECRET,
        )

    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """
        Genera URL de autorización para OAuth flow

        Args:
            state: Estado opcional para prevenir CSRF

        Returns:
            URL de autorización de Microsoft
        """
        auth_url = self.client_app.get_authorization_request_url(
            scopes=settings.SCOPE_LIST,
            redirect_uri=settings.REDIRECT_URI,
            state=state
        )
        return auth_url

    def acquire_token_by_auth_code(self, code: str) -> Optional[Dict]:
        """
        Adquiere token usando authorization code

        Args:
            code: Authorization code de Microsoft

        Returns:
            Dict con access_token, refresh_token, expires_in
        """
        try:
            result = self.client_app.acquire_token_by_authorization_code(
                code,
                scopes=settings.SCOPE_LIST,
                redirect_uri=settings.REDIRECT_URI
            )

            if "access_token" in result:
                return {
                    "access_token": result["access_token"],
                    "refresh_token": result.get("refresh_token"),
                    "expires_in": result.get("expires_in", 3600),
                    "token_type": result.get("token_type", "Bearer"),
                    "expires_at": datetime.utcnow() + timedelta(seconds=result.get("expires_in", 3600))
                }
            else:
                print(f"❌ Error al adquirir token: {result.get('error_description')}")
                return None

        except Exception as e:
            print(f"❌ Excepción al adquirir token: {str(e)}")
            return None

    def acquire_token_by_refresh_token(self, refresh_token: str) -> Optional[Dict]:
        """
        Refresca access token usando refresh token

        Args:
            refresh_token: Refresh token de Microsoft

        Returns:
            Dict con nuevo access_token
        """
        try:
            result = self.client_app.acquire_token_by_refresh_token(
                refresh_token,
                scopes=settings.SCOPE_LIST
            )

            if "access_token" in result:
                return {
                    "access_token": result["access_token"],
                    "refresh_token": result.get("refresh_token", refresh_token),
                    "expires_in": result.get("expires_in", 3600),
                    "expires_at": datetime.utcnow() + timedelta(seconds=result.get("expires_in", 3600))
                }
            else:
                print(f"❌ Error al refrescar token: {result.get('error_description')}")
                return None

        except Exception as e:
            print(f"❌ Excepción al refrescar token: {str(e)}")
            return None

    def is_token_expired(self, expires_at: datetime) -> bool:
        """
        Verifica si un token ha expirado

        Args:
            expires_at: Fecha de expiración del token

        Returns:
            True si el token ha expirado
        """
        # Agregar buffer de 5 minutos
        return datetime.utcnow() >= (expires_at - timedelta(minutes=5))


# Instancia global
msal_handler = MSALHandler()
