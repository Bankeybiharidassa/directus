from fastapi import APIRouter
from pydantic import BaseModel

from ..services import acme

router = APIRouter(prefix="/certificates", tags=["certificates"])


class CertRequest(BaseModel):
    hostnames: list[str]
    email: str
    staging: bool = False


@router.post("/request", summary="Request Let's Encrypt certificate")
def request_cert(req: CertRequest):
    return acme.request_certificate(req.hostnames, req.email, req.staging)
