"""
Users Endpoints - Gestión de usuarios
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.models.user import User
from src.auth.graph_client import GraphClient
from src.auth.dependencies import get_current_user

router = APIRouter()


@router.get("/")
async def list_users(
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)  # Descomentar en producción
):
    """
    Listar usuarios de la organización almacenados en BD
    """
    users = db.query(User).all()

    return {
        "total": len(users),
        "users": [
            {
                "id": user.id,
                "email": user.email,
                "display_name": user.display_name,
                "job_title": user.job_title,
                "department": user.department,
                "is_admin": user.is_admin,
                "is_active": user.is_active,
                "last_login": user.last_login
            }
            for user in users
        ]
    }


@router.get("/sync")
async def sync_organization_users(
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_admin_user)  # Solo admins
):
    """
    Sincronizar usuarios de Microsoft Graph con la base de datos local
    """
    # Por ahora retornamos placeholder
    # En producción, obtendríamos el token del admin actual
    return {
        "message": "Endpoint para sincronizar usuarios de Microsoft Graph",
        "note": "Requiere autenticación de administrador"
    }


@router.get("/{user_id}")
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
):
    """
    Obtener información de un usuario específico
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "id": user.id,
        "email": user.email,
        "display_name": user.display_name,
        "job_title": user.job_title,
        "department": user.department,
        "is_admin": user.is_admin,
        "is_active": user.is_active,
        "created_at": user.created_at,
        "last_login": user.last_login
    }
