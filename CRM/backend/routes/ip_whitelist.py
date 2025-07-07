from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import WhitelistedIP

router = APIRouter(prefix="/whitelisted_ips", tags=["security"])


@router.post("/", summary="Add entry to whitelist")
def add_entry(entry: str, db: Session = Depends(get_db)):
    record = WhitelistedIP(pattern=entry)
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"id": record.id, "pattern": record.pattern}


@router.get("/", summary="List whitelist entries")
def list_entries(db: Session = Depends(get_db)):
    entries = db.query(WhitelistedIP).all()
    return [{"id": i.id, "pattern": i.pattern} for i in entries]
