from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Page, User

router = APIRouter(prefix="/pages", tags=["cms"])


@router.post("/", summary="Create page")
def create_page(slug: str, content: str = "", db: Session = Depends(get_db)):
    page = Page(slug=slug, content=content)
    db.add(page)
    db.commit()
    db.refresh(page)
    return {"id": page.id, "slug": page.slug, "published": page.published}


@router.get("/", summary="List pages")
def list_pages(db: Session = Depends(get_db)):
    pages = db.query(Page).all()
    return [{"id": p.id, "slug": p.slug, "published": p.published} for p in pages]


@router.post("/{page_id}/publish", summary="Publish page")
def publish_page(page_id: int, db: Session = Depends(get_db)):
    page = db.get(Page, page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    page.published = True
    db.commit()
    db.refresh(page)
    return {"id": page.id, "slug": page.slug, "published": page.published}


@router.post("/portal/revoke/{user_id}", summary="Revoke portal access")
def revoke_portal_access(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.portal_access = False
    db.commit()
    db.refresh(user)
    return {"id": user.id, "portal_access": user.portal_access}
