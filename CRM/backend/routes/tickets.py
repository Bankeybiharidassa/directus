from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Ticket

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("/", summary="Create ticket")
def create_ticket(
    title: str,
    description: str,
    customer_id: int | None = None,
    db: Session = Depends(get_db),
):
    ticket = Ticket(title=title, description=description, customer_id=customer_id)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return {"id": ticket.id, "title": ticket.title, "status": ticket.status}


@router.get("/", summary="List tickets")
def list_tickets(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).all()
    return [
        {"id": t.id, "title": t.title, "status": t.status, "customer_id": t.customer_id}
        for t in tickets
    ]


@router.post("/{ticket_id}/close", summary="Close ticket")
def close_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found"
        )
    ticket.status = "closed"
    db.commit()
    db.refresh(ticket)
    return {"id": ticket.id, "title": ticket.title, "status": ticket.status}
