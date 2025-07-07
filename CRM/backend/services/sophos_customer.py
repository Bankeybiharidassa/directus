import logging

import requests

logger = logging.getLogger(__name__)

_TOKEN_CACHE: dict[str, str] = {}


class CustomerAPI:
    """Sophos Central Customer/Tenant API client."""

    def __init__(self, base_url: str = "https://api.sophos.com"):
        self.base_url = base_url.rstrip("/")

    def get_tenant_token(self, tenant_id: str, refresh_token: str) -> str:
        if tenant_id in _TOKEN_CACHE:
            return _TOKEN_CACHE[tenant_id]
        resp = requests.post(
            f"{self.base_url}/oauth2/token",
            data={"grant_type": "refresh_token", "refresh_token": refresh_token},
            timeout=10,
        )
        resp.raise_for_status()
        token = resp.json().get("access_token", "")
        _TOKEN_CACHE[tenant_id] = token
        logger.info("obtained tenant token for %s", tenant_id)
        return token

    def fetch_alerts(self, tenant_id: str, access_token: str) -> list[dict]:
        resp = requests.get(
            f"{self.base_url}/siem/v1/alerts",
            headers={
                "Authorization": f"Bearer {access_token}",
                "X-Tenant-ID": tenant_id,
            },
            timeout=10,
        )
        resp.raise_for_status()
        items = resp.json().get("items", [])
        logger.info("tenant %s: fetched %d alerts", tenant_id, len(items))
        return items
