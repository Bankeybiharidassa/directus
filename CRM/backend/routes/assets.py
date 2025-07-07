from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from scripts import sophos_sync, tenable_sync

from ..database import get_db
from ..models import Asset, Vulnerability

router = APIRouter(prefix="/assets", tags=["assets"])


@router.post("/", summary="Create asset")
def create_asset(hostname: str, status: str = "unknown", db: Session = Depends(get_db)):
    asset = Asset(hostname=hostname, status=status)
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return {"id": asset.id, "hostname": asset.hostname, "status": asset.status}


@router.get("/", summary="List assets")
def list_assets(db: Session = Depends(get_db)):
    assets = db.query(Asset).all()
    return [{"id": a.id, "hostname": a.hostname, "status": a.status} for a in assets]


@router.post("/{asset_id}/vulnerabilities", summary="Add vulnerability to asset")
def add_vulnerability(
    asset_id: int,
    description: str,
    severity: str = "low",
    db: Session = Depends(get_db),
):
    vuln = Vulnerability(asset_id=asset_id, description=description, severity=severity)
    db.add(vuln)
    db.commit()
    db.refresh(vuln)
    return {"id": vuln.id, "asset_id": vuln.asset_id, "severity": vuln.severity}


@router.get("/{asset_id}/vulnerabilities", summary="List vulnerabilities for asset")
def list_vulnerabilities(asset_id: int, db: Session = Depends(get_db)):
    vulns = db.query(Vulnerability).filter(Vulnerability.asset_id == asset_id).all()
    return [
        {"id": v.id, "description": v.description, "severity": v.severity}
        for v in vulns
    ]


@router.post("/sync", summary="Sync assets from external sources")
def sync_assets(source: str = "all", db: Session = Depends(get_db)):
    if source not in {"all", "sophos", "tenable"}:
        raise HTTPException(status_code=400, detail="Invalid source")

    assets: list[dict] = []
    if source in {"all", "sophos"}:
        assets.extend(sophos_sync.fetch_assets())
    if source in {"all", "tenable"}:
        assets.extend(tenable_sync.fetch_assets())

    new_assets = 0
    for data in assets:
        if not db.query(Asset).filter(Asset.hostname == data["hostname"]).first():
            asset = Asset(
                hostname=data["hostname"], status=data.get("status", "unknown")
            )
            db.add(asset)
            db.commit()
            new_assets += 1

    return {"status": "synced", "source": source, "new_assets": new_assets}
