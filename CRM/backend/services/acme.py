import logging
import subprocess

logger = logging.getLogger(__name__)


def request_certificate(
    hostnames: list[str], email: str, staging: bool = False
) -> dict:
    """Request/renew certificates for hostnames using certbot."""
    if not hostnames:
        raise ValueError("hostnames required")
    cmd = [
        "certbot",
        "certonly",
        "--non-interactive",
        "--agree-tos",
        "--email",
        email,
        "--reuse-key",
        "--cert-name",
        "nucleus",
        "--standalone",
    ]
    for h in hostnames:
        cmd += ["-d", h]
    if staging:
        cmd.append("--test-cert")

    logger.info("Executing: %s", " ".join(cmd))
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    logger.info(result.stdout)
    if result.returncode != 0:
        logger.error(result.stderr)
        raise RuntimeError("certbot failed")
    return {"status": "ok"}
