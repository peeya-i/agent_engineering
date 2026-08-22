#!/usr/bin/env python3
"""Deterministic Class 02A local grader."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SKILL = ROOT / "renewal_desk_agent" / "skills" / "renewal-advisor" / "SKILL.md"
SUBMISSION = ROOT / "submission.md"

checks: list[tuple[str, bool, int]] = []


def add(name: str, passed: bool, points: int) -> None:
    checks.append((name, passed, points))


skill = SKILL.read_text(encoding="utf-8")
submission = SUBMISSION.read_text(encoding="utf-8")

add("No TODOs remain in SKILL.md", "TODO" not in skill, 10)

for path in (
    "references/discount-policy.md",
    "references/renewal-process.md",
    "references/risk-escalation.md",
    "assets/renewal-brief-template.md",
    "scripts/calculate_quote.py",
):
    add(f"L2 routes exact path {path}", path in skill, 6)

lower = skill.lower()
add("L2 requires minimum-resource loading", "minimum" in lower and "resource" in lower, 8)
add("L2 handles missing inputs", "missing" in lower and "input" in lower, 8)
add("L2 requires citations", "cite" in lower, 8)
add("L2 handles unsupported questions", "unsupported" in lower, 8)
add(
    "L2 preserves requested/routed/approved states",
    all(word in lower for word in ("requested", "routed", "approved")),
    8,
)
add("submission.md completed", "TODO" not in submission and len(submission) >= 1800, 10)

pytest_run = subprocess.run(
    [sys.executable, "-m", "pytest", "-q"],
    cwd=ROOT,
    text=True,
    capture_output=True,
)
add("Full pytest suite passes", pytest_run.returncode == 0, 8)

earned = sum(points for _, passed, points in checks if passed)
possible = sum(points for _, _, points in checks)

print("Class 02A Local Grader")
print("=" * 72)
for name, passed, points in checks:
    print(f"{'PASS' if passed else 'FAIL':4}  {points:>2}  {name}")
print("=" * 72)
print(f"Score: {earned}/{possible}")

if pytest_run.returncode != 0:
    print("\npytest output:")
    print(pytest_run.stdout[-3000:])

raise SystemExit(0 if earned == possible else 1)
