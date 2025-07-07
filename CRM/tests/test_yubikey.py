from subprocess import CompletedProcess, CalledProcessError
from scripts import yubikey


def test_is_supported(monkeypatch):
    def fake_run(cmd, check, capture_output=True, text=True):
        return CompletedProcess(cmd, 0, stdout="4.0.0", stderr="")
    monkeypatch.setattr(yubikey.subprocess, "run", fake_run)
    assert yubikey.is_supported()


def test_is_supported_false(monkeypatch):
    def fake_run(cmd, check, capture_output=True, text=True):
        raise FileNotFoundError()

    monkeypatch.setattr(yubikey.subprocess, "run", fake_run)
    assert not yubikey.is_supported()


def test_is_connected(monkeypatch):
    def fake_run(cmd, check, capture_output=True, text=True):
        return CompletedProcess(cmd, 0, stdout="YubiKey 5", stderr="")
    monkeypatch.setattr(yubikey.subprocess, "run", fake_run)
    assert yubikey.is_connected()


def test_is_connected_false(monkeypatch):
    def fake_run(cmd, check, capture_output=True, text=True):
        raise CalledProcessError(1, cmd)

    monkeypatch.setattr(yubikey.subprocess, "run", fake_run)
    assert not yubikey.is_connected()


def test_generate_pgp_master_key(monkeypatch):
    calls = []

    def fake_run(cmd, check, capture_output=True, text=True):
        calls.append(cmd)
        return CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(yubikey.subprocess, "run", fake_run)
    yubikey.generate_pgp_master_key("Tester", "tester@example.com")
    assert any(c[0] == "gpg" for c in calls)


def test_store_private_key(monkeypatch):
    called = {}

    def fake_run(cmd, check, capture_output=True, text=True):
        called["cmd"] = cmd
        return CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(yubikey.subprocess, "run", fake_run)
    assert yubikey.store_private_key_to_yubikey("/tmp/key.asc")
    assert called["cmd"][0] == "ykman"


def test_store_private_key_failure(monkeypatch):
    def fake_run(cmd, check, capture_output=True, text=True):
        raise CalledProcessError(1, cmd)

    monkeypatch.setattr(yubikey.subprocess, "run", fake_run)
    assert not yubikey.store_private_key_to_yubikey("/tmp/key.asc")
