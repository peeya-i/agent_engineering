"""Assignment contract tests.

These intentionally fail on the starter and pass after L1/L2 are engineered.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = (
    ROOT
    / "renewal_desk_agent"
    / "skills"
    / "renewal-advisor"
    / "SKILL.md"
)
SUBMISSION = ROOT / "submission.md"


def skill_text() -> str:
    return SKILL.read_text(encoding="utf-8")


def test_l1_metadata_is_specific_and_complete() -> None:
    text = skill_text()
    assert "TODO" not in text, "Remove TODOs from the completed SKILL.md"

    frontmatter = text.split("---", 2)[1]
    match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
    assert match, "SKILL.md frontmatter must contain description"

    description = match.group(1).lower()
    assert len(description) >= 110, "L1 description is still too vague"
    for term in ("discount", "timing", "risk", "quote", "brief"):
        assert term in description, f"L1 description should mention {term}"
    assert "troubleshoot" in description or "troubleshooting" in description, (
        "L1 should include an exclusion for product troubleshooting"
    )


def test_l2_names_every_exact_resource_path() -> None:
    text = skill_text()
    for path in (
        "references/discount-policy.md",
        "references/renewal-process.md",
        "references/risk-escalation.md",
        "assets/renewal-brief-template.md",
        "scripts/calculate_quote.py",
    ):
        assert path in text, f"L2 must name exact path: {path}"


def test_l2_contains_operating_and_safety_contracts() -> None:
    text = skill_text().lower()
    required_concepts = {
        "minimum resource": ("minimum", "resource"),
        "missing input": ("missing", "input"),
        "citation": ("cite",),
        "unsupported": ("unsupported",),
        "requested": ("requested",),
        "routed": ("routed",),
        "approved": ("approved",),
    }
    for label, terms in required_concepts.items():
        assert all(term in text for term in terms), f"L2 missing concept: {label}"


def test_submission_is_complete() -> None:
    text = SUBMISSION.read_text(encoding="utf-8")
    assert "TODO" not in text, "Complete submission.md"
    for case in "ABCDEF":
        assert f"## Case {case}" in text
        section = text.split(f"## Case {case}", 1)[1]
        if case != "F":
            section = section.split("## Case ", 1)[0]
        assert "Observed L3:" in section
    assert len(text) >= 1800, "submission.md is too incomplete"
