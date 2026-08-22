from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).parents[1]
SKILL_DIR = ROOT / "renewal_desk_agent" / "skills" / "renewal-advisor"
SKILL_MD = SKILL_DIR / "SKILL.md"


def skill_text() -> str:
    return SKILL_MD.read_text(encoding="utf-8")


def frontmatter_value(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, flags=re.MULTILINE)
    assert match, f"Missing frontmatter key: {key}"
    return match.group(1).strip()


def test_skill_directory_matches_frontmatter_name():
    assert frontmatter_value(skill_text(), "name") == SKILL_DIR.name


def test_l1_description_is_finished_and_compact():
    description = frontmatter_value(skill_text(), "description")
    assert "TODO" not in description
    assert 40 <= len(description) <= 500
    assert any(word in description.lower() for word in ["renewal", "discount"])


def test_no_todos_remain_in_skill():
    assert "TODO" not in skill_text()


def test_l2_names_every_l3_path_exactly():
    text = skill_text()
    required_paths = [
        "references/discount-policy.md",
        "references/renewal-process.md",
        "references/risk-escalation.md",
        "assets/renewal-brief-template.md",
        "scripts/calculate_quote.py",
    ]
    for path in required_paths:
        assert path in text, f"L2 must name the exact L3 path: {path}"


def test_l2_contains_quality_and_safety_contracts():
    lower = skill_text().lower()
    for concept in ["when not to use", "minimum", "cite", "unsupported", "ambiguous"]:
        assert concept in lower, f"SKILL.md must address: {concept}"


def test_expected_l3_files_exist():
    paths = [
        SKILL_DIR / "references" / "discount-policy.md",
        SKILL_DIR / "references" / "renewal-process.md",
        SKILL_DIR / "references" / "risk-escalation.md",
        SKILL_DIR / "assets" / "renewal-brief-template.md",
        SKILL_DIR / "scripts" / "calculate_quote.py",
    ]
    for path in paths:
        assert path.is_file(), f"Missing resource: {path.relative_to(SKILL_DIR)}"


def test_quote_calculator_is_deterministic():
    script = SKILL_DIR / "scripts" / "calculate_quote.py"
    completed = subprocess.run(
        [
            sys.executable,
            str(script),
            "--arr",
            "92000",
            "--discount-percent",
            "12",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert '"discount_amount": "11040.00"' in completed.stdout
    assert '"net_arr": "80960.00"' in completed.stdout
