from fastapi import APIRouter

from ..services.sophos_partner import PartnerAPI

router = APIRouter(prefix="/sophos", tags=["sophos"])


@router.get("/tenants", summary="List Sophos tenants")
def list_tenants():
    api = PartnerAPI()
    return api.list_tenants()
