# Class 3 — WidgetWare SDR Context Package

This repository contains the structured, testable context package for WidgetWare SDR in Class 3.

## Context Model

The system maintains 5 strictly separated context layers:

1. **System Instructions**: Stable behavioral guidelines, observable requirements, and safety policies.
2. **Business Context**: Products (`config/products.yaml`), ICP definitions (`config/icp.yaml`), and policies (`config/policies.yaml`).
3. **Task Context**: Target account parameters (`account`) and research goals (`objective`). Untrusted account notes remain in task context.
4. **Retrieved Evidence**: Evidence records preserving source provenance (`claim`, `classification`, `source`, `excerpt`).
5. **Workflow State**: Execution state object (defaults to `{}` when omitted).

## Workspace Structure

```text
my-work/class-03/
├── README.md
├── SPEC.md
├── LAB.md
├── pyproject.toml
├── .env.example
├── config/
│   ├── products.yaml
│   ├── icp.yaml
│   └── policies.yaml
├── docs/
│   ├── widgetware-business-brief.md
│   └── acceptance-criteria.md
├── src/
│   └── widgetware_sdr/
│       ├── __init__.py
│       ├── instructions.py
│       └── context_builder.py
└── tests/
    ├── unit/
    │   ├── test_starter.py
    │   └── test_context_builder.py
    └── scenarios/
        ├── qualified_account.yaml
        ├── unqualified_account.yaml
        ├── insufficient_evidence.yaml
        └── prompt_injection.yaml
```

## Setup & Testing

Install dependencies:
```bash
python -m pip install -e ".[dev]"
```

Run test suite:
```bash
python -m pytest -v
```

## Boundaries

Class 3 strictly excludes:
- ADK Agent construction
- Gemini / LLM calls
- Live web search
- Email/social message sending
- CRM integration / writes
- Database persistence
- Deployment code
