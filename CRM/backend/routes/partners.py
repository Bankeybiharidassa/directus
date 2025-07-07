from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Partner

router = APIRouter(prefix="/partners", tags=["partners"])


@router.post("/", summary="Create partner")
def create_partner(
    name: str,
    parent_id: int | None = None,
    distributor_id: int | None = None,
    db: Session = Depends(get_db),
):
    partner = Partner(name=name, parent_id=parent_id, distributor_id=distributor_id)
    db.add(partner)
    db.commit()
    db.refresh(partner)
    return {
        "id": partner.id,
        "name": partner.name,
        "parent_id": partner.parent_id,
        "distributor_id": partner.distributor_id,
    }


@router.post("/{partner_id}/reassign", summary="Reassign partner parent")
def reassign_partner(
    partner_id: int,
    parent_id: int | None = None,
    distributor_id: int | None = None,
    db: Session = Depends(get_db),
):
    partner = db.get(Partner, partner_id)
    if not partner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Partner not found"
        )
    partner.parent_id = parent_id
    if distributor_id is not None:
        partner.distributor_id = distributor_id
    db.commit()
    db.refresh(partner)
    return {
        "id": partner.id,
        "name": partner.name,
        "parent_id": partner.parent_id,
        "distributor_id": partner.distributor_id,
    }


@router.get("/", summary="List partners")
def list_partners(db: Session = Depends(get_db)):
    partners = db.query(Partner).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "parent_id": p.parent_id,
            "distributor_id": p.distributor_id,
        }
        for p in partners
    ]
