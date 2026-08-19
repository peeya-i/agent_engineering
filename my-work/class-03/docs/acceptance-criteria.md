# Class 3 Acceptance Criteria Checklist

| Category | Observable Condition | Status |
|---|---|:---:|
| **Configuration** | `config/products.yaml` exists, loads valid YAML, defines $\ge 2$ offerings and approved claims | ✅ |
| **Configuration** | `config/icp.yaml` exists, defines numeric `minimum_employee_count`, preferred & excluded industries | ✅ |
| **Configuration** | `config/policies.yaml` exists, specifies 5 evidence classifications, prohibits CRM edits/messages, requires human approval | ✅ |
| **Documentation** | `docs/widgetware-business-brief.md` and `docs/acceptance-criteria.md` exist and provide accurate context | ✅ |
| **Instructions** | `src/widgetware_sdr/instructions.py` exports `get_system_instructions()` with stable, observable safety rules | ✅ |
| **Context Builder** | `src/widgetware_sdr/context_builder.py` returns 5 separate context layers without mutating inputs | ✅ |
| **Context Builder** | Missing configuration files raise explicit `FileNotFoundError` | ✅ |
| **Provenance** | Evidence records retain source metadata, retrieval date, and classifications | ✅ |
| **Unknowns** | Missing account fields remain unknown and are never hallucinated or invented | ✅ |
| **Security & Safety** | Untrusted account notes cannot override system instructions or policies (prompt injection defense) | ✅ |
| **Scenarios** | 4 scenario fixtures exist in `tests/scenarios/` (Qualified, Unqualified, Insufficient Evidence, Prompt Injection) | ✅ |
| **Testing** | All unit and scenario tests in `tests/unit/test_context_builder.py` pass cleanly | ✅ |
| **Scope Boundaries** | No Google ADK agent, no LLM API calls, no web scraping, no CRM/email side-effects | ✅ |
