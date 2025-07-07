from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..security.auth import authenticate, require_roles

router = APIRouter(prefix="/support", tags=["support"])


@router.post("/authorize", summary="Authorize remote support")
def authorize(
    current_user: User = Depends(authenticate), db: Session = Depends(get_db)
):
    current_user.remote_access_enabled = True
    db.commit()
    db.refresh(current_user)
    return {"authorized": True}


@router.post("/revoke", summary="Revoke remote support")
def revoke(current_user: User = Depends(authenticate), db: Session = Depends(get_db)):
    current_user.remote_access_enabled = False
    db.commit()
    db.refresh(current_user)
    return {"authorized": False}


@router.post("/login_as/{user_id}", summary="Impersonate user")
def login_as(
    user_id: int,
    current_user: User = Depends(require_roles(["support", "audit"])),
    db: Session = Depends(get_db),
):
    target = db.get(User, user_id)
    if not target or not target.remote_access_enabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Remote access not authorized"
        )
    with open("logs/remote_access.log", "a", encoding="utf-8") as fh:
        log_line = (
            f"{datetime.now(timezone.utc).isoformat()} "
            f"{current_user.username} -> {target.username}\n"
        )
        fh.write(log_line)
    return {"id": target.id, "username": target.username}
