"""
Authentication Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime

from src.core.database import get_db
from src.auth.msal_handler import msal_handler
from src.auth.graph_client import GraphClient
from src.models.user import User

router = APIRouter()


@router.get("/login")
async def login():
    """
    Iniciar sesión con Microsoft
    Redirige a la página de autorización de Microsoft
    """
    # Generar URL de autorización
    auth_url = msal_handler.get_authorization_url(state="random_state_string")

    return {
        "auth_url": auth_url,
        "message": "Redirigir al usuario a esta URL para autenticación"
    }


@router.get("/callback")
async def auth_callback(
    code: str,
    state: str = None,
    db: Session = Depends(get_db)
):
    """
    Callback de OAuth
    Microsoft redirige aquí después de la autenticación
    """
    if not code:
        raise HTTPException(status_code=400, detail="No se recibió código de autorización")

    # Adquirir token con el código
    token_result = msal_handler.acquire_token_by_auth_code(code)

    if not token_result:
        raise HTTPException(status_code=401, detail="Error al obtener token de acceso")

    access_token = token_result["access_token"]
    refresh_token = token_result.get("refresh_token")
    expires_at = token_result["expires_at"]

    # Obtener perfil del usuario
    graph_client = GraphClient(access_token)
    profile = await graph_client.get_user_profile()

    if not profile:
        raise HTTPException(status_code=401, detail="Error al obtener perfil del usuario")

    # Guardar o actualizar usuario en base de datos
    user_id = profile.get("id")
    email = profile.get("mail") or profile.get("userPrincipalName")
    display_name = profile.get("displayName")
    job_title = profile.get("jobTitle")
    department = profile.get("department")

    # Buscar usuario existente
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        # Actualizar usuario existente
        user.access_token = access_token
        user.refresh_token = refresh_token
        user.token_expires_at = expires_at
        user.last_login = datetime.utcnow()
        user.display_name = display_name
        user.job_title = job_title
        user.department = department
    else:
        # Crear nuevo usuario
        user = User(
            id=user_id,
            email=email,
            display_name=display_name,
            job_title=job_title,
            department=department,
            access_token=access_token,
            refresh_token=refresh_token,
            token_expires_at=expires_at,
            last_login=datetime.utcnow(),
            is_admin=True,  # El primer usuario es admin
            is_active=True
        )
        db.add(user)

    db.commit()
    db.refresh(user)

    # En producción, redirigir al frontend con el token
    return {
        "message": "Autenticación exitosa",
        "user": {
            "id": user.id,
            "email": user.email,
            "display_name": user.display_name,
            "is_admin": user.is_admin
        },
        "access_token": access_token,
        "token_type": "Bearer"
    }


@router.post("/logout")
async def logout(db: Session = Depends(get_db), current_user: User = None):
    """
    Cerrar sesión
    Elimina tokens del usuario
    """
    # En una implementación real, buscaríamos el usuario por token
    # Por ahora, solo retornamos mensaje de éxito
    return {"message": "Sesión cerrada exitosamente"}


@router.get("/me")
async def get_current_user_info(
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)  # Descomentado en producción
):
    """
    Obtener información del usuario actual
    """
    # Por ahora retornamos un placeholder
    # En producción, usaríamos el dependency get_current_user
    return {
        "message": "Endpoint para obtener información del usuario actual",
        "note": "Implementar autenticación completa en producción"
    }
