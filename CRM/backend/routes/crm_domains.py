from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Customer, Domain


router = APIRouter(prefix="/api/crm/domains", tags=["crm-domains"])


class DomainCreate(BaseModel):
    """Payload for creating a tenant domain."""  # pylint: disable=too-few-public-methods

    domain: str
    imap_host: str | None = None
    imap_user: str | None = None
    imap_password: str | None = None
    smtp_host: str | None = None
    smtp_user: str | None = None
    smtp_password: str | None = None


@router.post("/", summary="Add domain to tenant")
def add_domain(
    tenant_id: int,
    payload: DomainCreate,
    db: Session = Depends(get_db),
):
    if not db.query(Customer).filter(Customer.id == tenant_id).first():
        raise HTTPException(status_code=404, detail="Tenant not found")
    d = Domain(
        customer_id=tenant_id,
        domain=payload.domain,
        imap_host=payload.imap_host,
        imap_user=payload.imap_user,
        imap_password=payload.imap_password,
        smtp_host=payload.smtp_host,
        smtp_user=payload.smtp_user,
        smtp_password=payload.smtp_password,
    )
    db.add(d)
    db.commit()
    db.refresh(d)
    return {
        "id": d.id,
        "tenant_id": d.customer_id,
        "domain": d.domain,
        "imap_host": d.imap_host,
        "imap_user": d.imap_user,
        "smtp_host": d.smtp_host,
        "smtp_user": d.smtp_user,
    }


@router.get("/{tenant_id}", summary="List domains for tenant")
def list_domains(tenant_id: int, db: Session = Depends(get_db)):
    domains = db.query(Domain).filter(Domain.customer_id == tenant_id).all()
    return [
        {
            "id": d.id,
            "tenant_id": d.customer_id,
            "domain": d.domain,
            "imap_host": d.imap_host,
            "imap_user": d.imap_user,
            "smtp_host": d.smtp_host,
            "smtp_user": d.smtp_user,
        }
        for d in domains
    ]
