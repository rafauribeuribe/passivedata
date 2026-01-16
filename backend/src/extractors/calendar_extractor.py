"""
Calendar Extractor - Extrae metadata de eventos de calendario
"""
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import hashlib

from src.auth.graph_client import GraphClient
from src.models.calendar import CalendarEventMetadata
from src.core.config import settings


class CalendarExtractor:
    """Extractor de metadata de eventos de calendario"""

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

    def _parse_calendar_event(self, event: Dict) -> List[CalendarEventMetadata]:
        """
        Parsear evento de Graph API a CalendarEventMetadata

        Args:
            event: Evento de Microsoft Graph

        Returns:
            Lista de CalendarEventMetadata (uno por cada participante)
        """
        metadata_list = []

        # Información del organizador
        organizer = event.get("organizer", {}).get("emailAddress", {})
        organizer_email = organizer.get("address", "")
        organizer_name = organizer.get("name", "")

        # Timestamps
        start = event.get("start", {})
        end = event.get("end", {})
        start_datetime = start.get("dateTime")
        end_datetime = end.get("dateTime")

        if start_datetime:
            start_datetime = datetime.fromisoformat(start_datetime)
        if end_datetime:
            end_datetime = datetime.fromisoformat(end_datetime)

        # Duración en minutos
        duration_minutes = None
        if start_datetime and end_datetime:
            duration_minutes = int((end_datetime - start_datetime).total_seconds() / 60)

        # Metadata del evento
        event_id = event.get("id", "")
        subject = event.get("subject", "")
        is_online_meeting = event.get("isOnlineMeeting", False)
        is_cancelled = event.get("isCancelled", False)
        is_recurring = event.get("recurrence") is not None
        importance = event.get("importance", "normal")

        # Ubicación
        location = event.get("location", {})
        location_type = "online" if is_online_meeting else location.get("locationType", "unknown")

        # Crear un CalendarEventMetadata por cada participante
        attendees = event.get("attendees", [])

        # Si no hay participantes, crear uno con el organizador
        if not attendees:
            metadata = CalendarEventMetadata(
                id=f"{event_id}_0",
                organizer_email=organizer_email,
                organizer_name=organizer_name,
                participant_email=organizer_email,
                participant_name=organizer_name,
                participant_response="organizer",
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                duration_minutes=duration_minutes,
                subject_hash=self._hash_subject(subject),
                is_online_meeting=is_online_meeting,
                is_cancelled=is_cancelled,
                is_recurring=is_recurring,
                location_type=location_type,
                importance=importance,
                extracted_by=self.extracted_by
            )
            metadata_list.append(metadata)
        else:
            for idx, attendee in enumerate(attendees):
                attendee_email_address = attendee.get("emailAddress", {})
                participant_email = attendee_email_address.get("address", "")
                participant_name = attendee_email_address.get("name", "")
                status = attendee.get("status", {})
                response = status.get("response", "none")

                unique_id = f"{event_id}_{idx}"

                metadata = CalendarEventMetadata(
                    id=unique_id,
                    organizer_email=organizer_email,
                    organizer_name=organizer_name,
                    participant_email=participant_email,
                    participant_name=participant_name,
                    participant_response=response,
                    start_datetime=start_datetime,
                    end_datetime=end_datetime,
                    duration_minutes=duration_minutes,
                    subject_hash=self._hash_subject(subject),
                    is_online_meeting=is_online_meeting,
                    is_cancelled=is_cancelled,
                    is_recurring=is_recurring,
                    location_type=location_type,
                    importance=importance,
                    extracted_by=self.extracted_by
                )

                metadata_list.append(metadata)

        return metadata_list

    async def extract_user_calendar(
        self,
        user_id: str,
        max_events: Optional[int] = None,
        days_back: int = 90
    ) -> int:
        """
        Extraer metadata de calendario de un usuario

        Args:
            user_id: ID del usuario
            max_events: Número máximo de eventos a extraer
            days_back: Días hacia atrás para extraer

        Returns:
            Número de eventos procesados
        """
        if max_events is None:
            max_events = settings.MAX_CALENDAR_EVENTS_PER_USER

        start_date = datetime.utcnow() - timedelta(days=days_back)

        # Obtener eventos de Graph API
        events = await self.graph_client.get_user_calendar_events(
            user_id=user_id,
            max_results=max_events,
            start_date=start_date
        )

        total_records = 0

        # Procesar cada evento
        for event in events:
            metadata_list = self._parse_calendar_event(event)

            for metadata in metadata_list:
                # Verificar si ya existe
                existing = self.db.query(CalendarEventMetadata).filter(
                    CalendarEventMetadata.id == metadata.id
                ).first()

                if not existing:
                    self.db.add(metadata)
                    total_records += 1

        # Commit al final
        self.db.commit()

        return total_records

    async def extract_organization_calendars(
        self,
        user_ids: List[str],
        max_events_per_user: Optional[int] = None
    ) -> Dict[str, int]:
        """
        Extraer metadata de calendarios de múltiples usuarios

        Args:
            user_ids: Lista de IDs de usuarios
            max_events_per_user: Máximo de eventos por usuario

        Returns:
            Dict con user_id: número_de_eventos_extraídos
        """
        results = {}

        for user_id in user_ids:
            try:
                count = await self.extract_user_calendar(
                    user_id=user_id,
                    max_events=max_events_per_user
                )
                results[user_id] = count
                print(f"✅ Usuario {user_id}: {count} eventos extraídos")

            except Exception as e:
                print(f"❌ Error extrayendo calendario de {user_id}: {str(e)}")
                results[user_id] = 0

        return results
