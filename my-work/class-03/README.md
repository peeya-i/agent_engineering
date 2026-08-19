# 🏭 Class 3 — WidgetWare SDR Context Package

This directory contains the Class 3 implementation of the WidgetWare SDR Context Package. It translates WidgetWare business concepts into a structured, testable, and deterministic context model for a future AI Sales Development Representative (SDR) agent.

---

## 🎯 Overview & Objectives

The primary objective of Class 3 is to construct a **Context Package** that enforces safety boundaries, evidence provenance, and strict separation across **5 context layers**:

1. **System Instructions**: Stable, inspectable behavioral rules for the agent (requires evidence for factual claims, prohibits autonomous outreach or CRM modification).
2. **Business Context**: Product offerings (`config/products.yaml`), Ideal Customer Profile rules (`config/icp.yaml`), and safety policies (`config/policies.yaml`).
3. **Task Context**: Target account information and research objective (treated as untrusted input).
4. **Retrieved Evidence**: Provenance-tracked claims classified as `verified_fact`, `derived_fact`, `inference`, `unknown`, or `conflict`.
5. **Workflow State**: Execution state tracker (defaults to `{}`).

---

## 📁 Repository Structure

```text
my-work/class-03/
├── README.md                           # Setup and documentation
├── SPEC.md                             # Class specification
├── LAB.md                              # Lab instructions
├── pyproject.toml                      # Dependencies (PyYAML, pytest)
├── config/
│   ├── products.yaml                   # WidgetWare offerings & approved claims
│   ├── icp.yaml                        # Ideal Customer Profile fit criteria
│   └── policies.yaml                   # Safety policies & evidence classifications
├── docs/
│   ├── widgetware-business-brief.md    # Executive business overview
│   └── acceptance-criteria.md          # Acceptance criteria checklist
├── src/
│   └── widgetware_sdr/
│       ├── __init__.py
│       ├── instructions.py             # System instructions retriever
│       └── context_builder.py          # Deterministic 5-layer context builder
└── tests/
    ├── unit/
    │   └── test_context_builder.py    # Automated unit and scenario test suite
    └── scenarios/
        ├── qualified_account.yaml      # Qualified account scenario fixture
        ├── unqualified_account.yaml    # Unqualified account scenario fixture
        ├── insufficient_evidence.yaml  # Missing information scenario fixture
        └── prompt_injection.yaml       # Safety & prompt injection defense fixture
```

---

## 🚀 Setup & Installation Guide

### Prerequisites
- Python 3.11+
- Active virtual environment (`venv`)

### Setup Instructions

```bash
# 1. Navigate to the class-03 workspace
cd my-work/class-03

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install the package in editable mode with development dependencies
pip install -e ".[dev]"
```

---

## 🧪 Running Automated Tests

Run the full test suite using `pytest`:

```bash
python -m pytest -v
```

### Expected Test Output:
```text
tests/unit/test_context_builder.py::test_config_files_exist_and_load PASSED [  6%]
tests/unit/test_context_builder.py::test_policies_contain_required_boundaries PASSED [ 12%]
tests/unit/test_context_builder.py::test_evidence_classifications_present PASSED [ 18%]
tests/unit/test_context_builder.py::test_instructions_contain_required_rules PASSED [ 25%]
tests/unit/test_context_builder.py::test_build_context_returns_five_layers PASSED [ 31%]
tests/unit/test_context_builder.py::test_build_context_default_state_handling PASSED [ 37%]
tests/unit/test_context_builder.py::test_input_mutation_prevention PASSED [ 43%]
tests/unit/test_context_builder.py::test_missing_config_raises_file_not_found_error PASSED [ 50%]
tests/unit/test_context_builder.py::test_evidence_provenance_preservation PASSED [ 56%]
tests/unit/test_context_builder.py::test_missing_account_fields_remain_unknown PASSED [ 62%]
tests/unit/test_context_builder.py::test_untrusted_notes_and_evidence_isolation PASSED [ 68%]
tests/unit/test_context_builder.py::test_scenario_qualified_account PASSED [ 75%]
tests/unit/test_context_builder.py::test_scenario_unqualified_account PASSED [ 81%]
tests/unit/test_context_builder.py::test_scenario_insufficient_evidence PASSED [ 87%]
tests/unit/test_context_builder.py::test_scenario_prompt_injection PASSED [ 93%]
tests/unit/test_starter.py::test_starter_environment PASSED              [100%]

============================== 16 passed in 0.19s ==============================
```

---

## 🛡️ Safety & Scope Boundaries

As required by `SPEC.md`, this implementation:
- ❌ Does **NOT** build an ADK agent.
- ❌ Does **NOT** call Gemini or any LLM API.
- ❌ Does **NOT** perform web search or scraping.
- ❌ Does **NOT** send emails or social messages.
- ❌ Does **NOT** modify CRM data or databases.
- ✅ Operates strictly deterministically in Python.
