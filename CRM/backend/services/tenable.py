# pylint: disable=duplicate-code
"""Utility functions for Tenable integration."""

import logging
import os

import requests

logger = logging.getLogger(__name__)


def fetch_assets() -> list[dict]:
    """Fetch assets from Tenable API or return sample data."""
    url = os.getenv("TENABLE_URL", "")
    token = os.getenv("TENABLE_TOKEN", "")
    if url and token:
        resp = requests.get(
            url, headers={"Authorization": f"Bearer {token}"}, timeout=10
        )
        resp.raise_for_status()
        assets = resp.json()
    else:
        assets = [
            {"hostname": "tenable1", "status": "scanned"},
            {"hostname": "tenable2", "status": "scanned"},
        ]
    logger.info("fetched %d Tenable assets", len(assets))
    return assets
