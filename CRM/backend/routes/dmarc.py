from fastapi import APIRouter

from ..services import dmarc

router = APIRouter(prefix="/dmarc", tags=["dmarc"])


@router.get("/{domain}", summary="Get DMARC report for domain")
def get_report(domain: str):
    return dmarc.fetch_report(domain)
