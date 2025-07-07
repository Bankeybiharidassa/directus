"""Distributor API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Distributor

router = APIRouter(prefix="/distributors", tags=["distributors"])


@router.post("/", summary="Create distributor")
def create_distributor(name: str, db: Session = Depends(get_db)):
    """Create a new distributor."""
    d = Distributor(name=name)
    db.add(d)
    db.commit()
    db.refresh(d)
    return {"id": d.id, "name": d.name}


@router.get("/", summary="List distributors")
def list_distributors(db: Session = Depends(get_db)):
    """List all distributors."""
    distributors = db.query(Distributor).all()
    return [{"id": d.id, "name": d.name} for d in distributors]
