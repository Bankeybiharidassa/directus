#!/usr/bin/env python3
import json
import os
from backend.services.sophos_partner import PartnerAPI


def fetch_assets():
    """Fetch asset information via the Sophos Partner API."""
    if os.getenv("SOPHOS_CLIENT_ID") and os.getenv("SOPHOS_CLIENT_SECRET"):
        api = PartnerAPI()
        tenants = api.list_tenants()
        # For demonstration just return tenant IDs as asset list
        return [{"tenant_id": t.get("id", "unknown")} for t in tenants]
    return [
        {"hostname": "sophos1", "status": "protected"},
        {"hostname": "sophos2", "status": "protected"},
    ]


if __name__ == "__main__":
    print(json.dumps(fetch_assets()))
