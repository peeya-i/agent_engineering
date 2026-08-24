"""Assemble the WidgetWare context package.

Book 1 §3.2 separates context into five layers: system instructions,
business context, task context, retrieved evidence, and state. This
module builds that package deterministically, ensuring clear separation
and protection against input mutation and side effects.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import yaml

from widgetware_sdr.instructions import get_system_instructions

CONFIG_DIR = Path(__file__).resolve().parent.parent.parent / "config"


def load_config(name: str) -> dict[str, Any]:
    """Load one of the stable YAML business-configuration files.

    Raises FileNotFoundError if the file does not exist.
    """
    path = CONFIG_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Required configuration file '{name}' is missing at {path}")
    with path.open("r", encoding="utf-8") as f:
        content = yaml.safe_load(f)
        if content is None:
            return {}
        return content


def build_context(
    account: dict[str, Any],
    objective: str,
    evidence: list[dict[str, Any]],
    state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a full Context Package for one account.

    Guarantees:
    - Loads products.yaml, icp.yaml, and policies.yaml.
    - Raises FileNotFoundError if any of the configurations are missing.
    - Separates system instructions, business context, task context, evidence, and state.
    - Prevents mutation of input objects.
    - Preserves evidence provenance and supplied state.
    - Uses an empty state object when state is omitted.
    """
    # 1. Load stable configurations, raising clear errors if missing
    products = load_config("products.yaml")
    icp = load_config("icp.yaml")
    policies = load_config("policies.yaml")

    # 2. Avoid modifying input objects (create deep copies)
    account_copy = copy.deepcopy(account)
    evidence_copy = copy.deepcopy(evidence)
    state_copy = copy.deepcopy(state) if state is not None else {}

    # 3. Assemble the layers
    return {
        "system_instructions": get_system_instructions(),
        "business_context": {
            "products": products,
            "icp": icp,
            "policies": policies,
        },
        "task_context": {
            "account": account_copy,
            "objective": objective,
        },
        "retrieved_evidence": evidence_copy,
        "state": state_copy,
    }
