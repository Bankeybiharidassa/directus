from scripts import security_scan
from cryptography.fernet import Fernet


def test_cache_roundtrip(tmp_path, monkeypatch):
    key = Fernet.generate_key()
    cache_file = tmp_path / "cache.enc"
    monkeypatch.setattr(security_scan, "CACHE_FILE", str(cache_file))
    data = {"pkg": ["vuln1"]}
    security_scan.save_cache(data, key)
    loaded = security_scan.load_cache(key)
    assert loaded == data


def test_check_binaries(monkeypatch):
    monkeypatch.setattr(security_scan, "BINARIES", ["/bin/echo"])
    monkeypatch.setattr(security_scan, "fetch_cve", lambda name: ["CVE-123"])
    report = security_scan.check_binaries()
    assert "/bin/echo" in report
    assert report["/bin/echo"]["present"] is True

def test_scan_system(monkeypatch):
    monkeypatch.setattr(security_scan, "list_packages", lambda: {"a": "1"})
    monkeypatch.setattr(security_scan, "fetch_ubuntu_vulns", lambda pkg: [])
    monkeypatch.setattr(security_scan, "fetch_cve", lambda pkg: [])
    monkeypatch.setattr(security_scan, "check_binaries", lambda: {"/bin/bash": {"present": True}})
    monkeypatch.setattr(security_scan, "whitebox_scan", lambda: {"issues": 0})
    monkeypatch.setattr(security_scan, "blackbox_scan", lambda host='localhost', ports=(): {"open_ports": []})
    monkeypatch.setattr(security_scan, "CACHE_FILE", "/tmp/cache")
    key = Fernet.generate_key()
    monkeypatch.setenv(security_scan.KEY_ENV, key.decode())
    report = security_scan.scan_system()
    assert report["packages"]["a"]["version"] == "1"
    assert "/bin/bash" in report["binaries"]
