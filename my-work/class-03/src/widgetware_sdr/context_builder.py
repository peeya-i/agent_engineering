"""Context builder for WidgetWare SDR package."""

import copy
from pathlib import Path
from typing import Any
import yaml

from widgetware_sdr.instructions import get_system_instructions


def _load_yaml_config(file_path: Path) -> dict[str, Any]:
    """Load a YAML configuration file safely.

    Raises FileNotFoundError or ValueError if missing or invalid.
    """
    if not file_path.is_file():
        raise FileNotFoundError(f"Required configuration file missing: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = yaml.safe_load(f)
            if content is None:
                return {}
            if not isinstance(content, dict):
                raise ValueError(f"Configuration file {file_path} must contain a top-level dictionary mapping.")
            return content
    except yaml.YAMLError as exc:
        raise ValueError(f"Failed to parse YAML file {file_path}: {exc}") from exc


def _get_config_dir(config_dir: str | Path | None = None) -> Path:
    """Determine the configuration directory path."""
    if config_dir is not None:
        return Path(config_dir)

    # First check relative to this package source location
    pkg_base_config = Path(__file__).resolve().parents[2] / "config"
    if pkg_base_config.is_dir():
        return pkg_base_config

    # Fallback to current working directory 'config'
    cwd_config = Path.cwd() / "config"
    if cwd_config.is_dir():
        return cwd_config

    return pkg_base_config


def build_context(
    account: dict[str, Any],
    objective: str,
    evidence: list[dict[str, Any]],
    state: dict[str, Any] | None = None,
    config_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Assemble the 5 separate context layers into a structured context package.

    Layers:
    1. system_instructions
    2. business_context (products, icp, policies)
    3. task_context (account, objective)
    4. retrieved_evidence
    5. state

    Raises FileNotFoundError or ValueError if required configuration is missing or invalid.
    Input parameters are never mutated.
    """
    # Clone inputs to guarantee immutability
    account_copy = copy.deepcopy(account)
    evidence_copy = copy.deepcopy(evidence)
    state_copy = copy.deepcopy(state) if state is not None else {}

    base_config_path = _get_config_dir(config_dir)

    products_data = _load_yaml_config(base_config_path / "products.yaml")
    icp_data = _load_yaml_config(base_config_path / "icp.yaml")
    policies_data = _load_yaml_config(base_config_path / "policies.yaml")

    return {
        "system_instructions": get_system_instructions(),
        "business_context": {
            "products": products_data,
            "icp": icp_data,
            "policies": policies_data,
        },
        "task_context": {
            "account": account_copy,
            "objective": objective,
        },
        "retrieved_evidence": evidence_copy,
        "state": state_copy,
    }
