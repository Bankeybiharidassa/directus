"""Logging configuration helpers."""

import logging
import os


def setup_logging(log_file: str = "/var/log/nucleus/backend.log", level=logging.INFO) -> None:
    """Initialise logging with syslog-style timestamps."""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        force=True,
    )
