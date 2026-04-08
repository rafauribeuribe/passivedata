"""
PassiveData API - Microsoft 365 Organizational Network Analysis
"""
import uuid
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from .config import settings
from .database import init_db, get_db, User, ExtractionJob
from .graph import get_auth_url, exchange_code_for_token, GraphClient
from .extractor import extract_emails, extract_calendar
from .analytics import get_network, get_stats, get_pairs

app = FastAPI(title="PassiveData API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


# ─── Status ───────────────────────────────────────────────────────────────────

@app.get("/api/status")
def status(db: Session = Depends(get_db)):
    from .database import EmailEdge, CalendarEdge
    from sqlalchemy import func
    admin = db.query(User).filter(User.is_admin == True).first()
    email_count = db.query(func.count(EmailEdge.id)).scalar()
    cal_count = db.query(func.count(CalendarEdge.id)).scalar()
    return {
        "configured": settings.configured,
        "authenticated": admin is not None,
        "admin_email": admin.email if admin else None,
        "email_records": email_count,
        "calendar_records": cal_count,
    }


# ─── Auth ─────────────────────────────────────────────────────────────────────

@app.get("/auth/login")
def login():
    if not settings.configured:
        raise HTTPException(400, "Azure no configurado. Edita el archivo .env")
    return {"url": get_auth_url()}


@app.get("/auth/callback")
async def callback(code: str, db: Session = Depends(get_db)):
    token_data = exchange_code_for_token(code)
    if not token_data:
        raise HTTPException(400, "Error al obtener token de Microsoft")

    token = token_data["access_token"]
    client = GraphClient(token)
    me = await client.get_me()

    email = (me.get("mail") or me.get("userPrincipalName") or "").lower()
    user = db.query(User).filter(User.id == me["id"]).first()
    if not user:
        user = User(id=me["id"], is_admin=True)
        db.add(user)

    user.email = email
    user.display_name = me.get("displayName", "")
    user.access_token = token
    user.refresh_token = token_data.get("refresh_token", "")
    db.commit()

    # Redirige al frontend con el token
    return RedirectResponse(
        url=f"http://localhost:3000?token={token}&email={email}&name={user.display_name}"
    )


@app.post("/auth/logout")
def logout(db: Session = Depends(get_db)):
    db.query(User).filter(User.is_admin == True).delete()
    db.commit()
    return {"ok": True}


# ─── Users ────────────────────────────────────────────────────────────────────

@app.get("/api/users")
async def list_org_users(db: Session = Depends(get_db)):
    admin = db.query(User).filter(User.is_admin == True).first()
    if not admin:
        raise HTTPException(401, "No autenticado")

    client = GraphClient(admin.access_token)
    users = await client.get_users()
    return {"users": users, "total": len(users)}


# ─── Extraction ───────────────────────────────────────────────────────────────

async def _run_extraction(job_id: str, job_type: str, token: str, user_ids: list[str], max_per_user: int):
    """Tarea de extracción en background"""
    db = next(get_db())
    job = db.get(ExtractionJob, job_id)
    try:
        client = GraphClient(token)
        total = 0
        for i, uid in enumerate(user_ids):
            try:
                if job_type == "emails":
                    n = await extract_emails(client, db, uid, max_per_user)
                else:
                    n = await extract_calendar(client, db, uid, max_per_user)
                total += n
                job.users_processed = i + 1
                job.records_found = total
                db.commit()
            except Exception as e:
                # Un usuario falla → continúa con el siguiente
                print(f"[extractor] usuario {uid} falló: {e}")
                continue

        job.status = "done"
        job.finished_at = datetime.utcnow()
        db.commit()
    except Exception as e:
        job.status = "error"
        job.error_message = str(e)
        job.finished_at = datetime.utcnow()
        db.commit()
    finally:
        db.close()


@app.post("/api/extract/{job_type}")
async def start_extraction(
    job_type: str,
    background_tasks: BackgroundTasks,
    days_back: int = Query(90, ge=1, le=365),
    max_per_user: int = Query(500, ge=10, le=2000),
    db: Session = Depends(get_db),
):
    if job_type not in ("emails", "calendar"):
        raise HTTPException(400, "job_type debe ser 'emails' o 'calendar'")

    admin = db.query(User).filter(User.is_admin == True).first()
    if not admin:
        raise HTTPException(401, "No autenticado")

    # Obtener lista de usuarios de la organización
    client = GraphClient(admin.access_token)
    try:
        org_users = await client.get_users()
        user_ids = [u["id"] for u in org_users if u.get("id")]
        if not user_ids:
            user_ids = [admin.id]
    except Exception:
        user_ids = [admin.id]

    job_id = str(uuid.uuid4())
    job = ExtractionJob(
        id=job_id,
        job_type=job_type,
        status="running",
        users_processed=0,
        records_found=0,
        started_at=datetime.utcnow(),
    )
    db.add(job)
    db.commit()

    background_tasks.add_task(
        _run_extraction, job_id, job_type, admin.access_token, user_ids, max_per_user
    )

    return {"job_id": job_id, "status": "running", "total_users": len(user_ids)}


@app.get("/api/extract/status/{job_id}")
def extraction_status(job_id: str, db: Session = Depends(get_db)):
    job = db.get(ExtractionJob, job_id)
    if not job:
        raise HTTPException(404, "Job no encontrado")
    return {
        "job_id": job.id,
        "job_type": job.job_type,
        "status": job.status,
        "users_processed": job.users_processed,
        "records_found": job.records_found,
        "error": job.error_message,
        "started_at": job.started_at,
        "finished_at": job.finished_at,
    }


# ─── Analytics ────────────────────────────────────────────────────────────────

@app.get("/api/network")
def network(
    source: str = Query("both", regex="^(email|calendar|both)$"),
    days: int = Query(90, ge=1, le=365),
    min_weight: int = Query(1, ge=1),
    db: Session = Depends(get_db),
):
    return get_network(db, source=source, days=days, min_weight=min_weight)


@app.get("/api/stats")
def stats(days: int = Query(90, ge=1, le=365), db: Session = Depends(get_db)):
    return get_stats(db, days=days)


@app.get("/api/pairs")
def pairs(
    days: int = Query(90, ge=1, le=365),
    top: int = Query(50, ge=5, le=200),
    db: Session = Depends(get_db),
):
    return get_pairs(db, days=days, top=top)


@app.get("/api/jobs")
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(ExtractionJob).order_by(ExtractionJob.started_at.desc()).limit(20).all()
    return {"jobs": [
        {"id": j.id, "type": j.job_type, "status": j.status,
         "users_processed": j.users_processed, "records_found": j.records_found,
         "started_at": j.started_at, "finished_at": j.finished_at}
        for j in jobs
    ]}
