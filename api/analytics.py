"""Consultas analíticas sobre la red organizacional"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from collections import defaultdict

from .database import EmailEdge, CalendarEdge, User


def get_network(db: Session, source: str = "both", days: int = 90, min_weight: int = 1) -> dict:
    """
    Retorna nodos y aristas para visualizar la red organizacional.
    source: 'email', 'calendar' o 'both'
    """
    since = datetime.utcnow() - timedelta(days=days)
    edge_weights = defaultdict(lambda: {"email": 0, "calendar": 0})

    if source in ("email", "both"):
        rows = (
            db.query(EmailEdge.sender, EmailEdge.recipient, func.count().label("n"))
            .filter(EmailEdge.sent_at >= since)
            .group_by(EmailEdge.sender, EmailEdge.recipient)
            .all()
        )
        for sender, recipient, n in rows:
            key = (sender, recipient)
            edge_weights[key]["email"] += n

    if source in ("calendar", "both"):
        rows = (
            db.query(CalendarEdge.organizer, CalendarEdge.participant, func.count().label("n"))
            .filter(CalendarEdge.start_at >= since)
            .group_by(CalendarEdge.organizer, CalendarEdge.participant)
            .all()
        )
        for org, part, n in rows:
            key = (org, part)
            edge_weights[key]["calendar"] += n

    # Construir aristas filtradas
    edges = []
    nodes_set = set()
    for (src, tgt), weights in edge_weights.items():
        total = weights["email"] + weights["calendar"]
        if total < min_weight:
            continue
        edges.append({
            "source": src,
            "target": tgt,
            "email_count": weights["email"],
            "calendar_count": weights["calendar"],
            "total": total,
        })
        nodes_set.add(src)
        nodes_set.add(tgt)

    # Calcular grado de cada nodo
    degree = defaultdict(int)
    for e in edges:
        degree[e["source"]] += e["total"]
        degree[e["target"]] += e["total"]

    # Enriquecer con info de usuarios si existe
    users_map = {}
    for u in db.query(User).all():
        if u.email:
            users_map[u.email.lower()] = u

    nodes = []
    for email in nodes_set:
        u = users_map.get(email)
        nodes.append({
            "id": email,
            "label": u.display_name if u else email.split("@")[0],
            "department": u.department if u else "",
            "job_title": u.job_title if u else "",
            "degree": degree[email],
        })

    # Ordenar nodos por grado descendente
    nodes.sort(key=lambda x: x["degree"], reverse=True)

    return {"nodes": nodes, "edges": edges}


def get_stats(db: Session, days: int = 90) -> dict:
    since = datetime.utcnow() - timedelta(days=days)

    total_emails = db.query(func.count(EmailEdge.id)).filter(EmailEdge.sent_at >= since).scalar()
    total_meetings = db.query(func.count(CalendarEdge.id)).filter(CalendarEdge.start_at >= since).scalar()
    unique_email_senders = db.query(func.count(func.distinct(EmailEdge.sender))).filter(EmailEdge.sent_at >= since).scalar()
    unique_meeting_organizers = db.query(func.count(func.distinct(CalendarEdge.organizer))).filter(CalendarEdge.start_at >= since).scalar()

    # Top comunicadores por email
    top_senders = (
        db.query(EmailEdge.sender, func.count().label("n"))
        .filter(EmailEdge.sent_at >= since)
        .group_by(EmailEdge.sender)
        .order_by(func.count().desc())
        .limit(10)
        .all()
    )

    # Top organizadores de reuniones
    top_organizers = (
        db.query(CalendarEdge.organizer, func.count().label("n"))
        .filter(CalendarEdge.start_at >= since)
        .group_by(CalendarEdge.organizer)
        .order_by(func.count().desc())
        .limit(10)
        .all()
    )

    # Actividad por hora del día (emails)
    by_hour_email = (
        db.query(EmailEdge.hour_of_day, func.count().label("n"))
        .filter(EmailEdge.sent_at >= since)
        .group_by(EmailEdge.hour_of_day)
        .all()
    )
    email_by_hour = {h: n for h, n in by_hour_email}

    # Actividad por hora del día (reuniones)
    by_hour_cal = (
        db.query(CalendarEdge.hour_of_day, func.count().label("n"))
        .filter(CalendarEdge.start_at >= since)
        .group_by(CalendarEdge.hour_of_day)
        .all()
    )
    cal_by_hour = {h: n for h, n in by_hour_cal}

    hours = [{"hour": h,
              "emails": email_by_hour.get(h, 0),
              "meetings": cal_by_hour.get(h, 0)} for h in range(24)]

    # Actividad por día de semana
    days_names = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
    by_dow_email = {d: n for d, n in db.query(EmailEdge.day_of_week, func.count())
                    .filter(EmailEdge.sent_at >= since).group_by(EmailEdge.day_of_week).all()}
    by_dow_cal = {d: n for d, n in db.query(CalendarEdge.day_of_week, func.count())
                  .filter(CalendarEdge.start_at >= since).group_by(CalendarEdge.day_of_week).all()}

    by_dow = [{"day": days_names[d],
               "emails": by_dow_email.get(d, 0),
               "meetings": by_dow_cal.get(d, 0)} for d in range(7)]

    return {
        "totals": {
            "emails": total_emails,
            "meetings": total_meetings,
            "email_senders": unique_email_senders,
            "meeting_organizers": unique_meeting_organizers,
        },
        "top_senders": [{"email": e, "count": n} for e, n in top_senders],
        "top_organizers": [{"email": e, "count": n} for e, n in top_organizers],
        "activity_by_hour": hours,
        "activity_by_dow": by_dow,
    }


def get_pairs(db: Session, days: int = 90, top: int = 50) -> dict:
    """Pares más frecuentes de comunicación (email + reuniones combinados)"""
    since = datetime.utcnow() - timedelta(days=days)

    email_pairs = {
        (a, b): n for a, b, n in
        db.query(EmailEdge.sender, EmailEdge.recipient, func.count())
        .filter(EmailEdge.sent_at >= since)
        .group_by(EmailEdge.sender, EmailEdge.recipient)
        .all()
    }
    cal_pairs = {
        (a, b): n for a, b, n in
        db.query(CalendarEdge.organizer, CalendarEdge.participant, func.count())
        .filter(CalendarEdge.start_at >= since)
        .group_by(CalendarEdge.organizer, CalendarEdge.participant)
        .all()
    }

    all_pairs = set(email_pairs) | set(cal_pairs)
    rows = sorted(
        [{"from": a, "to": b,
          "emails": email_pairs.get((a, b), 0),
          "meetings": cal_pairs.get((a, b), 0),
          "total": email_pairs.get((a, b), 0) + cal_pairs.get((a, b), 0)}
         for a, b in all_pairs],
        key=lambda x: x["total"], reverse=True
    )

    return {"pairs": rows[:top]}
