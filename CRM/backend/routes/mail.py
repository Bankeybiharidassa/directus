import email
import imaplib
import logging
import os
from datetime import datetime
from email.header import decode_header

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import MailMessage

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/mail", tags=["mail"])


def _connect_imap():
    host = os.getenv("IMAP_HOST")
    user = os.getenv("IMAP_USER")
    password = os.getenv("IMAP_PASSWORD")
    if not all([host, user, password]):
        raise HTTPException(status_code=500, detail="IMAP credentials not configured")
    conn = imaplib.IMAP4_SSL(host)
    conn.login(user, password)
    return conn


@router.post("/sync", summary="Sync messages from IMAP server")
def sync_messages(db: Session = Depends(get_db)):
    conn = _connect_imap()
    conn.select("INBOX")
    status, ids = conn.search(None, "ALL")
    if status != "OK":
        raise HTTPException(status_code=500, detail="IMAP search failed")
    new_count = 0
    for msg_id in ids[0].split():
        status, data = conn.fetch(msg_id, "(BODY.PEEK[HEADER])")
        if status != "OK":
            continue
        msg = email.message_from_bytes(data[0][1])
        message_id = msg.get("Message-ID")
        if db.query(MailMessage).filter(MailMessage.message_id == message_id).first():
            continue
        subject, _ = decode_header(msg.get("Subject", ""))[0]
        if isinstance(subject, bytes):
            subject = subject.decode(errors="ignore")
        sender = msg.get("From", "")
        date_str = msg.get("Date")
        date_parsed = None
        try:
            date_parsed = (
                datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
                if date_str
                else None
            )
        except (ValueError, TypeError) as exc:
            logger.warning("Invalid date header %s: %s", date_str, exc)
        m = MailMessage(
            message_id=message_id, sender=sender, subject=subject, date=date_parsed
        )
        db.add(m)
        new_count += 1
    db.commit()
    conn.logout()
    return {"new_messages": new_count}


@router.get("/messages", summary="List mail messages")
def list_messages(db: Session = Depends(get_db)):
    messages = db.query(MailMessage).order_by(MailMessage.date.desc().nullslast()).all()
    return [
        {
            "id": m.id,
            "message_id": m.message_id,
            "sender": m.sender,
            "subject": m.subject,
            "date": m.date.isoformat() if m.date else None,
        }
        for m in messages
    ]
