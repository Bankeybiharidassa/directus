from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Role, User, UserRole

router = APIRouter(prefix="/roles", tags=["roles"])


@router.post("/", summary="Create role")
def create_role(name: str, db: Session = Depends(get_db)):
    role = Role(name=name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return {"id": role.id, "name": role.name}


@router.get("/", summary="List roles")
def list_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return [{"id": r.id, "name": r.name} for r in roles]


@router.post("/{role_id}/assign/{user_id}", summary="Assign role to user")
def assign_role(role_id: int, user_id: int, db: Session = Depends(get_db)):
    if not db.get(Role, role_id) or not db.get(User, user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    link = UserRole(user_id=user_id, role_id=role_id)
    db.add(link)
    db.commit()
    db.refresh(link)
    return {"id": link.id, "user_id": link.user_id, "role_id": link.role_id}


@router.get("/user/{user_id}", summary="List user roles")
def list_user_roles(user_id: int, db: Session = Depends(get_db)):
    links = db.query(UserRole).filter(UserRole.user_id == user_id).all()
    roles = [db.get(Role, l.role_id) for l in links]
    return [{"id": r.id, "name": r.name} for r in roles]
