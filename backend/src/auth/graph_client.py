"""
Microsoft Graph Client - Cliente para interactuar con Microsoft Graph API
"""
import httpx
from typing import Optional, Dict, List
from datetime import datetime

from src.core.config import settings


class GraphClient:
    """Cliente para Microsoft Graph API"""

    def __init__(self, access_token: str):
        """
        Inicializar cliente con access token

        Args:
            access_token: Token de acceso de Microsoft Graph
        """
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        self.base_url = settings.GRAPH_API_ENDPOINT

    async def get_user_profile(self) -> Optional[Dict]:
        """
        Obtener perfil del usuario actual

        Returns:
            Dict con información del usuario
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/me",
                    headers=self.headers,
                    timeout=30.0
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"❌ Error al obtener perfil: {str(e)}")
            return None

    async def get_organization_users(self, max_results: int = 999) -> List[Dict]:
        """
        Obtener lista de usuarios de la organización

        Args:
            max_results: Número máximo de usuarios a obtener

        Returns:
            Lista de usuarios
        """
        try:
            users = []
            url = f"{self.base_url}/users?$top=999&$select=id,mail,displayName,jobTitle,department"

            async with httpx.AsyncClient() as client:
                while url and len(users) < max_results:
                    response = await client.get(
                        url,
                        headers=self.headers,
                        timeout=30.0
                    )
                    response.raise_for_status()
                    data = response.json()

                    users.extend(data.get("value", []))
                    url = data.get("@odata.nextLink")  # Paginación

            return users[:max_results]

        except Exception as e:
            print(f"❌ Error al obtener usuarios: {str(e)}")
            return []

    async def get_user_messages(
        self,
        user_id: str = "me",
        max_results: int = 100,
        start_date: Optional[datetime] = None
    ) -> List[Dict]:
        """
        Obtener mensajes de correo de un usuario

        Args:
            user_id: ID del usuario (default: 'me' para usuario actual)
            max_results: Número máximo de mensajes
            start_date: Fecha de inicio para filtrar mensajes

        Returns:
            Lista de mensajes (metadata solamente)
        """
        try:
            messages = []
            select_fields = "id,sender,toRecipients,sentDateTime,receivedDateTime,subject,hasAttachments,importance,conversationId,isRead,categories"
            url = f"{self.base_url}/users/{user_id}/messages?$top=100&$select={select_fields}"

            if start_date:
                date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                url += f"&$filter=receivedDateTime ge {date_str}"

            async with httpx.AsyncClient() as client:
                while url and len(messages) < max_results:
                    response = await client.get(
                        url,
                        headers=self.headers,
                        timeout=30.0
                    )
                    response.raise_for_status()
                    data = response.json()

                    messages.extend(data.get("value", []))
                    url = data.get("@odata.nextLink")

            return messages[:max_results]

        except Exception as e:
            print(f"❌ Error al obtener mensajes: {str(e)}")
            return []

    async def get_user_calendar_events(
        self,
        user_id: str = "me",
        max_results: int = 100,
        start_date: Optional[datetime] = None
    ) -> List[Dict]:
        """
        Obtener eventos de calendario de un usuario

        Args:
            user_id: ID del usuario
            max_results: Número máximo de eventos
            start_date: Fecha de inicio para filtrar eventos

        Returns:
            Lista de eventos
        """
        try:
            events = []
            select_fields = "id,subject,organizer,attendees,start,end,isOnlineMeeting,isCancelled,recurrence,importance,location"
            url = f"{self.base_url}/users/{user_id}/calendar/events?$top=100&$select={select_fields}"

            if start_date:
                date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                url += f"&$filter=start/dateTime ge '{date_str}'"

            async with httpx.AsyncClient() as client:
                while url and len(events) < max_results:
                    response = await client.get(
                        url,
                        headers=self.headers,
                        timeout=30.0
                    )
                    response.raise_for_status()
                    data = response.json()

                    events.extend(data.get("value", []))
                    url = data.get("@odata.nextLink")

            return events[:max_results]

        except Exception as e:
            print(f"❌ Error al obtener eventos: {str(e)}")
            return []

    async def get_user_chats(
        self,
        user_id: str = "me",
        max_results: int = 50
    ) -> List[Dict]:
        """
        Obtener chats de Teams de un usuario

        Args:
            user_id: ID del usuario
            max_results: Número máximo de chats

        Returns:
            Lista de chats
        """
        try:
            chats = []
            url = f"{self.base_url}/users/{user_id}/chats?$expand=members"

            async with httpx.AsyncClient() as client:
                while url and len(chats) < max_results:
                    response = await client.get(
                        url,
                        headers=self.headers,
                        timeout=30.0
                    )
                    response.raise_for_status()
                    data = response.json()

                    chats.extend(data.get("value", []))
                    url = data.get("@odata.nextLink")

            return chats[:max_results]

        except Exception as e:
            print(f"❌ Error al obtener chats: {str(e)}")
            return []

    async def get_chat_messages(
        self,
        chat_id: str,
        max_results: int = 100
    ) -> List[Dict]:
        """
        Obtener mensajes de un chat específico

        Args:
            chat_id: ID del chat
            max_results: Número máximo de mensajes

        Returns:
            Lista de mensajes
        """
        try:
            messages = []
            select_fields = "id,from,createdDateTime,lastModifiedDateTime,messageType,attachments,replyToId,importance"
            url = f"{self.base_url}/chats/{chat_id}/messages?$top=50&$select={select_fields}"

            async with httpx.AsyncClient() as client:
                while url and len(messages) < max_results:
                    response = await client.get(
                        url,
                        headers=self.headers,
                        timeout=30.0
                    )
                    response.raise_for_status()
                    data = response.json()

                    messages.extend(data.get("value", []))
                    url = data.get("@odata.nextLink")

            return messages[:max_results]

        except Exception as e:
            print(f"❌ Error al obtener mensajes del chat: {str(e)}")
            return []
