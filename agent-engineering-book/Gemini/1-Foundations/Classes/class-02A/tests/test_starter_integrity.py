"""Tests that prove the supplied starter itself is healthy.

These should pass before the student edits SKILL.md.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "renewal_desk_agent" / "skills" / "renewal-advisor"


def test_required_l3_resources_exist() -> None:
    expected = [
        SKILL_DIR / "references" / "discount-policy.md",
        SKILL_DIR / "references" / "renewal-process.md",
        SKILL_DIR / "references" / "risk-escalation.md",
        SKILL_DIR / "assets" / "renewal-brief-template.md",
        SKILL_DIR / "scripts" / "calculate_quote.py",
    ]
    assert all(path.is_file() for path in expected)


def test_calculator_is_deterministic() -> None:
    script = SKILL_DIR / "scripts" / "calculate_quote.py"
    spec = importlib.util.spec_from_file_location("calculate_quote", script)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    result = module.calculate_quote(92000, 12)
    assert result["discount_amount"] == 11040.00
    assert result["net_arr"] == 80960.00


def test_env_example_has_one_clear_model_setting_and_both_auth_paths() -> None:
    text = (ROOT / "renewal_desk_agent" / ".env.example").read_text(encoding="utf-8")
    assert "GEMINI_MODEL=gemini-3.7-flash" in text
    assert "GEMINI_API_KEY=" in text
    assert "GOOGLE_CLOUD_PROJECT=" in text
    assert "GOOGLE_CLOUD_LOCATION=" in text
    assert "GOOGLE_GENAI_USE_VERTEXAI" in text


def test_agent_reads_model_from_environment() -> None:
    text = (ROOT / "renewal_desk_agent" / "agent.py").read_text(encoding="utf-8")
    assert 'os.getenv("GEMINI_MODEL"' in text
    assert "gemini-3.7-flash" in text


def test_readme_has_correct_adk_web_launch_directory() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "adk web ." in text
    assert "Do **not** `cd renewal_desk_agent`" in text
