import tempfile

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Customer, Domain

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("/", summary="Create customer")
def create_customer(
    name: str,
    contact_email: str,
    sophos_api_mode: str = "customer",
    db: Session = Depends(get_db),
):
    customer = Customer(
        name=name,
        contact_email=contact_email,
        sophos_api_mode=sophos_api_mode,
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    placeholder_domain = Domain(
        customer_id=customer.id, domain=f"{name.lower()}.example.com"
    )
    db.add(placeholder_domain)
    db.commit()
    return {"id": customer.id, "name": customer.name}


@router.get("/", summary="List customers")
def list_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "contact_email": c.contact_email,
            "sophos_api_mode": c.sophos_api_mode,
        }
        for c in customers
    ]


@router.get("/export", summary="Export customers to PDF")
def export_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".pdf", mode="w", encoding="utf-8"
    ) as tmp:
        tmp.write("Customers\n")
        for c in customers:
            tmp.write(f"{c.id}: {c.name} <{c.contact_email}>\n")
        tmp_path = tmp.name
    return FileResponse(
        tmp_path, filename="customers.pdf", media_type="application/pdf"
    )
