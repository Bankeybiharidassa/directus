import logging
import os

import requests
from sqlalchemy.orm import Session

from ..models import DmarcAbuse, DmarcReport

logger = logging.getLogger(__name__)


def fetch_report(domain: str) -> dict:
    """Fetch DMARC report for a domain or return sample data."""
    url = os.getenv("DMARC_API_URL", "")
    token = os.getenv("DMARC_API_TOKEN", "")
    if url and token:
        resp = requests.get(
            f"{url}/{domain}", headers={"Authorization": f"Bearer {token}"}, timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
    else:
        data = {"domain": domain, "pass": 10, "fail": 1}
    logger.info("fetched DMARC report for %s", domain)
    return data


def get_crm_report(tenant_id: int, domain: str, db: Session) -> dict:
    """Return DMARC stats for a tenant/domain from the database."""
    report = (
        db.query(DmarcReport)
        .filter(DmarcReport.tenant_id == tenant_id, DmarcReport.domain == domain)
        .first()
    )
    if not report:
        # placeholder data
        report = DmarcReport(
            tenant_id=tenant_id,
            domain=domain,
            pass_count=10,
            fail_count=1,
            volume=11,
            abuse_contacts=0,
            complaint_rate=0.0,
        )
        db.add(report)
        db.commit()
        db.refresh(report)
    logger.info("retrieved CRM DMARC report for %s tenant %d", domain, tenant_id)
    return {
        "tenant_id": report.tenant_id,
        "domain": report.domain,
        "pass": report.pass_count,
        "fail": report.fail_count,
        "volume": report.volume,
        "abuse_contacts": report.abuse_contacts,
        "complaint_rate": report.complaint_rate,
    }


def send_abuse(tenant_id: int, domain: str, ip: str, contact: str, db: Session) -> None:
    """Store an abuse complaint and notify external analyzer if configured."""
    abuse = DmarcAbuse(
        tenant_id=tenant_id,
        domain=domain,
        ip_address=ip,
        contact=contact,
        status="sent",
    )
    db.add(abuse)
    db.commit()
    webhook = os.getenv("DMARC_ABUSE_WEBHOOK")
    if webhook:
        try:
            requests.post(
                webhook,
                json={
                    "tenant_id": tenant_id,
                    "domain": domain,
                    "ip": ip,
                    "contact": contact,
                },
                timeout=10,
            )
        except requests.RequestException as exc:  # pragma: no cover - best effort
            logger.warning("webhook notification failed: %s", exc)
    logger.info("abuse report stored for %s tenant %d", domain, tenant_id)


def update_abuse_status(report_id: int, status: str, db: Session) -> None:
    """Update stored abuse report status."""
    abuse = db.query(DmarcAbuse).filter(DmarcAbuse.id == report_id).first()
    if abuse:
        abuse.status = status
        db.commit()
        logger.info("abuse report %d updated to %s", report_id, status)
