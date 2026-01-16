"""
Email Extractor - Extrae metadata de correos electrónicos
"""
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import hashlib

from src.auth.graph_client import GraphClient
from src.models.email import EmailMetadata
from src.core.config import settings


class EmailExtractor:
    """Extractor de metadata de correos electrónicos"""

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

    @staticmethod
    def _hash_subject(subject: str) -> str:
        """Hash del subject para privacidad"""
        if not subject:
            return ""
        return hashlib.sha256(subject.encode()).hexdigest()[:16]

    def _parse_email_metadata(self, message: Dict) -> List[EmailMetadata]:
        """
        Parsear mensaje de Graph API a EmailMetadata

        Args:
            message: Mensaje de Microsoft Graph

        Returns:
            Lista de EmailMetadata (uno por cada destinatario)
        """
        metadata_list = []

        # Información del remitente
        sender = message.get("sender", {}).get("emailAddress", {})
        sender_email = sender.get("address", "")
        sender_name = sender.get("name", "")

        # Timestamps
        sent_datetime = message.get("sentDateTime")
        received_datetime = message.get("receivedDateTime")

        if sent_datetime:
            sent_datetime = datetime.fromisoformat(sent_datetime.replace("Z", "+00:00"))
        if received_datetime:
            received_datetime = datetime.fromisoformat(received_datetime.replace("Z", "+00:00"))

        # Metadata del mensaje
        message_id = message.get("id", "")
        subject = message.get("subject", "")
        has_attachments = message.get("hasAttachments", False)
        importance = message.get("importance", "normal")
        conversation_id = message.get("conversationId", "")
        is_read = message.get("isRead", False)
        categories = ",".join(message.get("categories", []))

        # Crear un EmailMetadata por cada destinatario
        recipients = message.get("toRecipients", [])
        for idx, recipient in enumerate(recipients):
            recipient_email_address = recipient.get("emailAddress", {})
            recipient_email = recipient_email_address.get("address", "")
            recipient_name = recipient_email_address.get("name", "")

            # ID único por destinatario
            unique_id = f"{message_id}_{idx}"

            metadata = EmailMetadata(
                id=unique_id,
                sender_email=sender_email,
                sender_name=sender_name,
                recipient_email=recipient_email,
                recipient_name=recipient_name,
                sent_datetime=sent_datetime,
                received_datetime=received_datetime,
                subject_hash=self._hash_subject(subject),
                has_attachments=has_attachments,
                importance=importance,
                conversation_id=conversation_id,
                is_read=is_read,
                categories=categories,
                extracted_by=self.extracted_by
            )

            metadata_list.append(metadata)

        return metadata_list

    async def extract_user_emails(
        self,
        user_id: str,
        max_emails: Optional[int] = None,
        days_back: int = 90
    ) -> int:
        """
        Extraer metadata de correos de un usuario

        Args:
            user_id: ID del usuario
            max_emails: Número máximo de correos a extraer
            days_back: Días hacia atrás para extraer

        Returns:
            Número de emails procesados
        """
        if max_emails is None:
            max_emails = settings.MAX_EMAILS_PER_USER

        start_date = datetime.utcnow() - timedelta(days=days_back)

        # Obtener mensajes de Graph API
        messages = await self.graph_client.get_user_messages(
            user_id=user_id,
            max_results=max_emails,
            start_date=start_date
        )

        total_records = 0

        # Procesar cada mensaje
        for message in messages:
            metadata_list = self._parse_email_metadata(message)

            for metadata in metadata_list:
                # Verificar si ya existe
                existing = self.db.query(EmailMetadata).filter(
                    EmailMetadata.id == metadata.id
                ).first()

                if not existing:
                    self.db.add(metadata)
                    total_records += 1

        # Commit al final
        self.db.commit()

        return total_records

    async def extract_organization_emails(
        self,
        user_ids: List[str],
        max_emails_per_user: Optional[int] = None
    ) -> Dict[str, int]:
        """
        Extraer metadata de correos de múltiples usuarios

        Args:
            user_ids: Lista de IDs de usuarios
            max_emails_per_user: Máximo de correos por usuario

        Returns:
            Dict con user_id: número_de_emails_extraídos
        """
        results = {}

        for user_id in user_ids:
            try:
                count = await self.extract_user_emails(
                    user_id=user_id,
                    max_emails=max_emails_per_user
                )
                results[user_id] = count
                print(f"✅ Usuario {user_id}: {count} emails extraídos")

            except Exception as e:
                print(f"❌ Error extrayendo emails de {user_id}: {str(e)}")
                results[user_id] = 0

        return results
