#!/usr/bin/env python3
import json
from backend.services import tenable


def fetch_assets():
    """Proxy to service function for backward compatibility."""
    return tenable.fetch_assets()


if __name__ == "__main__":
    print(json.dumps(fetch_assets()))
