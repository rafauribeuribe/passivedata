"""
Teams Extractor - Extrae metadata de chats de Microsoft Teams
"""
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from datetime import datetime

from src.auth.graph_client import GraphClient
from src.models.teams import TeamsMessageMetadata
from src.core.config import settings


class TeamsExtractor:
    """Extractor de metadata de chats de Microsoft Teams"""

    def __init__(self, access_token: str, db: Session, extracted_by: str):
        """
        Inicializar extractor

        Args:
            access_token: Token de acceso de Microsoft Graph
            db: Sesión de base de datos
            extracted_by: Email del usuario que extrae los datos
        """
        self.graph_client = GraphClient(access_token)
        self.db = db
        self.extracted_by = extracted_by

    def _parse_chat_message(
        self,
        message: Dict,
        chat_id: str,
        chat_type: str,
        participants: List[str]
    ) -> Optional[TeamsMessageMetadata]:
        """
        Parsear mensaje de chat a TeamsMessageMetadata

        Args:
            message: Mensaje de Microsoft Graph
            chat_id: ID del chat
            chat_type: Tipo de chat (oneOnOne, group, etc)
            participants: Lista de emails de participantes

        Returns:
            TeamsMessageMetadata o None si no se puede parsear
        """
        # Información del remitente
        from_user = message.get("from", {})
        if not from_user:
            return None

        user_info = from_user.get("user", {})
        sender_email = user_info.get("userPrincipalName", "")
        sender_name = user_info.get("displayName", "")

        # Timestamps
        created_datetime = message.get("createdDateTime")
        last_modified_datetime = message.get("lastModifiedDateTime")

        if created_datetime:
            created_datetime = datetime.fromisoformat(created_datetime.replace("Z", "+00:00"))
        if last_modified_datetime:
            last_modified_datetime = datetime.fromisoformat(last_modified_datetime.replace("Z", "+00:00"))

        # Metadata del mensaje
        message_id = message.get("id", "")
        message_type = message.get("messageType", "message")
        attachments = message.get("attachments", [])
        has_attachments = len(attachments) > 0
        attachment_count = len(attachments)
        importance = message.get("importance", "normal")

        # Para chats 1:1, determinar el otro participante
        participant_email = None
        participant_name = None
        if chat_type == "oneOnOne" and len(participants) == 2:
            for email in participants:
                if email != sender_email:
                    participant_email = email
                    # No tenemos el nombre del participante aquí
                    break

        metadata = TeamsMessageMetadata(
            id=message_id,
            chat_id=chat_id,
            chat_type=chat_type,
            sender_email=sender_email,
            sender_name=sender_name,
            participant_email=participant_email,
            participant_name=participant_name,
            created_datetime=created_datetime,
            last_modified_datetime=last_modified_datetime,
            message_type=message_type,
            has_attachments=has_attachments,
            attachment_count=attachment_count,
            importance=importance,
            extracted_by=self.extracted_by
        )

        return metadata

    async def extract_user_teams_chats(
        self,
        user_id: str,
        max_messages_per_chat: int = 100,
        max_chats: int = 50
    ) -> int:
        """
        Extraer metadata de chats de Teams de un usuario

        Args:
            user_id: ID del usuario
            max_messages_per_chat: Máximo de mensajes por chat
            max_chats: Máximo de chats a procesar

        Returns:
            Número de mensajes procesados
        """
        # Obtener chats del usuario
        chats = await self.graph_client.get_user_chats(
            user_id=user_id,
            max_results=max_chats
        )

        total_records = 0

        # Procesar cada chat
        for chat in chats:
            chat_id = chat.get("id")
            chat_type = chat.get("chatType", "unknown")

            # Obtener emails de participantes
            members = chat.get("members", [])
            participant_emails = []
            for member in members:
                email = member.get("email")
                if email:
                    participant_emails.append(email)

            try:
                # Obtener mensajes del chat
                messages = await self.graph_client.get_chat_messages(
                    chat_id=chat_id,
                    max_results=max_messages_per_chat
                )

                # Procesar cada mensaje
                for message in messages:
                    metadata = self._parse_chat_message(
                        message=message,
                        chat_id=chat_id,
                        chat_type=chat_type,
                        participants=participant_emails
                    )

                    if metadata:
                        # Verificar si ya existe
                        existing = self.db.query(TeamsMessageMetadata).filter(
                            TeamsMessageMetadata.id == metadata.id
                        ).first()

                        if not existing:
                            self.db.add(metadata)
                            total_records += 1

            except Exception as e:
                print(f"❌ Error procesando chat {chat_id}: {str(e)}")
                continue

        # Commit al final
        self.db.commit()

        return total_records

    async def extract_organization_teams_chats(
        self,
        user_ids: List[str],
        max_messages_per_chat: int = 100
    ) -> Dict[str, int]:
        """
        Extraer metadata de chats de Teams de múltiples usuarios

        Args:
            user_ids: Lista de IDs de usuarios
            max_messages_per_chat: Máximo de mensajes por chat

        Returns:
            Dict con user_id: número_de_mensajes_extraídos
        """
        results = {}

        for user_id in user_ids:
            try:
                count = await self.extract_user_teams_chats(
                    user_id=user_id,
                    max_messages_per_chat=max_messages_per_chat
                )
                results[user_id] = count
                print(f"✅ Usuario {user_id}: {count} mensajes de Teams extraídos")

            except Exception as e:
                print(f"❌ Error extrayendo Teams de {user_id}: {str(e)}")
                results[user_id] = 0

        return results
