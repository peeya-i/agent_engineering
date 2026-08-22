#!/usr/bin/env python3
"""Class 02A preflight checks.

Offline mode validates local configuration and structure.
--online makes one tiny model request to expose auth/model/quota problems early.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT_DIR = ROOT / "renewal_desk_agent"
ENV_FILE = AGENT_DIR / ".env"


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def fail(message: str) -> None:
    print(f"[FAIL] {message}")
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"[ OK ] {message}")


def check_structure() -> None:
    required = [
        AGENT_DIR / "agent.py",
        AGENT_DIR / ".env.example",
        AGENT_DIR / "skills" / "renewal-advisor" / "SKILL.md",
        AGENT_DIR / "skills" / "renewal-advisor" / "references" / "discount-policy.md",
        AGENT_DIR / "skills" / "renewal-advisor" / "references" / "renewal-process.md",
        AGENT_DIR / "skills" / "renewal-advisor" / "references" / "risk-escalation.md",
        AGENT_DIR / "skills" / "renewal-advisor" / "assets" / "renewal-brief-template.md",
        AGENT_DIR / "skills" / "renewal-advisor" / "scripts" / "calculate_quote.py",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    if missing:
        fail("Missing required starter files: " + ", ".join(missing))
    ok("Starter file structure is complete")


def check_python() -> None:
    if sys.version_info < (3, 11):
        fail(f"Python 3.11+ required; found {sys.version.split()[0]}")
    ok(f"Python {sys.version.split()[0]}")


def check_adk_import() -> None:
    try:
        import google.adk  # noqa: F401
    except Exception as exc:
        fail(f"google-adk is not importable: {exc}. Install requirements.txt first.")
    ok("google-adk import works")


def check_env() -> tuple[str, str]:
    if not ENV_FILE.exists():
        fail(
            "renewal_desk_agent/.env is missing. "
            "Copy renewal_desk_agent/.env.example to renewal_desk_agent/.env."
        )

    load_env_file(ENV_FILE)
    model = os.getenv("GEMINI_MODEL", "").strip()
    if not model:
        fail("GEMINI_MODEL is empty")
    ok(f"Model configured: {model}")

    use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "FALSE").strip().upper() == "TRUE"

    if use_vertex:
        project = os.getenv("GOOGLE_CLOUD_PROJECT", "").strip()
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "").strip()
        if not project or not location:
            fail(
                "Vertex mode requires GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION"
            )
        ok(f"Auth mode: Vertex AI ({project}, {location})")
        return "vertex", model

    key = os.getenv("GEMINI_API_KEY", "").strip() or os.getenv("GOOGLE_API_KEY", "").strip()
    if not key:
        fail("Gemini API-key mode requires GEMINI_API_KEY (or GOOGLE_API_KEY)")
    if key == "PASTE_YOUR_KEY_HERE":
        fail("Replace PASTE_YOUR_KEY_HERE with a real key")
    ok("Auth mode: Gemini API key")
    return "api_key", model


def online_check(mode: str, model: str) -> None:
    try:
        from google import genai

        if mode == "vertex":
            client = genai.Client(
                vertexai=True,
                project=os.environ["GOOGLE_CLOUD_PROJECT"],
                location=os.environ["GOOGLE_CLOUD_LOCATION"],
            )
        else:
            key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
            client = genai.Client(api_key=key)

        response = client.models.generate_content(
            model=model,
            contents="Reply with exactly: OK",
        )
        text = (getattr(response, "text", "") or "").strip()
        if not text:
            fail("Model call returned no text")
        ok(f"Live model request succeeded: {text[:40]}")
    except SystemExit:
        raise
    except Exception as exc:
        fail(
            "Live model request failed. This is usually auth/model/quota/billing/network, "
            f"not SKILL.md. Error: {type(exc).__name__}: {exc}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--online",
        action="store_true",
        help="Make one tiny live model request after local checks.",
    )
    args = parser.parse_args()

    print("Class 02A preflight")
    print(f"Root: {ROOT}")
    check_python()
    check_structure()
    check_adk_import()
    mode, model = check_env()

    if args.online:
        online_check(mode, model)
    else:
        print("[INFO] Offline checks complete. Use --online to test credentials/model access.")

    print("[PASS] Preflight complete")


if __name__ == "__main__":
    main()
