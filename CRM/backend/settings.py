"""Utility functions for configuration management."""

import os
from functools import lru_cache

import yaml

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "settings.yaml")


@lru_cache(maxsize=1)
def load_settings():
    """Load settings from YAML configuration file."""
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def apply_env():
    """Populate environment variables from settings when not already defined."""
    cfg = load_settings()

    def _clean(val: str | None) -> str:
        if isinstance(val, str) and val.startswith("${") and val.endswith("}"):
            return ""
        return val or ""

    db = cfg.get("database", {})
    if "DATABASE_URL" not in os.environ:
        engine = db.get("engine", "sqlite")
        host = _clean(db.get("host"))
        user = _clean(db.get("user"))
        password = _clean(db.get("password"))
        port = db.get("port", 3306)
        name = db.get("name", "test.db")

        if engine == "sqlite" or not host:
            url = f"sqlite:///./{name}"
        else:
            url = f"{engine}://{user}:{password}@{host}:{port}/{name}"
        os.environ["DATABASE_URL"] = url

    imap = cfg.get("imap", {})
    os.environ.setdefault("IMAP_HOST", imap.get("host", ""))
    os.environ.setdefault("IMAP_USER", imap.get("user", ""))
    os.environ.setdefault("IMAP_PASSWORD", imap.get("password", ""))

    sophos = cfg.get("sophos", {})

    os.environ.setdefault("SOPHOS_URL", _clean(sophos.get("url")))
    os.environ.setdefault("SOPHOS_TOKEN", _clean(sophos.get("token")))

    tenable = cfg.get("tenable", {})
    os.environ.setdefault("TENABLE_URL", _clean(tenable.get("url")))
    os.environ.setdefault("TENABLE_TOKEN", _clean(tenable.get("token")))
