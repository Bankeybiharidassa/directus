"""Case management routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Case

router = APIRouter(prefix="/cases", tags=["cases"])


@router.post("/", summary="Create case")
def create_case(
    title: str,
    description: str = "",
    namespace: str = "default",
    db: Session = Depends(get_db),
):
    """Create a new case."""
    case = Case(title=title, description=description, namespace=namespace)
    db.add(case)
    db.commit()
    db.refresh(case)
    return {"id": case.id, "title": case.title, "namespace": case.namespace}


@router.get("/", summary="List cases")
def list_cases(namespace: str | None = None, db: Session = Depends(get_db)):
    """List cases, optionally filtering by namespace."""
    query = db.query(Case)
    if namespace:
        query = query.filter(Case.namespace == namespace)
    cases = query.all()
    return [
        {
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "namespace": c.namespace,
        }
        for c in cases
    ]


@router.get("/search", summary="Search cases")
def search_cases(q: str, namespace: str | None = None, db: Session = Depends(get_db)):
    """Search cases by title or description."""
    query = db.query(Case).filter(Case.title.contains(q) | Case.description.contains(q))
    if namespace:
        query = query.filter(Case.namespace == namespace)
    cases = query.all()
    return [
        {
            "id": c.id,
            "title": c.title,
            "namespace": c.namespace,
        }
        for c in cases
    ]
