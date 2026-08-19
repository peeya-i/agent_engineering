"""Context builder for WidgetWare SDR analysis."""

import copy
from pathlib import Path
from typing import Any
import yaml

from widgetware_sdr.instructions import get_system_instructions


def _load_yaml_config(file_path: Path) -> dict[str, Any]:
    """Load a YAML configuration file safely, raising FileNotFoundError if missing."""
    if not file_path.is_file():
        raise FileNotFoundError(f"Required configuration file not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if data is None:
        return {}
    return data


def build_context(
    account: dict[str, Any],
    objective: str,
    evidence: list[dict[str, Any]],
    state: dict[str, Any] | None = None,
    config_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Assemble the 5-layer WidgetWare SDR context package deterministically.

    Args:
        account: Target account data (treated as untrusted task context).
        objective: SDR research / analysis goal.
        evidence: List of provenance-tracked evidence records.
        state: Workflow execution state. Defaults to empty dictionary if None.
        config_dir: Optional path to configuration directory. Defaults to 'config/' at workspace root.

    Returns:
        A dictionary containing the 5 isolated context layers:
        - system_instructions (str)
        - business_context (dict with products, icp, policies)
        - task_context (dict with account, objective)
        - retrieved_evidence (list of evidence records)
        - state (dict)
    """
    if config_dir is None:
        # Default to repo root config directory relative to this source file
        base_dir = Path(__file__).resolve().parent.parent.parent
        resolved_config_dir = base_dir / "config"
    else:
        resolved_config_dir = Path(config_dir)

    products_path = resolved_config_dir / "products.yaml"
    icp_path = resolved_config_dir / "icp.yaml"
    policies_path = resolved_config_dir / "policies.yaml"

    products_config = _load_yaml_config(products_path)
    icp_config = _load_yaml_config(icp_path)
    policies_config = _load_yaml_config(policies_path)

    # Deepcopy all untrusted/dynamic inputs to ensure no input mutation
    safe_account = copy.deepcopy(account)
    safe_objective = copy.deepcopy(objective)
    safe_evidence = copy.deepcopy(evidence)
    safe_state = copy.deepcopy(state) if state is not None else {}

    context: dict[str, Any] = {
        "system_instructions": get_system_instructions(),
        "business_context": {
            "products": products_config,
            "icp": icp_config,
            "policies": policies_config,
        },
        "task_context": {
            "account": safe_account,
            "objective": safe_objective,
        },
        "retrieved_evidence": safe_evidence,
        "state": safe_state,
    }

    return context
