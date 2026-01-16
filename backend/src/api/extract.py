"""
Data Extraction Endpoints - Extracción de metadata
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from src.core.database import get_db
from src.models.user import User
from src.extractors.email_extractor import EmailExtractor
from src.extractors.calendar_extractor import CalendarExtractor
from src.extractors.teams_extractor import TeamsExtractor
from src.auth.dependencies import get_current_admin_user

router = APIRouter()


class ExtractEmailsRequest(BaseModel):
    """Request para extraer emails"""
    user_ids: Optional[List[str]] = None  # Si es None, extrae de todos los usuarios
    max_emails_per_user: Optional[int] = 1000
    days_back: int = 90


class ExtractCalendarRequest(BaseModel):
    """Request para extraer calendario"""
    user_ids: Optional[List[str]] = None
    max_events_per_user: Optional[int] = 1000
    days_back: int = 90


class ExtractTeamsRequest(BaseModel):
    """Request para extraer Teams"""
    user_ids: Optional[List[str]] = None
    max_messages_per_chat: int = 100
    max_chats: int = 50


@router.post("/emails")
async def extract_emails(
    request: ExtractEmailsRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin_user)  # Solo admins
):
    """
    Extraer metadata de correos electrónicos
    """
    # Placeholder - en producción obtendríamos el token del admin actual
    return {
        "message": "Extracción de emails iniciada",
        "status": "processing",
        "note": "En producción, esto ejecutaría la extracción en background",
        "parameters": {
            "user_ids": request.user_ids or "all",
            "max_emails_per_user": request.max_emails_per_user,
            "days_back": request.days_back
        }
    }


@router.post("/calendar")
async def extract_calendar(
    request: ExtractCalendarRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin_user)
):
    """
    Extraer metadata de eventos de calendario
    """
    return {
        "message": "Extracción de calendario iniciada",
        "status": "processing",
        "note": "En producción, esto ejecutaría la extracción en background",
        "parameters": {
            "user_ids": request.user_ids or "all",
            "max_events_per_user": request.max_events_per_user,
            "days_back": request.days_back
        }
    }


@router.post("/teams")
async def extract_teams(
    request: ExtractTeamsRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin_user)
):
    """
    Extraer metadata de chats de Microsoft Teams
    """
    return {
        "message": "Extracción de Teams iniciada",
        "status": "processing",
        "note": "En producción, esto ejecutaría la extracción en background",
        "parameters": {
            "user_ids": request.user_ids or "all",
            "max_messages_per_chat": request.max_messages_per_chat,
            "max_chats": request.max_chats
        }
    }


@router.get("/status/{task_id}")
async def get_extraction_status(
    task_id: str,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
):
    """
    Obtener estado de una tarea de extracción
    """
    return {
        "task_id": task_id,
        "status": "completed",
        "progress": 100,
        "message": "Extracción completada",
        "note": "En producción, esto consultaría el estado real de la tarea"
    }
