# Class 3 Acceptance Criteria

This document defines the acceptance criteria for the Class 3 WidgetWare SDR Context Package.

---

## 1. Configuration & Structure Requirements

- [x] `config/products.yaml` exists and defines at least two WidgetWare product offerings (`plant_operations_platform`, `industrial_ai_accelerator`).
- [x] `config/icp.yaml` defines numeric minimum company scale, preferred/excluded industries, target regions, and required fields.
- [x] `config/policies.yaml` specifies 5 evidence classifications (`verified_fact`, `derived_fact`, `inference`, `unknown`, `conflict`), prohibited actions, human approval requirements, and prompt injection policies.

---

## 2. Context Model & Layer Separation

- [x] The context builder (`src/widgetware_sdr/context_builder.py`) returns a dictionary with 5 separate layers:
  1. `system_instructions`
  2. `business_context`
  3. `task_context`
  4. `retrieved_evidence`
  5. `state`
- [x] System instructions are loaded from `src/widgetware_sdr/instructions.py` (`get_system_instructions()`).
- [x] Account details and user notes are placed strictly in `task_context`.
- [x] Input dictionaries are not mutated during context construction.
- [x] Missing configuration files trigger clear errors.

---

## 3. Policy & Safety Guardrails

- [x] External outreach (email, social messages) is strictly prohibited.
- [x] CRM modification is strictly prohibited without human approval.
- [x] Missing account fields are preserved as unknown and trigger `insufficient_evidence` policy.
- [x] Account notes containing prompt injection attempts cannot modify system instructions or safety policies.

---

## 4. Testing & Verification

- [x] Automated unit test suite `tests/unit/test_context_builder.py` passes via `python -m pytest -v`.
- [x] All 4 required scenario fixtures exist in `tests/scenarios/`:
  - `qualified_account.yaml`
  - `unqualified_account.yaml`
  - `insufficient_evidence.yaml`
  - `prompt_injection.yaml`
- [x] All scenario tests pass.
