# Class 02A Troubleshooting

Use this file before changing the agent implementation.

---

## Problem: `.env` is missing

Create it from the supplied example:

```bash
cp renewal_desk_agent/.env.example renewal_desk_agent/.env
```

Windows PowerShell:

```powershell
Copy-Item renewal_desk_agent\.env.example renewal_desk_agent\.env
```

The file belongs **inside `renewal_desk_agent/`**.

---

## Problem: API key vs Vertex AI is confusing

Pick **one** mode.

### AI Studio

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-3.7-flash
```

### Vertex AI

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=...
GOOGLE_CLOUD_LOCATION=us-central1
GEMINI_MODEL=gemini-3.7-flash
```

Then:

```bash
gcloud auth application-default login
```

Do not combine both modes.

---

## Problem: `No agent found`

Run ADK Web from the Class 02A **parent directory**:

```bash
adk web .
```

The current directory must contain:

```text
renewal_desk_agent/
```

Do not run it from inside `renewal_desk_agent/`.

---

## Problem: 404 / model unavailable

First check:

```text
renewal_desk_agent/.env
```

The starter uses:

```dotenv
GEMINI_MODEL=gemini-3.7-flash
```

Then run:

```bash
python scripts/preflight.py --online
```

Do not hard-code a random model into `agent.py`.

---

## Problem: 400 invalid API key

Check:

- key was copied completely;
- no extra quotes/spaces were pasted;
- `.env` is in `renewal_desk_agent/`;
- you selected the API-key mode;
- the key/account is permitted to use the Gemini API.

Never share the key on screen or commit it to Git.

---

## Problem: 429 / RESOURCE_EXHAUSTED

This is usually a quota, billing, rate-limit, or credit issue rather than a skill-code issue.

Run the live preflight and inspect the exact message.

Do not rewrite `SKILL.md` to fix an account quota problem.

---

## Problem: organization policy disallows API keys

Use an account/project where API keys are permitted, or switch to the Vertex AI path if your organization supports it.

This is an account/security-policy issue, not a lab-code issue.

---

## Problem: certificate verification failure

This is normally a local machine/network/corporate-certificate issue.

Do not disable TLS verification in the lab code.

Use your organization's supported certificate/network configuration.

---

## Problem: `pytest -q` fails before I start

That is expected.

First run:

```bash
python -m pytest -q tests/test_starter_integrity.py
```

That must pass.

The full suite intentionally checks whether you completed L1/L2 and `submission.md`.

---

## Problem: the agent answers correctly but loads everything

That is still a design failure for this lab.

The goal is **minimum sufficient context**, not only answer correctness.

Inspect the trace and tighten the L2 routing instructions.

---

## Problem: the agent says the discount is approved

The supplied policy only tells the agent how to route requests.

A requested or routed discount is not approved unless explicit approval evidence exists.

Fix the L2 state-language requirement.
