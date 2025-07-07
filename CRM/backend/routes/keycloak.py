from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import KeycloakConfig

router = APIRouter(prefix="/keycloak", tags=["keycloak"])


@router.post("/", summary="Configure Keycloak")
def set_keycloak(
    url: str,
    realm: str,
    client_id: str,
    client_secret: str,
    db: Session = Depends(get_db),
):
    cfg = db.query(KeycloakConfig).first()
    if cfg:
        cfg.url = url
        cfg.realm = realm
        cfg.client_id = client_id
        cfg.client_secret = client_secret
    else:
        cfg = KeycloakConfig(
            url=url, realm=realm, client_id=client_id, client_secret=client_secret
        )
        db.add(cfg)
    db.commit()
    return {"url": cfg.url, "realm": cfg.realm, "client_id": cfg.client_id}


@router.get("/", summary="Get Keycloak config")
def get_keycloak(db: Session = Depends(get_db)):
    cfg = db.query(KeycloakConfig).first()
    if not cfg:
        return {}
    return {"url": cfg.url, "realm": cfg.realm, "client_id": cfg.client_id}
