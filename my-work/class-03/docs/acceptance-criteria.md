# Acceptance Criteria — Class 3 WidgetWare SDR Context Package

To pass Class 3 verification, the repository must meet all of the following observable criteria:

## 1. File Structure & Configuration
- [x] `config/products.yaml`, `config/icp.yaml`, and `config/policies.yaml` exist.
- [x] At least two WidgetWare offerings are configured.
- [x] ICP configuration specifies employee count thresholds, preferred/excluded industries, and required fields.
- [x] Policies explicitly declare evidence classifications (`verified_fact`, `derived_fact`, `inference`, `unknown`, `conflict`), prohibited actions, and human approval triggers.

## 2. Context Model & Isolation
- [x] System instructions are inspectable via `get_system_instructions()`.
- [x] The context builder `build_context()` returns five distinct context layers: `system_instructions`, `business_context`, `task_context`, `retrieved_evidence`, and `state`.
- [x] Account information is placed strictly inside `task_context`.
- [x] Input objects are never mutated by `build_context()`.
- [x] Provenance is preserved for every evidence item.

## 3. Security & Safety Boundaries
- [x] Untrusted inputs (such as `account_notes`) cannot alter `system_instructions` or `business_context`.
- [x] Unknown or missing fields remain `unknown` without hallucinating or inventing data.
- [x] Prompt-injection attempts cannot bypass safety policies or authorize external actions.

## 4. Scenarios & Testing
- [x] Four scenario fixtures exist under `tests/scenarios/`: `qualified_account.yaml`, `unqualified_account.yaml`, `insufficient_evidence.yaml`, and `prompt_injection.yaml`.
- [x] Automated unit and scenario tests pass completely via `python -m pytest -v`.

## 5. Scope Boundaries
- [x] No Google ADK agent code is included.
- [x] No Gemini or LLM API calls exist.
- [x] No live web search or external research is performed.
- [x] No email, social message, CRM write, database access, or deployment code is present.
