"""
Data Query Endpoints - Consulta de datos extraídos
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import Optional, List
from datetime import datetime, timedelta

from src.core.database import get_db
from src.models.email import EmailMetadata
from src.models.calendar import CalendarEventMetadata
from src.models.teams import TeamsMessageMetadata
from src.auth.dependencies import get_current_user

router = APIRouter()


@router.get("/emails")
async def get_emails(
    skip: int = 0,
    limit: int = 100,
    sender_email: Optional[str] = None,
    recipient_email: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_user)
):
    """
    Obtener metadata de correos electrónicos
    """
    query = db.query(EmailMetadata)

    # Filtros opcionales
    if sender_email:
        query = query.filter(EmailMetadata.sender_email == sender_email)

    if recipient_email:
        query = query.filter(EmailMetadata.recipient_email == recipient_email)

    if start_date:
        start_dt = datetime.fromisoformat(start_date)
        query = query.filter(EmailMetadata.sent_datetime >= start_dt)

    if end_date:
        end_dt = datetime.fromisoformat(end_date)
        query = query.filter(EmailMetadata.sent_datetime <= end_dt)

    # Paginación
    total = query.count()
    emails = query.order_by(EmailMetadata.sent_datetime.desc()).offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "emails": [
            {
                "id": email.id,
                "sender_email": email.sender_email,
                "sender_name": email.sender_name,
                "recipient_email": email.recipient_email,
                "recipient_name": email.recipient_name,
                "sent_datetime": email.sent_datetime,
                "has_attachments": email.has_attachments,
                "importance": email.importance
            }
            for email in emails
        ]
    }


@router.get("/calendar")
async def get_calendar_events(
    skip: int = 0,
    limit: int = 100,
    organizer_email: Optional[str] = None,
    participant_email: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_user)
):
    """
    Obtener metadata de eventos de calendario
    """
    query = db.query(CalendarEventMetadata)

    # Filtros opcionales
    if organizer_email:
        query = query.filter(CalendarEventMetadata.organizer_email == organizer_email)

    if participant_email:
        query = query.filter(CalendarEventMetadata.participant_email == participant_email)

    if start_date:
        start_dt = datetime.fromisoformat(start_date)
        query = query.filter(CalendarEventMetadata.start_datetime >= start_dt)

    if end_date:
        end_dt = datetime.fromisoformat(end_date)
        query = query.filter(CalendarEventMetadata.start_datetime <= end_dt)

    # Paginación
    total = query.count()
    events = query.order_by(CalendarEventMetadata.start_datetime.desc()).offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "events": [
            {
                "id": event.id,
                "organizer_email": event.organizer_email,
                "organizer_name": event.organizer_name,
                "participant_email": event.participant_email,
                "participant_name": event.participant_name,
                "start_datetime": event.start_datetime,
                "duration_minutes": event.duration_minutes,
                "is_online_meeting": event.is_online_meeting
            }
            for event in events
        ]
    }


@router.get("/teams")
async def get_teams_messages(
    skip: int = 0,
    limit: int = 100,
    sender_email: Optional[str] = None,
    chat_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_user)
):
    """
    Obtener metadata de mensajes de Teams
    """
    query = db.query(TeamsMessageMetadata)

    # Filtros opcionales
    if sender_email:
        query = query.filter(TeamsMessageMetadata.sender_email == sender_email)

    if chat_type:
        query = query.filter(TeamsMessageMetadata.chat_type == chat_type)

    if start_date:
        start_dt = datetime.fromisoformat(start_date)
        query = query.filter(TeamsMessageMetadata.created_datetime >= start_dt)

    if end_date:
        end_dt = datetime.fromisoformat(end_date)
        query = query.filter(TeamsMessageMetadata.created_datetime <= end_dt)

    # Paginación
    total = query.count()
    messages = query.order_by(TeamsMessageMetadata.created_datetime.desc()).offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "messages": [
            {
                "id": msg.id,
                "chat_id": msg.chat_id,
                "chat_type": msg.chat_type,
                "sender_email": msg.sender_email,
                "sender_name": msg.sender_name,
                "created_datetime": msg.created_datetime,
                "has_attachments": msg.has_attachments
            }
            for msg in messages
        ]
    }


@router.get("/stats")
async def get_statistics(
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_user)
):
    """
    Obtener estadísticas generales de los datos
    """
    # Contar totales
    total_emails = db.query(EmailMetadata).count()
    total_calendar = db.query(CalendarEventMetadata).count()
    total_teams = db.query(TeamsMessageMetadata).count()

    # Top comunicadores por email
    top_senders = db.query(
        EmailMetadata.sender_email,
        func.count(EmailMetadata.id).label('count')
    ).group_by(EmailMetadata.sender_email).order_by(func.count(EmailMetadata.id).desc()).limit(10).all()

    # Top organizadores de reuniones
    top_organizers = db.query(
        CalendarEventMetadata.organizer_email,
        func.count(CalendarEventMetadata.id).label('count')
    ).group_by(CalendarEventMetadata.organizer_email).order_by(func.count(CalendarEventMetadata.id).desc()).limit(10).all()

    return {
        "totals": {
            "emails": total_emails,
            "calendar_events": total_calendar,
            "teams_messages": total_teams
        },
        "top_email_senders": [
            {"email": sender, "count": count}
            for sender, count in top_senders
        ],
        "top_meeting_organizers": [
            {"email": organizer, "count": count}
            for organizer, count in top_organizers
        ]
    }


@router.get("/communication-network")
async def get_communication_network(
    days_back: int = 30,
    min_interactions: int = 1,
    db: Session = Depends(get_db),
    # current_user = Depends(get_current_user)
):
    """
    Obtener red de comunicación (quién se comunica con quién)
    Útil para visualizaciones de red
    """
    start_date = datetime.utcnow() - timedelta(days=days_back)

    # Comunicación por email
    email_connections = db.query(
        EmailMetadata.sender_email,
        EmailMetadata.recipient_email,
        func.count(EmailMetadata.id).label('count')
    ).filter(
        EmailMetadata.sent_datetime >= start_date
    ).group_by(
        EmailMetadata.sender_email,
        EmailMetadata.recipient_email
    ).having(
        func.count(EmailMetadata.id) >= min_interactions
    ).all()

    # Comunicación por reuniones
    meeting_connections = db.query(
        CalendarEventMetadata.organizer_email,
        CalendarEventMetadata.participant_email,
        func.count(CalendarEventMetadata.id).label('count')
    ).filter(
        CalendarEventMetadata.start_datetime >= start_date
    ).group_by(
        CalendarEventMetadata.organizer_email,
        CalendarEventMetadata.participant_email
    ).having(
        func.count(CalendarEventMetadata.id) >= min_interactions
    ).all()

    return {
        "email_network": [
            {
                "from": sender,
                "to": recipient,
                "count": count,
                "type": "email"
            }
            for sender, recipient, count in email_connections
        ],
        "meeting_network": [
            {
                "from": organizer,
                "to": participant,
                "count": count,
                "type": "meeting"
            }
            for organizer, participant, count in meeting_connections
        ]
    }
