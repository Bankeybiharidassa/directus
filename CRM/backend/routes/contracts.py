from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Contract

router = APIRouter(prefix="/contracts", tags=["contracts"])


@router.post("/", summary="Create contract")
def create_contract(
    customer_id: int, description: str = "", db: Session = Depends(get_db)
):
    contract = Contract(customer_id=customer_id, description=description)
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return {
        "id": contract.id,
        "customer_id": contract.customer_id,
        "status": contract.status,
    }


@router.get("/", summary="List contracts")
def list_contracts(db: Session = Depends(get_db)):
    contracts = db.query(Contract).all()
    return [
        {
            "id": c.id,
            "customer_id": c.customer_id,
            "description": c.description,
            "status": c.status,
        }
        for c in contracts
    ]


@router.post("/{contract_id}/close", summary="Close contract")
def close_contract(contract_id: int, db: Session = Depends(get_db)):
    contract = db.get(Contract, contract_id)
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contract not found"
        )
    contract.status = "closed"
    db.commit()
    db.refresh(contract)
    return {"id": contract.id, "status": contract.status}
