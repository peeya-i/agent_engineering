# Implementation Plan - Class 3 WidgetWare SDR Context Package

Bounded technical implementation plan for constructing the WidgetWare SDR Context Package in `my-work/class-03/` as defined in `SPEC.md`.

## User Review Required

> [!IMPORTANT]
> **Strict Scope Boundaries**:
> - NO ADK agent building
> - NO Gemini or LLM API calls
> - NO web search, live research, email delivery, CRM access, database, or deployment code.
> - Purely deterministic Python context builder & YAML configurations.

## 1. Existing Workspace Files Analysis

The `my-work/class-03/` starter currently contains:
- `pyproject.toml` (Configured with `PyYAML>=6.0` runtime dependency and `pytest>=8.0` dev dependency)
- `.env.example`
- `README.md` (Starter README)
- `SPEC.md` & `LAB.md` (Specification & Lab instructions)
- `STARTER_CONTENTS.md`
- `config/.gitkeep`
- `docs/.gitkeep`
- `src/widgetware_sdr/__init__.py`
- `tests/unit/test_starter.py`
- `tests/scenarios/.gitkeep`
- `venv/` (Active virtual environment)

---

## 2. SPEC.md Requirements Overview

The outcome of Class 3 is a structured, testable **Context Package** for a future SDR agent. It mandates strict layer separation across **5 context layers**:
1. **System instructions**: Stable behavioral rules and safety guardrails.
2. **Business context**: Company offerings (`products.yaml`), fit rules (`icp.yaml`), safety policies (`policies.yaml`).
3. **Task context**: Target account data & research objective (untrusted input).
4. **Retrieved evidence**: Provenance-tracked claims classified as `verified_fact`, `derived_fact`, `inference`, `unknown`, or `conflict`.
5. **Workflow state**: Execution state tracker (defaults to `{}`).

---

## 3. Proposed Changes & File Operations

### Configuration Layer (`config/`)

#### [NEW] [products.yaml](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/config/products.yaml)
WidgetWare company overview, offerings (Plant Operations Platform, Industrial AI Accelerator), target buyers, approved claims, and boundaries.

#### [NEW] [icp.yaml](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/config/icp.yaml)
Ideal Customer Profile: minimum company size (numeric), preferred/excluded industries, target regions, buying signals, and required fields.

#### [NEW] [policies.yaml](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/config/policies.yaml)
Safety policies: 5 evidence classifications, prohibited actions (no emails, no CRM modifications, no invented facts), required human approvals, insufficient evidence rules, prompt injection handling.

---

### Documentation (`docs/`)

#### [NEW] [widgetware-business-brief.md](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/docs/widgetware-business-brief.md)
Executive brief on WidgetWare sales context, product offerings, target buyers, and SDR boundaries.

#### [NEW] [acceptance-criteria.md](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/docs/acceptance-criteria.md)
Acceptance checklist confirming layer separation, policy enforcement, scenario fixtures, and test coverage.

---

### Core Source Code (`src/widgetware_sdr/`)

#### [NEW] [instructions.py](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/src/widgetware_sdr/instructions.py)
Defines `get_system_instructions() -> str` returning inspectable, observable system instructions enforcing factual evidence requirements, prohibition of outreach/CRM edits, and prompt injection immutability.

#### [NEW] [context_builder.py](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/src/widgetware_sdr/context_builder.py)
Defines `build_context(account, objective, evidence, state=None, config_dir=None) -> dict` returning a dict containing all 5 context layers, loading YAML configs, preserving evidence provenance, keeping input dicts unmutated, and raising clear errors if config files are missing.

---

### Scenario Fixtures (`tests/scenarios/`)

#### [NEW] [qualified_account.yaml](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/tests/scenarios/qualified_account.yaml)
Fixture representing a target account matching industry, size, region, and buying signals with verified evidence.

#### [NEW] [unqualified_account.yaml](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/tests/scenarios/unqualified_account.yaml)
Fixture representing a disqualified account (below size threshold or in excluded industry).

#### [NEW] [insufficient_evidence.yaml](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/tests/scenarios/insufficient_evidence.yaml)
Fixture with missing key fields (unknown employee count/industry).

#### [NEW] [prompt_injection.yaml](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/tests/scenarios/prompt_injection.yaml)
Fixture containing malicious account notes trying to override safety policies or force unauthorized outreach.

---

### Tests & Documentation Updates (`tests/unit/` & Root)

#### [NEW] [test_context_builder.py](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/tests/unit/test_context_builder.py)
Automated unit tests covering:
1. Configuration loading & schema rules (`products`, `icp`, `policies`).
2. System instruction properties & policy precedence.
3. Context builder 5-layer assembly, default state handling, non-mutation of inputs, missing config handling.
4. Scenario tests for all 4 fixture files (`qualified`, `unqualified`, `insufficient_evidence`, `prompt_injection`).

#### [MODIFY] [README.md](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/README.md)
Update documentation with setup instructions, 5 context layer explanations, and verification commands.

---

## 4. Dependencies

- `PyYAML>=6.0,<7.0`: Required for reading `.yaml` configuration files and scenario fixtures.
- `pytest>=8.0,<9.0`: Required for test execution.
- Python `>=3.11` standard library (`pathlib`, `typing`, `copy`).

---

## 5. Verification & Testing Plan

### Automated Testing Command
```bash
python -m pytest -v
```

### Verification Criteria
- All tests in `tests/unit/test_context_builder.py` pass.
- Baseline starter test `test_starter_environment` passes.
- All 4 scenario fixtures load and behave as specified in `SPEC.md`.

---

## 6. Out of Scope Explicit Reminders

- No ADK agent.
- No LLM/Gemini API calls.
- No web search or scraping.
- No email/messaging delivery.
- No CRM integration.
- No database or external side effects.
