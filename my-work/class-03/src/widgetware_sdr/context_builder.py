"""Deterministic Context Builder for the WidgetWare SDR Context Package."""

import copy
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import yaml

from widgetware_sdr.instructions import get_system_instructions


def load_yaml_config(file_path: Path) -> Dict[str, Any]:
    """Load a YAML configuration file from disk.

    Raises FileNotFoundError if the file is missing, or ValueError if invalid.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Required configuration file missing: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if data is None:
                return {}
            if not isinstance(data, dict):
                raise ValueError(f"Configuration file {file_path} must contain a top-level mapping/dictionary.")
            return data
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file {file_path}: {e}") from e


def resolve_config_dir(config_dir: Optional[Union[str, Path]] = None) -> Path:
    """Resolve the directory containing configuration YAML files."""
    if config_dir is not None:
        p = Path(config_dir)
        if not p.exists():
            raise FileNotFoundError(f"Specified config directory does not exist: {p}")
        return p

    # Check current working directory config/
    cwd_config = Path.cwd() / "config"
    if (cwd_config / "products.yaml").exists():
        return cwd_config

    # Check relative to module package root
    file_dir = Path(__file__).resolve()
    package_root_config = file_dir.parents[2] / "config"
    if (package_root_config / "products.yaml").exists():
        return package_root_config

    return cwd_config


def build_context(
    account: Dict[str, Any],
    objective: str,
    evidence: List[Dict[str, Any]],
    state: Optional[Dict[str, Any]] = None,
    config_dir: Optional[Union[str, Path]] = None,
) -> Dict[str, Any]:
    """Assemble the 5-layer WidgetWare SDR context package.

    Args:
        account: Target account information (untrusted task data).
        objective: Research objective string.
        evidence: List of evidence records with provenance.
        state: Optional current workflow state dictionary. Defaults to {}.
        config_dir: Optional path to config folder containing YAML files.

    Returns:
        Dict with 5 top-level keys: system_instructions, business_context,
        task_context, retrieved_evidence, state.

    Raises:
        FileNotFoundError: If any required YAML config file is missing.
        ValueError: If configuration or input formats are invalid.
    """
    target_config_dir = resolve_config_dir(config_dir)

    # 1. Load Business Configurations (Products, ICP, Policies)
    products_path = target_config_dir / "products.yaml"
    icp_path = target_config_dir / "icp.yaml"
    policies_path = target_config_dir / "policies.yaml"

    products_data = load_yaml_config(products_path)
    icp_data = load_yaml_config(icp_path)
    policies_data = load_yaml_config(policies_path)

    # Validate essential YAML fields
    if "company" not in products_data or "offerings" not in products_data:
        raise ValueError("products.yaml missing required 'company' or 'offerings' sections.")
    if "evidence_classifications" not in policies_data:
        raise ValueError("policies.yaml missing required 'evidence_classifications' section.")

    # 2. Layer 1: System Instructions
    system_instructions = get_system_instructions()

    # 3. Layer 2: Business Context
    business_context = {
        "products": copy.deepcopy(products_data),
        "icp": copy.deepcopy(icp_data),
        "policies": copy.deepcopy(policies_data),
    }

    # 4. Layer 3: Task Context (Unmutated inputs)
    task_context = {
        "account": copy.deepcopy(account if account is not None else {}),
        "objective": str(objective if objective is not None else ""),
    }

    # 5. Layer 4: Retrieved Evidence (Preserving provenance)
    retrieved_evidence = copy.deepcopy(evidence if evidence is not None else [])

    # 6. Layer 5: Workflow State (Default to empty dict if omitted)
    workflow_state = copy.deepcopy(state) if state is not None else {}

    # Assemble complete 5-layer package
    context_package = {
        "system_instructions": system_instructions,
        "business_context": business_context,
        "task_context": task_context,
        "retrieved_evidence": retrieved_evidence,
        "state": workflow_state,
    }

    return context_package
