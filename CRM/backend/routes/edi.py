from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import EdiMessage
from ..security.auth import require_role, require_roles

router = APIRouter(prefix="/edi", tags=["edi"])


class EdiRequest(BaseModel):
    """Payload for an EDI message."""

    sender_type: str
    sender_id: int
    receiver_type: str
    receiver_id: int
    content: str


@router.post("/", summary="Send EDI message")
def send_message(
    req: EdiRequest,
    db: Session = Depends(get_db),
    _current_user=Depends(require_roles(["distributor", "partner"])),
):
    msg = EdiMessage(
        sender_type=req.sender_type,
        sender_id=req.sender_id,
        receiver_type=req.receiver_type,
        receiver_id=req.receiver_id,
        content=req.content,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return {"id": msg.id}


@router.get("/", summary="List EDI messages")
def list_messages(
    db: Session = Depends(get_db),
    _current_user=Depends(require_role("admin")),
):
    msgs = db.query(EdiMessage).all()
    return [
        {
            "id": m.id,
            "sender_type": m.sender_type,
            "sender_id": m.sender_id,
            "receiver_type": m.receiver_type,
            "receiver_id": m.receiver_id,
            "content": m.content,
        }
        for m in msgs
    ]
