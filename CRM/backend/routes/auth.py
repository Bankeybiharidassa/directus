import pyotp
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..security.auth import authenticate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", summary="Create user")
def create_user(username: str, password: str, db: Session = Depends(get_db)):
    user = User(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "username": user.username}


@router.get("/me", summary="Get current user")
def read_current_user(current_user: User = Depends(authenticate)):
    return {"id": current_user.id, "username": current_user.username}


@router.post("/{user_id}/enforce_mfa", summary="Enforce MFA for user")
def enforce_mfa(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    secret = pyotp.random_base32()
    user.mfa_enabled = True
    user.mfa_secret = secret
    db.commit()
    db.refresh(user)
    return {"id": user.id, "mfa_enabled": user.mfa_enabled, "secret": secret}
