from fastapi import APIRouter, Depends, Header, HTTPException, status as http_status
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db
from ..services import dmarc

router = APIRouter(prefix="/api/crm/dmarc", tags=["crm-dmarc"])


@router.get("/{tenant_id}/{domain}", summary="Get DMARC stats for tenant domain")
def get_crm_report(
    tenant_id: int,
    domain: str,
    fmt: str = "json",
    x_crm_tenant: int | None = Header(default=None),
    db: Session = Depends(get_db),
):
    if x_crm_tenant is not None and x_crm_tenant != tenant_id:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN, detail="Forbidden"
        )
    data = dmarc.get_crm_report(tenant_id, domain, db)
    if fmt == "csv":
        csv_header = "domain,pass,fail,volume,abuse_contacts,complaint_rate\n"
        csv_row = (
            f"{data['domain']},{data['pass']},{data['fail']}"
            f",{data['volume']},{data['abuse_contacts']}"
            f",{data['complaint_rate']}\n"
        )
        csv = csv_header + csv_row
        return PlainTextResponse(csv, media_type="text/csv")
    return data


class AbusePayload(BaseModel):
    """Payload for reporting abuse."""  # pylint: disable=too-few-public-methods

    ip: str
    contact: str


@router.post("/abuse", summary="Report abuse for tenant domain")
def report_abuse(
    tenant_id: int,
    domain: str,
    payload: AbusePayload,
    x_crm_tenant: int | None = Header(default=None),
    db: Session = Depends(get_db),
):
    if x_crm_tenant is not None and x_crm_tenant != tenant_id:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN, detail="Forbidden"
        )
    dmarc.send_abuse(tenant_id, domain, payload.ip, payload.contact, db)
    return {"status": "sent"}


@router.put("/abuse/{report_id}", summary="Update abuse report status")
def update_abuse(
    report_id: int,
    status: str,
    db: Session = Depends(get_db),
):
    if status not in {"sent", "responded", "actioned"}:
        raise HTTPException(status_code=400, detail="Invalid status")
    dmarc.update_abuse_status(report_id, status, db)
    return {"id": report_id, "status": status}
