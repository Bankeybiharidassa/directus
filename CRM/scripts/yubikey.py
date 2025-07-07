"""YubiKey helper utilities."""
import subprocess
import tempfile
import os


def is_supported() -> bool:
    """Return True if the ykman CLI is available."""
    try:
        subprocess.run(["ykman", "--version"], check=True, capture_output=True, text=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def is_connected() -> bool:
    """Return True if a YubiKey is detected."""
    try:
        result = subprocess.run(
            ["ykman", "list"], check=True, capture_output=True, text=True
        )
        return bool(result.stdout.strip())
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def generate_pgp_master_key(name: str, email: str, passphrase: str = "") -> None:
    """Generate a PGP master key using GPG in batch mode."""
    cfg = f"""
Key-Type: RSA
Key-Length: 2048
Name-Real: {name}
Name-Email: {email}
Expire-Date: 0
%no-protection
%commit
"""
    with tempfile.NamedTemporaryFile("w", delete=False) as fh:
        fh.write(cfg)
        cfg_path = fh.name
    try:
        subprocess.run(
            [
                "gpg",
                "--batch",
                "--pinentry-mode",
                "loopback",
                "--generate-key",
                cfg_path,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    finally:
        os.remove(cfg_path)


def store_private_key_to_yubikey(key_path: str) -> bool:
    """Import a private key into the YubiKey via ykman."""
    try:
        subprocess.run(
            ["ykman", "openpgp", "keys", "import", "private", key_path],
            check=True,
            capture_output=True,
            text=True,
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False
