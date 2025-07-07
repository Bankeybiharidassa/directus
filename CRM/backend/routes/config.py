from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ApiConfig

router = APIRouter(prefix="/config", tags=["config"])

AVAILABLE_MODELS = ["gpt-4", "gpt-3.5-turbo"]


@router.post("/api", summary="Save API configuration")
def save_api_config(api_key: str, model: str, db: Session = Depends(get_db)):
    config = db.query(ApiConfig).first()
    if config:
        config.api_key = api_key
        config.model = model
    else:
        config = ApiConfig(api_key=api_key, model=model)
        db.add(config)
    db.commit()
    db.refresh(config)
    return {"id": config.id, "model": config.model}


@router.get("/api", summary="Get API configuration")
def get_api_config(db: Session = Depends(get_db)):
    config = db.query(ApiConfig).first()
    if not config:
        return {}
    return {"id": config.id, "model": config.model}


@router.get("/models", summary="List available models")
def list_models():
    return AVAILABLE_MODELS
