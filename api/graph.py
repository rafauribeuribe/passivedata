"""Cliente para Microsoft Graph API"""
import msal
import httpx
from datetime import datetime
from typing import Optional
from .config import settings


def get_auth_url() -> str:
    app = msal.ConfidentialClientApplication(
        settings.MICROSOFT_CLIENT_ID,
        authority=settings.authority,
        client_credential=settings.MICROSOFT_CLIENT_SECRET,
    )
    return app.get_authorization_request_url(
        scopes=settings.scopes,
        redirect_uri=settings.REDIRECT_URI,
        state="passivedata"
    )


def exchange_code_for_token(code: str) -> Optional[dict]:
    app = msal.ConfidentialClientApplication(
        settings.MICROSOFT_CLIENT_ID,
        authority=settings.authority,
        client_credential=settings.MICROSOFT_CLIENT_SECRET,
    )
    result = app.acquire_token_by_authorization_code(
        code,
        scopes=settings.scopes,
        redirect_uri=settings.REDIRECT_URI,
    )
    if "access_token" in result:
        return result
    return None


class GraphClient:
    BASE = "https://graph.microsoft.com/v1.0"

    def __init__(self, token: str):
        self.headers = {"Authorization": f"Bearer {token}"}

    async def get(self, path: str, params: dict = None) -> dict:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(f"{self.BASE}{path}", headers=self.headers, params=params)
            r.raise_for_status()
            return r.json()

    async def get_me(self) -> dict:
        return await self.get("/me")

    async def get_users(self) -> list[dict]:
        """Obtiene todos los usuarios de la organización"""
        users = []
        url = "/users?$select=id,mail,displayName,department,jobTitle&$top=999"
        while url:
            data = await self.get(url) if url.startswith("/") else await self._get_full(url)
            users.extend(data.get("value", []))
            url = data.get("@odata.nextLink")
            if url:
                # nextLink ya viene con la URL completa, extrae solo el path+query
                url = url.replace(self.BASE, "")
        return users

    async def _get_full(self, full_url: str) -> dict:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(full_url, headers=self.headers)
            r.raise_for_status()
            return r.json()

    async def get_messages(self, user_id: str, top: int = 500) -> list[dict]:
        """Metadata de correos de un usuario"""
        messages = []
        fields = "id,sender,toRecipients,sentDateTime,hasAttachments,importance,conversationId"
        path = f"/users/{user_id}/messages"
        params = {"$select": fields, "$top": min(top, 100), "$orderby": "sentDateTime desc"}
        while path and len(messages) < top:
            data = await self.get(path, params)
            messages.extend(data.get("value", []))
            next_link = data.get("@odata.nextLink")
            path = next_link.replace(self.BASE, "") if next_link else None
            params = None  # ya viene en el nextLink
        return messages[:top]

    async def get_calendar_events(self, user_id: str, top: int = 500) -> list[dict]:
        """Metadata de eventos de calendario de un usuario"""
        events = []
        fields = "id,organizer,attendees,start,end,isOnlineMeeting,recurrence,isCancelled"
        path = f"/users/{user_id}/calendar/events"
        params = {"$select": fields, "$top": min(top, 100), "$orderby": "start/dateTime desc"}
        while path and len(events) < top:
            data = await self.get(path, params)
            events.extend(data.get("value", []))
            next_link = data.get("@odata.nextLink")
            path = next_link.replace(self.BASE, "") if next_link else None
            params = None
        return events[:top]
