"""Runtime configuration loaded from environment variables."""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    log_level: str = "INFO"


def load_settings() -> Settings:
    return Settings(log_level=os.getenv("LOG_LEVEL", "INFO").upper())


def configure_logging() -> Settings:
    """Load settings and apply them to the root logger. Call once at
    process startup (server entrypoint, CLI scripts)."""
    settings = load_settings()
    logging.basicConfig(
        level=getattr(logging, settings.log_level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    return settings
