from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..services import crm_sync

router = APIRouter(prefix="/api/crm/sync", tags=["crm-sync"])


@router.post("/import", summary="Import tenants and users from external CRM")
def import_data(source_url: str | None = None, db: Session = Depends(get_db)):
    count = crm_sync.import_from_external(db, url=source_url)
    return {"imported": count}
