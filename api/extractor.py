"""Extrae metadata de Graph API y la guarda en SQLite"""
import hashlib
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from .database import EmailEdge, CalendarEdge
from .graph import GraphClient


def _make_id(*parts) -> str:
    raw = "|".join(str(p) for p in parts)
    return hashlib.md5(raw.encode()).hexdigest()


def _parse_dt(s: Optional[str]) -> Optional[datetime]:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).replace(tzinfo=None)
    except Exception:
        return None


async def extract_emails(client: GraphClient, db: Session, user_id: str, max_items: int = 500) -> int:
    messages = await client.get_messages(user_id, top=max_items)
    count = 0
    for msg in messages:
        sender_obj = msg.get("sender", {}).get("emailAddress", {})
        sender = sender_obj.get("address", "").lower()
        if not sender:
            continue

        sent_dt = _parse_dt(msg.get("sentDateTime"))
        if not sent_dt:
            continue

        for rec in msg.get("toRecipients", []):
            recipient = rec.get("emailAddress", {}).get("address", "").lower()
            if not recipient or recipient == sender:
                continue

            edge_id = _make_id(msg.get("id", ""), recipient)
            if db.get(EmailEdge, edge_id):
                continue

            edge = EmailEdge(
                id=edge_id,
                sender=sender,
                recipient=recipient,
                sent_at=sent_dt,
                hour_of_day=sent_dt.hour,
                day_of_week=sent_dt.weekday(),
                has_attachments=msg.get("hasAttachments", False),
                importance=msg.get("importance", "normal"),
            )
            db.add(edge)
            count += 1

    db.commit()
    return count


async def extract_calendar(client: GraphClient, db: Session, user_id: str, max_items: int = 500) -> int:
    events = await client.get_calendar_events(user_id, top=max_items)
    count = 0
    for ev in events:
        if ev.get("isCancelled"):
            continue

        org_obj = ev.get("organizer", {}).get("emailAddress", {})
        organizer = org_obj.get("address", "").lower()
        if not organizer:
            continue

        start_dt = _parse_dt(ev.get("start", {}).get("dateTime"))
        end_dt = _parse_dt(ev.get("end", {}).get("dateTime"))
        if not start_dt:
            continue

        duration = int((end_dt - start_dt).total_seconds() / 60) if end_dt else 0

        for att in ev.get("attendees", []):
            participant = att.get("emailAddress", {}).get("address", "").lower()
            if not participant or participant == organizer:
                continue
            # Solo contar quienes aceptaron
            response = att.get("status", {}).get("response", "")
            if response == "declined":
                continue

            edge_id = _make_id(ev.get("id", ""), participant)
            if db.get(CalendarEdge, edge_id):
                continue

            edge = CalendarEdge(
                id=edge_id,
                organizer=organizer,
                participant=participant,
                start_at=start_dt,
                duration_minutes=duration,
                hour_of_day=start_dt.hour,
                day_of_week=start_dt.weekday(),
                is_online=ev.get("isOnlineMeeting", False),
                is_recurring=bool(ev.get("recurrence")),
            )
            db.add(edge)
            count += 1

    db.commit()
    return count
