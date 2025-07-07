#!/usr/bin/env python3
"""Run basic system and API checks."""
import json
import os
import sys
import psutil
from fastapi.testclient import TestClient

# Use SQLite file for checks to avoid external DB dependencies
os.environ.setdefault("DATABASE_URL", "sqlite:///./check.db")

# Ensure repository root is in PYTHONPATH
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from backend.main import app
from backend.database import Base, engine
import backend.models

# Create tables for in-memory database
Base.metadata.create_all(bind=engine)

def check_disk():
    usage = psutil.disk_usage('/')
    return {'total': usage.total, 'used': usage.used, 'free': usage.free}

def check_cpu():
    return {'cpu_percent': psutil.cpu_percent(interval=1)}

def check_memory():
    mem = psutil.virtual_memory()
    return {'total': mem.total, 'available': mem.available}

def check_api():
    client = TestClient(app)
    resp = client.get('/customers/')
    status = resp.status_code
    return {'/customers/': status}

def main():
    report = {
        'disk': check_disk(),
        'cpu': check_cpu(),
        'memory': check_memory(),
        'api': check_api(),
    }
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
