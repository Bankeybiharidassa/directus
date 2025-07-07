import logging
import os

import requests

logger = logging.getLogger(__name__)

_TOKEN_CACHE: dict[tuple[str, str], str] = {}


class PartnerAPI:  # pylint: disable=too-few-public-methods
    """Simple Sophos Central Partner API client."""

    def __init__(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
        base_url: str = "https://api.sophos.com",
    ):
        self.client_id = client_id or os.getenv("SOPHOS_CLIENT_ID", "")
        self.client_secret = client_secret or os.getenv("SOPHOS_CLIENT_SECRET", "")
        self.base_url = base_url.rstrip("/")

    def _get_token(self) -> str:
        key = (self.client_id, self.client_secret)
        if key in _TOKEN_CACHE:
            return _TOKEN_CACHE[key]
        resp = requests.post(
            f"{self.base_url}/oauth2/token",
            data={"grant_type": "client_credentials"},
            auth=(self.client_id, self.client_secret),
            timeout=10,
        )
        resp.raise_for_status()
        token = resp.json().get("access_token", "")
        _TOKEN_CACHE[key] = token
        logger.info("obtained partner token")
        return token

    def list_tenants(self) -> list[dict]:
        token = self._get_token()
        resp = requests.get(
            f"{self.base_url}/partner/v1/tenants",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
        )
        resp.raise_for_status()
        items = resp.json().get("items", [])
        logger.info("fetched %d tenants", len(items))
        return items
