"""Load the single project-level .env and configure shared runtime settings."""

from __future__ import annotations

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from google.genai import types

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def configure_logging() -> None:
    """Use Cloud Logging on Vertex AI when available; otherwise use local logs."""
    use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "FALSE").upper() == "TRUE"
    if use_vertex:
        try:
            import google.cloud.logging

            google.cloud.logging.Client().setup_logging()
            return
        except Exception as exc:  # Cloud credentials may not be configured yet.
            logging.basicConfig(level=logging.INFO)
            logging.getLogger(__name__).warning(
                "Cloud Logging unavailable; using local logging: %s", exc
            )
            return

    logging.basicConfig(level=logging.INFO)


configure_logging()

MODEL_NAME = os.getenv("MODEL", "gemini-2.5-flash")
RETRY_OPTIONS = types.HttpRetryOptions(
    attempts=5,
    initial_delay=1,
    max_delay=8,
)

