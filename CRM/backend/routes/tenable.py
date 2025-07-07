from fastapi import APIRouter

from ..services import tenable

router = APIRouter(prefix="/tenable", tags=["tenable"])


@router.get("/assets", summary="List Tenable assets")
def list_assets():
    return tenable.fetch_assets()
