# Implementation Plan: Class 3 WidgetWare SDR Context Package

Implement the structured, deterministic WidgetWare SDR context package following the exact specification in `SPEC.md`.

## Context & Objectives

The goal of Class 3 is to construct a testable, deterministic 5-layer context package in Python for a future AI Sales Development Representative (SDR) agent, without building an ADK agent, without calling LLMs, and without performing external actions.

## User Review Required

> [!NOTE]
> All in-scope files have been checked against `SPEC.md`. The configuration files, core logic, documentation, scenario fixtures, and automated test suite are already aligned and passing. We will run a complete verification pass and ensure clean formatting across all files.

## Proposed Changes & Status

### 1. Configuration Layer (`config/`)

#### [`config/products.yaml`](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/config/products.yaml)
- Define WidgetWare company description.
- Define two core offerings: *Plant Operations Platform* and *Industrial AI Accelerator*.
- Detail target buyer personas and approved claims with no unverified ROI/uptime promises.

#### [`config/icp.yaml`](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/config/icp.yaml)
- Define numeric company scale thresholds (`min_employee_count: 100`).
- Define preferred industries (Discrete Manufacturing, Process Manufacturing, Industrial Automation) and excluded industries (Retail, Financial Services, Hospitality).
- Specify target geographies, structured buying signals, and required account fields.

#### [`config/policies.yaml`](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/config/policies.yaml)
- Specify the 5 required evidence classifications: `verified_fact`, `derived_fact`, `inference`, `unknown`, `conflict`.
- Prohibit autonomous messaging, CRM data modifications, and pricing/contract commitments.
- Require explicit human approval for outreach and enforce strict isolation against prompt injection.

---

### 2. Documentation (`docs/`)

#### [`docs/widgetware-business-brief.md`](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/docs/widgetware-business-brief.md)
- Detail company background, ICP guidelines, product definitions, and SDR safety boundaries.

#### [`docs/acceptance-criteria.md`](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/docs/acceptance-criteria.md)
- Checklist covering configuration, context layer separation, policy guardrails, and scenario testing.

---

### 3. Core Implementation (`src/widgetware_sdr/`)

#### [`src/widgetware_sdr/instructions.py`](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/src/widgetware_sdr/instructions.py)
- Expose `get_system_instructions() -> str` defining the 8 core operational boundaries answering role, objective, information usage, evidence classification, handling uncertainty, prohibited actions, stopping criteria, and human escalation.

#### [`src/widgetware_sdr/context_builder.py`](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/src/widgetware_sdr/context_builder.py)
- Implement `build_context(account, objective, evidence, state=None, config_dir=None) -> dict`.
- Return 5 distinct layers: `system_instructions`, `business_context`, `task_context`, `retrieved_evidence`, `state`.
- Guarantee deep-copy non-mutation of inputs and deterministic YAML loading.

---

### 4. Scenario Fixtures & Test Suite (`tests/`)

#### Scenario Fixtures
- [`tests/scenarios/qualified_account.yaml`](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/tests/scenarios/qualified_account.yaml): Qualified manufacturing account with verified plant expansion signal.
- [`tests/scenarios/unqualified_account.yaml`](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/tests/scenarios/unqualified_account.yaml): Disqualified retail account below headcount threshold.
- [`tests/scenarios/insufficient_evidence.yaml`](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/tests/scenarios/insufficient_evidence.yaml): Missing headcount and industry triggering human escalation.
- [`tests/scenarios/prompt_injection.yaml`](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/tests/scenarios/prompt_injection.yaml): Malicious prompt injection attempt in account notes kept isolated within task context.

#### [`tests/unit/test_context_builder.py`](file:///home/pi-net/Documents/agent_eng_labs/agent_engineering/my-work/class-03/tests/unit/test_context_builder.py)
- Test configuration loading, safety boundary enforcement, evidence classifications, system instruction contents, 5-layer separation, input mutation protection, provenance preservation, missing fields handling, and scenario validations.

---

## Verification Plan

### Automated Tests
- Run `python -m pytest -v` using the virtual environment interpreter (`./venv/bin/pytest -v`).
- Verify all 16 tests pass across unit and scenario suites.
