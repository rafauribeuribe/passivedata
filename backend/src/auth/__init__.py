"""
Authentication Module - Microsoft Graph OAuth 2.0
"""
from .msal_handler import MSALHandler
from .dependencies import get_current_user

__all__ = ["MSALHandler", "get_current_user"]
