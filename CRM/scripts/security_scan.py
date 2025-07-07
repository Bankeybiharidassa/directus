#!/usr/bin/env python3
"""Comprehensive security scan utilities.

This module provides package and binary version checks, CVE lookups,
whitebox static analysis and a simple blackbox port scan. Caching is
used so both Codex and live operators can run scans without repeated
network calls.
"""
import json
import os
import socket
import subprocess
from typing import Dict, Any, List

import requests
from cryptography.fernet import Fernet

CACHE_FILE = os.path.join(os.path.dirname(__file__), '..', 'security_cache.enc')
KEY_ENV = 'SEC_SCAN_KEY'
BINARIES = [
    '/bin/bash',
    '/usr/bin/ssh',
    '/usr/bin/python3',
    '/usr/bin/node',
]

PORTS = [22, 80, 443]


def _load_key() -> bytes:
    key = os.environ.get(KEY_ENV)
    if key:
        return key.encode()
    key = Fernet.generate_key()
    os.environ[KEY_ENV] = key.decode()
    return key


def list_packages() -> Dict[str, str]:
    """Return installed dpkg package versions."""
    result = subprocess.run(
        ['dpkg-query', '-W', '-f=${binary:Package} ${Version}\n'],
        capture_output=True, text=True, check=False
    )
    packages = {}
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            packages[parts[0]] = parts[1]
    return packages


def fetch_ubuntu_vulns(package: str) -> Any:
    """Fetch vulnerability info from Ubuntu notices."""
    try:
        url = f'https://ubuntu.com/security/notices.json?package={package}'
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get('results', [])
    except Exception:
        pass
    return []


def fetch_cve(name: str) -> List[str]:
    """Fetch CVE list from the public CVE API."""
    try:
        url = f'https://cve.circl.lu/api/search/{name}'
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return [e.get('id') for e in data.get('data', [])]
    except Exception:
        pass
    return []


def save_cache(data: Dict[str, Any], key: bytes) -> None:
    f = Fernet(key)
    enc = f.encrypt(json.dumps(data).encode())
    with open(CACHE_FILE, 'wb') as fh:
        fh.write(enc)


def load_cache(key: bytes) -> Dict[str, Any]:
    if not os.path.exists(CACHE_FILE):
        return {}
    f = Fernet(key)
    with open(CACHE_FILE, 'rb') as fh:
        enc = fh.read()
    try:
        return json.loads(f.decrypt(enc).decode())
    except Exception:
        return {}


def check_packages(cache: Dict[str, Any]) -> Dict[str, Any]:
    """Check installed packages and collect vulnerabilities."""
    pkgs = list_packages()
    report = {}
    for pkg, ver in pkgs.items():
        vulns = cache.get(pkg)
        if vulns is None:
            vulns = fetch_ubuntu_vulns(pkg)
            if not vulns:
                vulns = fetch_cve(pkg)
            cache[pkg] = vulns
        report[pkg] = {"version": ver, "vulns": vulns}
    return report


def check_binaries() -> Dict[str, Any]:
    """Verify critical binaries and collect CVEs."""
    report = {}
    for path in BINARIES:
        if not os.path.exists(path):
            report[path] = {"present": False}
            continue
        try:
            res = subprocess.run([path, '--version'], capture_output=True, text=True)
            line = res.stdout.splitlines()[0] if res.stdout else ''
        except Exception:
            line = ''
        report[path] = {
            "present": True,
            "version": line,
            "cves": fetch_cve(os.path.basename(path)),
        }
    return report


def whitebox_scan() -> Dict[str, Any]:
    """Run bandit static analysis if available."""
    try:
        res = subprocess.run(['bandit', '-r', '.', '-f', 'json'], capture_output=True, text=True)
        if res.returncode == 0:
            data = json.loads(res.stdout or '{}')
            issues = [i for i in data.get('results', []) if i.get('issue_severity') in {'MEDIUM', 'HIGH'}]
            return {"issues": len(issues)}
    except FileNotFoundError:
        return {"error": "bandit not installed"}
    except Exception:
        pass
    return {"issues": 0}


def blackbox_scan(host: str = 'localhost', ports: List[int] = PORTS) -> Dict[str, Any]:
    """Simple TCP port scan for common ports."""
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((host, port)) == 0:
                open_ports.append(port)
    return {"host": host, "open_ports": open_ports}


def scan_system() -> Dict[str, Any]:
    """Run full security scan and return report."""
    key = _load_key()
    cache = load_cache(key)
    result = {
        "packages": check_packages(cache),
        "binaries": check_binaries(),
        "whitebox": whitebox_scan(),
        "blackbox": blackbox_scan(),
    }
    save_cache(cache, key)
    return result


def main() -> None:
    report = scan_system()
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
